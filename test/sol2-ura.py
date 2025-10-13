import math
densities = {'유리':2.4,'알루미늄':2.7,'탄소강':7.85}
def sphere_area(diameter: float, material:str, thickness:float=1.0):
    if diameter <= 0 or thickness <= 0 or \
        not math.isfinite(diameter) or not math.isfinite(thickness) or\
        material not in densities:
        raise ValueError
    area_m2 = math.pi * diameter * diameter
    area_cm2 = area_m2 * 10000
    volume_cm3 = area_cm2 * thickness
    mass_kg = densities[material] * volume_cm3 / 1000
    return area_m2, mass_kg * 0.38
def main():
    try:
        d_raw = input('지름(m)을 입력하세요:').strip()
        if not d_raw:
            raise ValueError
        try:
            d = float(d_raw)
        except ValueError:
            raise ValueError
        if d <= 0:
            raise ValueError
        mat = input('재질(유리/알루미늄/탄소강)을 입력하세요:').strip()
        if mat not in densities:
            raise ValueError
        th = input('두께(cm)을 입력하세요:').strip()
        if not th:
            th = 1.0
        try:
            t = float(th)
        except ValueError:
            raise ValueError
        if t <= 0:
            raise ValueError
        A, wM = sphere_area(d, mat, t)
        print(f'재질 : {mat}, 지름: {d:g}, 두께: {t:g}, 면적: {A:.3f}, 무게{wM:.3f}kg')

    except ValueError:
        print('Invalid input.')
    except Exception:
        print('Processing Error')
if __name__ == "__main__":
    main()