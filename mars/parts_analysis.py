import numpy as np  

try:  
    arr1 = np.genfromtxt('mars_base_main_parts-001.csv', delimiter=',', skip_header=1, dtype=[('parts', 'U50'), ('strength', 'i4')])  
    arr2 = np.genfromtxt('mars_base_main_parts-002.csv', delimiter=',', skip_header=1, dtype=[('parts', 'U50'), ('strength', 'i4')])  
    arr3 = np.genfromtxt('mars_base_main_parts-003.csv', delimiter=',', skip_header=1, dtype=[('parts', 'U50'), ('strength', 'i4')])  
except FileNotFoundError:  
    print('One or more files not found.')  
except Exception as e:  
    print(f'Unexpected error: {e}')  

parts = np.concatenate((arr1, arr2, arr3))  

unique_parts = np.unique(parts['parts'])  
averages = {}  
for part in unique_parts:  
    strengths = parts['strength'][parts['parts'] == part]  
    averages[part] = np.mean(strengths)  

low_avg_parts = {k: v for k, v in averages.items() if v < 50}  
try:  
    with open('parts_to_work_on.csv', 'w', encoding='utf-8') as csv_file:  
        csv_file.write('parts,average_strength\n')  
        for part, avg in low_avg_parts.items():  
            csv_file.write(f'{part},{round(avg, 3)}\n')  
except Exception as e:  
    print(f'Error saving CSV: {e}')  