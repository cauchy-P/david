import math  

def sphere_area(diameter, material, thickness=1):  
    if diameter <= 0 or thickness <= 0:  
        raise ValueError('Diameter and thickness must be positive.')  
    radius = diameter / 2  
    surface_area = 2 * math.pi * radius ** 2  # 반구 표면적  
    densities = {'glass': 2.4, 'aluminum': 2.7, 'carbon_steel': 7.85}  
    if material not in densities:  
        raise ValueError('Invalid material.')  
    volume = surface_area * (thickness / 100)  # cm로 변환  
    weight_earth = densities[material] * volume * 1000  # kg으로 변환  
    weight_mars = weight_earth * 0.38  
    return round(surface_area, 3), round(weight_mars, 3)  

while True:  
    try:  
        material = input('Enter material (glass, aluminum, carbon_steel): ')  
        diameter = float(input('Enter diameter (m): '))  
        area, weight = sphere_area(diameter, material)  
        print(f'재질 ⇒ {material}, 지름 ⇒ {diameter}, 두께 ⇒ 1, 면적 ⇒ {area}, 무게 ⇒ {weight} kg')  
    except ValueError as ve:  
        print(f'Invalid input: {ve}')  
    except Exception as e:  
        print(f'Unexpected error: {e}')  
    if input('Continue? (y/n): ').lower() != 'y':  
        break  


    import numpy as np  

try:  
    arr1 = np.genfromtxt('mars_base_main_parts-001.csv', delimiter=',', skip_header=1, dtype=[('parts', 'U50'), ('strength', 'i4')])  
    arr2 = np.genfromtxt('mars_base_main_parts-002.csv', delimiter=',', skip_header=1, dtype=[('parts', 'U50'), ('strength', 'i4')])  
    arr3 = np.genfromtxt('mars_base_main_parts-003.csv', delimiter=',', skip_header=1, dtype=[('parts', 'U50'), ('strength', 'i4')])  
except FileNotFoundError:  
    print('One or more files not found.')  
except Exception as e:  
    print(f'Unexpected error: {e}')  