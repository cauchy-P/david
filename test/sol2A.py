import math


def sphere_area(diameter: float, material: str, thickness: float = 1.0):
    if not math.isfinite(diameter) or not math.isfinite(thickness):
        raise ValueError
    if diameter <= 0 or thickness <= 0:
        raise ValueError
    material = material.strip()
    densities = {'유리': 2.4, '알루미늄': 2.7, '탄소강': 7.85}
    if material not in densities:
        raise ValueError
    area = math.pi * (diameter ** 2)
    mass = densities[material] * area * 10000.0 * thickness / 1000.0
    return area, mass * 0.38


print(sphere_area(3, "유리", 5))
