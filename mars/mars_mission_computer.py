import random
import time
import json
import platform
import os
import multiprocessing

class DummySensor:
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': 0,
            'mars_base_external_temperature': 0,
            'mars_base_internal_humidity': 0,
            'mars_base_external_illuminance': 0,
            'mars_base_internal_co2': 0,
            'mars_base_internal_oxygen': 0
        }

    def set_env(self):
        self.env_values['mars_base_internal_temperature'] = random.randint(18, 30)
        self.env_values['mars_base_external_temperature'] = random.randint(0, 21)
        self.env_values['mars_base_internal_humidity'] = random.randint(50, 60)
        self.env_values['mars_base_external_illuminance'] = random.randint(500, 715)
        self.env_values['mars_base_internal_co2'] = round(random.uniform(0.02, 0.1), 2)
        self.env_values['mars_base_internal_oxygen'] = round(random.uniform(4, 7), 2)

    def get_env(self):
        return self.env_values

class MissionComputer:
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': 0,
            'mars_base_external_temperature': 0,
            'mars_base_internal_humidity': 0,
            'mars_base_external_illuminance': 0,
            'mars_base_internal_co2': 0,
            'mars_base_internal_oxygen': 0
        }
        self.ds = DummySensor()

    def get_sensor_data(self):
        time.sleep(random.uniform(0, 2))  # 초기 지연으로 stagger
        pid = multiprocessing.current_process().pid
        while True:
            self.ds.set_env()
            self.env_values = self.ds.get_env()
            print(f"Process {pid} (Sensor): \n{json.dumps(self.env_values, indent=4)}")
            time.sleep(5)

    def get_mission_computer_info(self):
        time.sleep(random.uniform(0, 2))
        pid = multiprocessing.current_process().pid
        while True:
            try:
                info = {
                    'os': platform.system(),
                    'os_version': platform.release(),
                    'cpu_type': platform.processor(),
                    'cpu_cores': os.cpu_count()
                }
                if platform.system() == 'Linux':
                    with open('/proc/meminfo') as f:
                        meminfo = f.read()
                    total_mem = int([line for line in meminfo.splitlines() if line.startswith('MemTotal')][0].split()[1]) / 1024 ** 2  # GB
                    info['memory_size'] = round(total_mem, 2)
                else:
                    info['memory_size'] = 'Not available on this OS'
                print(f"Process {pid} (Info): \n{json.dumps(info, indent=4)}")
            except Exception as e:
                print(f'Error getting system info: {e}')
            time.sleep(20)

    def get_mission_computer_load(self):
        time.sleep(random.uniform(0, 2))
        pid = multiprocessing.current_process().pid
        while True:
            try:
                load = {}
                if platform.system() == 'Linux':
                    with open('/proc/stat') as f:
                        lines = f.read().splitlines()
                    cpu = lines[0].split()[1:]
                    idle1 = int(cpu[3]) + int(cpu[4])
                    total1 = sum(int(x) for x in cpu)
                    time.sleep(1)
                    with open('/proc/stat') as f:
                        lines = f.read().splitlines()
                    cpu = lines[0].split()[1:]
                    idle2 = int(cpu[3]) + int(cpu[4])
                    total2 = sum(int(x) for x in cpu)
                    delta_idle = idle2 - idle1
                    delta_total = total2 - total1
                    cpu_percent = 100 * (1 - delta_idle / delta_total) if delta_total != 0 else 0.0
                    load['cpu_usage'] = round(cpu_percent, 2)

                    with open('/proc/meminfo') as f:
                        meminfo = f.read()
                    lines = meminfo.splitlines()
                    total = int([line for line in lines if line.startswith('MemTotal')][0].split()[1])
                    free = int([line for line in lines if line.startswith('MemFree')][0].split()[1])
                    available = int([line for line in lines if line.startswith('MemAvailable')][0].split()[1])
                    used = total - available
                    memory_percent = (used / total) * 100
                    load['memory_usage'] = round(memory_percent, 2)
                else:
                    load['cpu_usage'] = 'Not available on this OS'
                    load['memory_usage'] = 'Not available on this OS'
                print(f"Process {pid} (Load): \n{json.dumps(load, indent=4)}")
            except Exception as e:
                print(f'Error getting load: {e}')
            time.sleep(20)

def run_info():
    rc = MissionComputer()
    rc.get_mission_computer_info()

def run_load():
    rc = MissionComputer()
    rc.get_mission_computer_load()

def run_sensor():
    rc = MissionComputer()
    rc.get_sensor_data()

if __name__ == '__main__':
    p1 = multiprocessing.Process(target=run_info, name='runComputer1')
    p2 = multiprocessing.Process(target=run_load, name='runComputer2')
    p3 = multiprocessing.Process(target=run_sensor, name='runComputer3')
    p1.start()
    p2.start()
    p3.start()
    p1.join()
    p2.join()
    p3.join()