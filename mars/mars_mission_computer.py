import random  
import json  
import time  
import platform  
import multiprocessing  
import os
import threading  

class MissionComputer:  
    def __init__(self):  
        self.env_values = {}
    def get_sensor_data(self):  
        while True:  
            ds.set_env()  
            self.env_values = ds.get_env()  
            print(json.dumps(self.env_values, indent=4))  
            time.sleep(5)
    def get_mission_computer_info(self):  
        while True:  
            try:  
                info = {  
                    'os': platform.system(),  
                    'os_version': platform.release(),  
                    'cpu_type': platform.processor(),  
                    'cpu_cores': multiprocessing.cpu_count(),  
                    'memory_size_gb': round(os.sysconf('SC_PHYS_PAGES') * os.sysconf('SC_PAGE_SIZE') / (1024 ** 3), 2)  
                }  
                print(json.dumps(info, indent=4))  
            except Exception as e:  
                print(f'Error getting system info: {e}')
            print(json.dumps(info, indent=4))  
            time.sleep(20)
    def get_mission_computer_load(self):  
        while True:  
            try:  
                load = {  
                    'cpu_usage_percent': round(os.getloadavg()[0] / multiprocessing.cpu_count() * 100, 2)  
                }  
                with open('/proc/meminfo', 'r') as f:  
                    meminfo = f.readlines()  
                mem_total = int([x for x in meminfo if 'MemTotal' in x][0].split()[1])  
                mem_free = int([x for x in meminfo if 'MemFree' in x][0].split()[1])  
                load['memory_usage_percent'] = round((mem_total - mem_free) / mem_total * 100, 2)  
                print(json.dumps(load, indent=4))  
            except Exception as e:  
                print(f'Error getting load: {e}')
            print(json.dumps(load, indent=4))  
            time.sleep(20)
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
    
def run_instance(computer):  
    computer.get_mission_computer_info()  
    computer.get_mission_computer_load()  
    computer.get_sensor_data()
ds = DummySensor()
ds.set_env()  
print(ds.get_env()) 
RunComputer = MissionComputer()
RunComputer.get_sensor_data()
runComputer = MissionComputer()  
runComputer.get_mission_computer_info()  
runComputer.get_mission_computer_load()



t1 = threading.Thread(target=runComputer.get_mission_computer_info)  
t2 = threading.Thread(target=runComputer.get_mission_computer_load)  
t3 = threading.Thread(target=runComputer.get_sensor_data)  
t1.start()  
t2.start()  
t3.start()  
t1.join()  
t2.join()  
t3.join()

runComputer1 = MissionComputer()  
runComputer2 = MissionComputer()  
runComputer3 = MissionComputer()

p1 = multiprocessing.Process(target=run_instance, args=(runComputer1,))  
p2 = multiprocessing.Process(target=run_instance, args=(runComputer2,))  
p3 = multiprocessing.Process(target=run_instance, args=(runComputer3,))  
p1.start()  
p2.start()  
p3.start()  
p1.join()  
p2.join()  
p3.join()