#!/usr/bin/env python3
'''Smart farm sensor simulation with queue-based persistence.

This module simulates multiple Parm sensors that periodically produce
temperature, light, and humidity readings. Records are pushed into a queue,
persisted to a MySQL database, and stored
in an in-memory table for rolling averages. A simple ASCII graph is printed
at the end showing per-sensor hourly temperature averages. Humidity spikes
above 90% are highlighted with red markers when present in the dataset.
'''
# NOTE for junior developers
# -------------------------
# 이 파일은 스마트 팜 센서 5개를 시뮬레이션하여, 주기적으로(기본 10초)
# 데이터(온도/조도/습도)를 생성하고 출력합니다. 출력된 데이터는 바로 DB에
# 넣지 않고 먼저 FIFO 큐(sensorQ)에 저장되며, 별도의 쓰레드가 큐의 내용을
# 1초 단위로 가져와 MySQL 데이터베이스의 parm_data 테이블에 INSERT 합니다.
#
# 구성 요약
# - ParmSensor: 센서 1개를 나타내는 클래스 (난수로 값을 생성)
# - SensorDataFrame: 최근 데이터를 메모리에 보관하고 5분 평균을 계산
# - DatabaseManager: MySQL 연결/테이블 생성/INSERT/SELECT 담당
# - sensor_worker: 센서 1개당 실행되는 쓰레드(값 생성 → 출력 → 큐에 push)
# - queue_worker: 큐에서 데이터를 가져와 DB에 저장하는 쓰레드
# - average_worker: 5분 롤링 평균을 주기적으로 출력하는 쓰레드
# - plot_temperature_trends: DB에서 읽은 값으로 시간대(시 단위) 평균 온도 그래프 출력
#
# 실행 방법(기본 설정)
#   python3 sol3/smart_farm.py
#
# MySQL 연결 설정을 바꾸려면 run_simulation(db_config={ ... }) 인자로
# host/port/user/password/database 값을 전달하세요. 최초 실행 시 지정한 DB가 없으면
# 자동으로 생성한 후 테이블도 준비합니다(권한 필요).

from __future__ import annotations

import random
import threading
import time
from collections import defaultdict, deque
from dataclasses import dataclass
from datetime import datetime, timedelta
from queue import Queue, Empty
from typing import Deque, Dict, Iterable, List, Optional, Tuple

try:
    import mysql.connector as mysql_connector
    from mysql.connector import errorcode as mysql_errorcode
except ImportError as error:  # pragma: no cover - import failure handled at runtime.
    mysql_connector = None  # type: ignore[assignment]
    mysql_errorcode = None  # type: ignore[assignment]
    MYSQL_IMPORT_ERROR = error
else:
    MYSQL_IMPORT_ERROR = None

TEMP_RANGE: Tuple[int, int] = (20, 30)        # 온도 범위
LIGHT_RANGE: Tuple[int, int] = (5000, 10000)  # 조도 범위
HUMIDITY_RANGE: Tuple[int, int] = (40, 70)    # 습도 범위

SENSOR_NAMES: Tuple[str, ...] = (
    'Parm-1',
    'Parm-2',
    'Parm-3',
    'Parm-4',
    'Parm-5',
)

# MySQL 기본 연결 설정. run_simulation(db_config=...)으로 덮어쓸 수 있습니다.
DEFAULT_DB_CONFIG: Dict[str, object] = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': '',
    'database': 'smart_farm',
}


@dataclass(frozen=True)
class SensorRecord:
    '''Immutable container for a sensor reading.'''

    timestamp: datetime
    sensor_name: str
    temperature: int
    light: int
    humidity: int


class ParmSensor:
    '''Simulates a smart farm sensor producing random readings.'''

    def __init__(self, name: str) -> None:
        self.name = name
        self.temperature = TEMP_RANGE[0]
        self.light = LIGHT_RANGE[0]
        self.humidity = HUMIDITY_RANGE[0]
        self.lock = threading.Lock()

    def set_data(self) -> None:
        '''Populate the sensor with fresh random values within the limits.'''
        # 잠금(lock)을 사용하여 set/get 시점이 겹쳐도 안전하게 보호합니다.
        with self.lock:
            self.temperature = random.randint(*TEMP_RANGE)
            self.light = random.randint(*LIGHT_RANGE)
            self.humidity = random.randint(*HUMIDITY_RANGE)

    def get_data(self) -> Tuple[int, int, int]:
        '''Return the current sensor readings.'''
        with self.lock:
            return self.temperature, self.light, self.humidity


class SensorDataFrame:
    '''Lightweight in-memory tabular structure for sensor data.'''

    def __init__(self, max_records: int = 2048) -> None:
        self._records: Deque[SensorRecord] = deque(maxlen=max_records)
        self._lock = threading.Lock()

    def append(self, record: SensorRecord) -> None:
        '''Append a new record, keeping the structure thread-safe.'''
        # deque(maxlen=...)에 쌓아 최근 일정량만 보관합니다.
        with self._lock:
            self._records.append(record)

    def iter_recent(self, interval: timedelta) -> Iterable[SensorRecord]:
        '''Yield records that fall within the provided time interval.'''
        threshold = datetime.now() - interval
        with self._lock:
            return [record for record in self._records if record.timestamp >= threshold]

    def calculate_averages(self, interval: timedelta) -> Dict[str, Dict[str, float]]:
        '''Compute per-sensor averages over a rolling interval.'''
        # interval(기본 5분) 내의 값들만 모아 평균을 계산합니다.
        recent_records = self.iter_recent(interval)
        grouped: Dict[str, List[SensorRecord]] = defaultdict(list)
        for record in recent_records:
            grouped[record.sensor_name].append(record)

        averages: Dict[str, Dict[str, float]] = {}
        for sensor_name, sensor_records in grouped.items():
            count = len(sensor_records)
            if count == 0:
                continue
            temp_sum = sum(rec.temperature for rec in sensor_records)
            light_sum = sum(rec.light for rec in sensor_records)
            humidity_sum = sum(rec.humidity for rec in sensor_records)
            averages[sensor_name] = {
                'temperature': temp_sum / count,
                'light': light_sum / count,
                'humidity': humidity_sum / count,
                'count': float(count),
            }
        return averages


class DatabaseManager:
    '''MySQL-backed persistence layer that provides the requested schema.'''

    def __init__(
        self,
        host: str,
        port: int,
        user: str,
        password: str,
        database: str,
    ) -> None:
        if mysql_connector is None:  # pragma: no cover - handled via runtime error.
            raise RuntimeError(
                'mysql.connector module is required. Install mysql-connector-python.'
            ) from MYSQL_IMPORT_ERROR
        # 전달받은 연결 설정을 보관합니다.
        self.config = {
            'host': host,
            'port': port,
            'user': user,
            'password': password,
            'database': database,
        }
        self._lock = threading.Lock()
        self._initialize()

    def _initialize(self) -> None:
        '''Prepare the parm_data table if it does not yet exist.'''
        # 1) 지정한 DB로 접속을 시도합니다.
        # 2) DB가 없으면(_should_attempt_database_create) 자동으로 생성합니다.
        try:
            connection = self._connect()
        except Exception as error:
            if self._should_attempt_database_create(error):
                self._create_database()
                connection = self._connect()
            else:
                raise
        try:
            cursor = connection.cursor()
            # 센서 데이터를 저장할 테이블을 준비합니다.
            cursor.execute(
                '''
                CREATE TABLE IF NOT EXISTS parm_data (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    sensor_name VARCHAR(64) NOT NULL,
                    timestamp DATETIME NOT NULL,
                    temperature INT NOT NULL,
                    light INT NOT NULL,
                    humidity INT NOT NULL
                )
                '''
            )
            connection.commit()
        finally:
            cursor.close()
            connection.close()

    def insert_sensor_data(self, record: SensorRecord) -> None:
        '''Persist a sensor record into the database.'''
        with self._lock:
            connection = self._connect()
            try:
                cursor = connection.cursor()
                # 파라미터 바인딩으로 안전하게 INSERT 합니다.
                cursor.execute(
                    '''
                    INSERT INTO parm_data (sensor_name, timestamp, temperature, light, humidity)
                    VALUES (%s, %s, %s, %s, %s)
                    ''',
                    (
                        record.sensor_name,
                        record.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                        record.temperature,
                        record.light,
                        record.humidity,
                    ),
                )
                connection.commit()
            finally:
                cursor.close()
                connection.close()

    def get_sensor_data(self) -> List[SensorRecord]:
        '''Fetch all sensor records ordered by timestamp.'''
        # 전체 레코드를 시간순으로 조회하여 SensorRecord 리스트로 변환합니다.
        connection = self._connect()
        try:
            cursor = connection.cursor()
            cursor.execute(
                '''
                SELECT sensor_name, timestamp, temperature, light, humidity
                FROM parm_data
                ORDER BY timestamp ASC
                '''
            )
            rows = cursor.fetchall()
        finally:
            cursor.close()
            connection.close()
        records: List[SensorRecord] = []
        for sensor_name, timestamp_value, temperature, light, humidity in rows:
            if isinstance(timestamp_value, datetime):
                timestamp = timestamp_value
            else:
                timestamp = datetime.strptime(str(timestamp_value), '%Y-%m-%d %H:%M:%S')
            records.append(
                SensorRecord(
                    timestamp=timestamp,
                    sensor_name=sensor_name,
                    temperature=int(temperature),
                    light=int(light),
                    humidity=int(humidity),
                )
            )
        return records

    def get_sensor_counts(self) -> Dict[str, int]:
        '''Return the number of stored points per sensor.'''
        # 센서별 저장된 데이터 개수를 반환합니다.
        connection = self._connect()
        try:
            cursor = connection.cursor()
            cursor.execute(
                '''
                SELECT sensor_name, COUNT(*) FROM parm_data GROUP BY sensor_name
                '''
            )
            rows = cursor.fetchall()
        finally:
                cursor.close()
                connection.close()
        return {sensor_name: int(count) for sensor_name, count in rows}

    def _connect(self):
        if mysql_connector is None:  # pragma: no cover - defensive guard.
            raise RuntimeError(
                'mysql.connector module is required. Install mysql-connector-python.'
            )
        return mysql_connector.connect(**self.config)

    def _create_database(self) -> None:
        # database가 없을 때 1회 생성합니다(권한 필요).
        database_name = str(self.config['database'])
        base_config = self.config.copy()
        base_config.pop('database', None)
        connection = mysql_connector.connect(**base_config)
        try:
            cursor = connection.cursor()
            cursor.execute(f'CREATE DATABASE IF NOT EXISTS `{database_name}`')
            connection.commit()
        finally:
            cursor.close()
            connection.close()

    def _should_attempt_database_create(self, error: Exception) -> bool:
        # 에러 코드가 "Unknown database"인 경우에만 DB 생성을 시도합니다.
        if mysql_errorcode is None:
            return False
        if not isinstance(error, mysql_connector.Error):
            return False
        return getattr(error, 'errno', None) == mysql_errorcode.ER_BAD_DB_ERROR


def sensor_worker(
    sensor: ParmSensor,
    sensorQ: Queue,
    data_frame: SensorDataFrame,
    stop_event: threading.Event,
    interval_seconds: int,
) -> None:
    '''Background worker producing sensor readings every interval.'''
    # 1) 센서 값을 생성하고 2) 화면에 출력, 3) 메모리 데이터프레임에 보관,
    # 4) sensorQ에 push 하여 DB 쓰레드가 저장하게 합니다.
    while not stop_event.is_set():
        sensor.set_data()
        temperature, light, humidity = sensor.get_data()
        record = SensorRecord(
            timestamp=datetime.now(),
            sensor_name=sensor.name,
            temperature=temperature,
            light=light,
            humidity=humidity,
        )
        data_frame.append(record)
        print(
            f'{record.timestamp:%Y-%m-%d %H:%M:%S} {sensor.name} — '
            f'temp {temperature:02d}, light {light:05d}, humi {humidity:02d}'
        )
        sensorQ.put(record)
        if stop_event.wait(interval_seconds):
            break


def queue_worker(
    sensorQ: Queue,
    db_manager: DatabaseManager,
    stop_event: threading.Event,
) -> None:
    '''Persist queued sensor data at roughly one-second intervals.'''
    # 1초에 한 번씩 큐에서 데이터를 꺼내 insert_sensor_data를 호출합니다.
    # 프로그램 종료 시에도 큐가 빌 때까지 계속 처리합니다.
    while not stop_event.is_set() or not sensorQ.empty():
        try:
            record = sensorQ.get(timeout=1)
        except Empty:
            continue
        db_manager.insert_sensor_data(record)
        sensorQ.task_done()


def average_worker(
    data_frame: SensorDataFrame,
    stop_event: threading.Event,
    average_interval: int,
) -> None:
    '''Periodically print five-minute rolling averages.'''
    # average_interval(기본 300초)마다 최근 구간의 평균을 출력합니다.
    interval = timedelta(seconds=average_interval)
    while not stop_event.is_set():
        if stop_event.wait(average_interval):
            break
        _print_rolling_averages(data_frame, interval)
    # Ensure at least one summary is printed on exit.
    _print_rolling_averages(data_frame, interval)


def _print_rolling_averages(data_frame: SensorDataFrame, interval: timedelta) -> None:
    averages = data_frame.calculate_averages(interval)
    if not averages:
        print('No sensor data available for rolling average window.')
        return
    print(f'Rolling averages for last {int(interval.total_seconds())} seconds:')
    for sensor_name in sorted(averages):
        stats = averages[sensor_name]
        print(
            f"  {sensor_name}: temp {stats['temperature']:.1f}, "
            f"light {stats['light']:.1f}, humi {stats['humidity']:.1f} "
            f"({int(stats['count'])} samples)"
        )


def plot_temperature_trends(records: Iterable[SensorRecord]) -> None:
    '''Render a simple ASCII chart of hourly average temperatures per sensor.'''
    # 레코드를 센서/시간대(시 단위)로 묶어서 평균 온도를 텍스트 그래프로 출력합니다.
    # 같은 시간대에서 습도 90%를 초과한 값이 하나라도 있으면 빨간색 느낌표로 표시합니다.
    grouped: Dict[str, Dict[datetime, List[SensorRecord]]] = defaultdict(lambda: defaultdict(list))
    for record in records:
        hour_slot = record.timestamp.replace(minute=0, second=0, microsecond=0)
        grouped[record.sensor_name][hour_slot].append(record)

    if not grouped:
        print('No persisted data available for plotting.')
        return

    for sensor_name in sorted(grouped):
        print(f'\nTemperature profile for {sensor_name}')
        sensor_data = grouped[sensor_name]
        averages: List[Tuple[datetime, float, bool]] = []
        max_temp = 0.0
        for hour_slot, bucket in sorted(sensor_data.items()):
            average_temp = sum(item.temperature for item in bucket) / len(bucket)
            has_humidity_spike = any(item.humidity > 90 for item in bucket)
            averages.append((hour_slot, average_temp, has_humidity_spike))
            if average_temp > max_temp:
                max_temp = average_temp

        if max_temp == 0:
            max_temp = 1.0

        scale = max_temp / 40.0 if max_temp > 40 else 1.0
        for hour_slot, average_temp, has_spike in averages:
            bar_length = int(average_temp / scale)
            bar = '#' * bar_length
            suffix = ''
            if has_spike:
                suffix = ' \033[31m!\033[0m humidity > 90%'
            print(
                f'{hour_slot:%Y-%m-%d %H:%M} | {bar:<40} {average_temp:5.1f}°C{suffix}'
            )


def run_simulation(
    runtime_seconds: int = 120,
    sensor_interval: int = 10,
    average_interval: int = 300,
    db_config: Optional[Dict[str, object]] = None,
) -> None:
    '''Coordinate sensors, queue, and persistence for a limited runtime.'''
    # 전체 파이프라인을 구성하고 주어진 시간(runtime_seconds) 동안 실행합니다.
    # - sensor_worker (N개): 10초 간격으로 데이터 생성 → 출력 → sensorQ push
    # - queue_worker (1개): sensorQ pop → DB INSERT
    # - average_worker (1개): 5분 평균 출력
    stop_event = threading.Event()
    sensorQ: Queue = Queue()
    data_frame = SensorDataFrame()
    config = DEFAULT_DB_CONFIG.copy()
    if db_config:
        config.update(db_config)
    db_manager = DatabaseManager(
        host=str(config['host']),
        port=int(config['port']),
        user=str(config['user']),
        password=str(config['password']),
        database=str(config['database']),
    )

    sensors = [ParmSensor(name) for name in SENSOR_NAMES]
    sensor_threads = [
        threading.Thread(
            target=sensor_worker,
            args=(sensor, sensorQ, data_frame, stop_event, sensor_interval),
            daemon=True,
        )
        for sensor in sensors
    ]

    # 센서 쓰레드들을 시작합니다.
    for thread in sensor_threads:
        thread.start()

    queue_thread = threading.Thread(
        target=queue_worker,
        args=(sensorQ, db_manager, stop_event),
        daemon=True,
    )
    average_thread = threading.Thread(
        target=average_worker,
        args=(data_frame, stop_event, average_interval),
        daemon=True,
    )
    queue_thread.start()
    average_thread.start()

    try:
        time.sleep(runtime_seconds)
    except KeyboardInterrupt:
        print('\nSimulation interrupted by user.')
    finally:
        stop_event.set()
        for thread in sensor_threads:
            thread.join()
        queue_thread.join()
        sensorQ.join()
        average_thread.join()

    print('\nSensor data counts per device:')
    counts = db_manager.get_sensor_counts()
    for sensor_name in sorted(counts):
        print(f'  {sensor_name}: {counts[sensor_name]} samples')

    # 저장된 전체 데이터를 가져와 ASCII 그래프를 출력합니다.
    records = db_manager.get_sensor_data()
    plot_temperature_trends(records)


if __name__ == '__main__':
    run_simulation()
