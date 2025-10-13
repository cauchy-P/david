# design_dome.py
import math

densities = {'유리': 2.4, '알루미늄': 2.7, '탄소강': 7.85}
def _read_positive_float(prompt: str, default: float | None = None) -> float:
    raw = input(prompt).strip()
    if raw == '':
        if default is None:
            raise ValueError
        value = default
    else:
        try:
            value = float(raw)
        except (TypeError, ValueError) as exc:
            raise ValueError from exc
    if not math.isfinite(value) or value <= 0:
        raise ValueError
    return value


def sphere_area(diameter: float, material: str, thickness: float = 1.0) -> tuple[float, float]:
    material = material.strip()
    if material not in densities or diameter <= 0 or thickness <= 0 or\
        not math.isfinite(diameter) or not math.isfinite(thickness):
        raise ValueError
    area = math.pi * (diameter ** 2)
    mass = densities[material] * area * 10000.0 * thickness / 1000.0
    return area, mass * 0.38


def main() -> None:
    try:
        diameter = _read_positive_float('지름(m)을 입력하세요:')
        material = input('재질(유리/알루미늄/탄소강)을 입력하세요:').strip()
        if material not in densities:
            raise ValueError
        thickness = _read_positive_float('두께(cm)를 입력하세요(기본값 1):', default=1.0)
        area, mars_weight = sphere_area(diameter, material, thickness)
        print(f'재질 : {material}, 지름 : {diameter:g}, 두께 : {thickness:g}, 면적 : {area:.3f}, 무게 : {mars_weight:.3f} kg')
    except ValueError:
        print('Invalid input.')
    except Exception:
        print('Processing error.')


if __name__ == '__main__':

    main()