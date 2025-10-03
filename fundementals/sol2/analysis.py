"""KOSIS 일반가구원 통계 분석 및 시각화 스크립트."""

from pathlib import Path
from typing import Iterable, List

import matplotlib.pyplot as plt
import pandas as pd

CSV_FILE = Path('polulation.csv')
PLOT_FILE = Path('gender_age_trend.svg')
TARGET_REGION = '전국'
START_YEAR = 2015


def age_sort_key(label: str) -> tuple:
    """연령 구간을 연속적으로 정렬하기 위한 키를 계산한다."""
    if label == '합계':
        return (0, 0)
    if label == '15~64세':
        return (2, 1000)
    if label == '65세이상':
        return (2, 1001)

    digits = ''.join(ch for ch in label if ch.isdigit())

    if '미만' in label:
        number = int(digits) if digits else 0
        return (1, max(number - 1, 0))
    if '~' in label:
        start = label.split('~')[0]
        start_value = int(''.join(ch for ch in start if ch.isdigit()))
        return (1, start_value)
    if '이상' in label:
        number = int(digits) if digits else 0
        return (3, number)
    return (4, label)


def load_dataset(path: Path) -> pd.DataFrame:
    """CSV 파일을 읽어 필요한 컬럼만 남기고 필터링한다."""
    columns = ['행정구역별(시군구)', '시점', '성별', '연령별', '일반가구원']
    dataset = pd.read_csv(path, usecols=columns)
    dataset = dataset[dataset['행정구역별(시군구)'] == TARGET_REGION].copy()
    dataset['시점'] = pd.to_numeric(dataset['시점'], errors='coerce').astype('Int64')
    dataset = dataset.dropna(subset=['시점'])
    dataset = dataset[dataset['시점'] >= START_YEAR]
    dataset['일반가구원'] = pd.to_numeric(dataset['일반가구원'], errors='coerce')
    dataset = dataset.dropna(subset=['일반가구원'])
    return dataset.reset_index(drop=True)


def get_gender_year_summary(dataset: pd.DataFrame) -> pd.DataFrame:
    """연도별로 남자/여자의 일반가구원 수를 반환한다."""
    criteria = dataset['연령별'] == '합계'
    criteria &= dataset['성별'].isin(['남자', '여자'])
    filtered = dataset[criteria]
    pivot = filtered.pivot_table(
        index='시점',
        columns='성별',
        values='일반가구원',
        aggfunc='sum',
    )
    return pivot.sort_index()


def get_age_year_summary(dataset: pd.DataFrame) -> pd.DataFrame:
    """연령별(성별: 계) 일반가구원 수를 연도별로 정리한다."""
    filtered = dataset[dataset['성별'] == '계']
    pivot = filtered.pivot_table(
        index='시점',
        columns='연령별',
        values='일반가구원',
        aggfunc='sum',
    )
    ordered_columns = sorted(pivot.columns, key=age_sort_key)
    return pivot.loc[:, ordered_columns].sort_index()


def format_with_commas(table: pd.DataFrame) -> pd.DataFrame:
    """숫자를 천 단위 구분 기호와 함께 문자열로 변환한다."""
    def formatter(value: float) -> str:
        return f"{int(round(value)):,}"

    return table.apply(lambda column: column.map(formatter))


def get_ordered_age_labels(labels: Iterable[str]) -> List[str]:
    """연령 구간 라벨을 정렬 순서에 맞게 정리한다."""
    return sorted(labels, key=age_sort_key)


def to_ascii_age_label(label: str) -> str:
    """그래프에서 사용할 ASCII 기반 연령 구간 라벨을 생성한다."""
    digits = ''.join(ch for ch in label if ch.isdigit())
    if '미만' in label and digits:
        return f'Under {int(digits)}'
    if '~' in label:
        start, end = label.split('~')
        start_value = int(''.join(ch for ch in start if ch.isdigit()))
        end_value = int(''.join(ch for ch in end if ch.isdigit()))
        return f'{start_value}-{end_value}'
    if '이상' in label and digits:
        return f'{int(digits)}+'
    return label


def build_gender_age_plot(dataset: pd.DataFrame, output_path: Path) -> None:
    """남자/여자 연령별 일반가구원 평균을 꺾은선 그래프로 저장한다."""
    allowed_genders = ['남자', '여자']
    gender_labels = {'남자': 'Male', '여자': 'Female'}
    excluded_labels = {'합계', '15~64세', '65세이상'}

    subset = dataset[dataset['성별'].isin(allowed_genders)]
    subset = subset[~subset['연령별'].isin(excluded_labels)]

    grouped = subset.groupby(['성별', '연령별'])['일반가구원'].mean().reset_index()
    ordered_labels = get_ordered_age_labels(grouped['연령별'].unique())
    x_positions = list(range(len(ordered_labels)))
    tick_labels = [to_ascii_age_label(label) for label in ordered_labels]

    plt.figure(figsize=(12, 6))
    ax = plt.gca()

    for gender in allowed_genders:
        gender_data = grouped[grouped['성별'] == gender]
        gender_data = gender_data.set_index('연령별').reindex(ordered_labels)
        y_values = gender_data['일반가구원'].astype(float).tolist()
        ax.plot(x_positions, y_values, marker='o', label=gender_labels[gender])

    ax.set_title('Average general household members by age (2015 onward)')
    ax.set_xlabel('Age group')
    ax.set_ylabel('Average household members')
    ax.set_xticks(x_positions)
    ax.set_xticklabels(tick_labels, rotation=45, ha='right')
    ax.legend()
    ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)
    plt.tight_layout()
    plt.savefig(output_path, format='svg')
    plt.close()


def print_table_with_heading(heading: str, table: pd.DataFrame) -> None:
    """제목과 함께 표를 출력한다."""
    print(heading)
    print(table.to_string())
    print()


def describe_change(start_value: float, end_value: float) -> tuple:
    """변화량과 백분율을 계산한다."""
    absolute = end_value - start_value
    percent = (absolute / start_value * 100) if start_value else 0.0
    return absolute, percent


def create_trend_report(dataset: pd.DataFrame) -> List[str]:
    """연령별 및 성별 주요 변화를 요약한 문장을 생성한다."""
    start_year = int(dataset['시점'].min())
    end_year = int(dataset['시점'].max())
    report_lines: List[str] = []

    total_rows = dataset[(dataset['성별'] == '계') & (dataset['연령별'] == '합계')]
    total_start = float(total_rows[total_rows['시점'] == start_year]['일반가구원'].iloc[0])
    total_end = float(total_rows[total_rows['시점'] == end_year]['일반가구원'].iloc[0])
    total_change, total_pct = describe_change(total_start, total_end)
    direction = '증가' if total_change >= 0 else '감소'
    report_lines.append(
        f"{start_year}년 대비 {end_year}년 전체 일반가구원은 {direction} {abs(int(total_change)):,}명({total_pct:.2f}%)입니다."
    )

    senior_rows = dataset[(dataset['성별'] == '계') & (dataset['연령별'] == '65세이상')]
    senior_start = float(senior_rows[senior_rows['시점'] == start_year]['일반가구원'].iloc[0])
    senior_end = float(senior_rows[senior_rows['시점'] == end_year]['일반가구원'].iloc[0])
    senior_change, senior_pct = describe_change(senior_start, senior_end)
    direction = '증가' if senior_change >= 0 else '감소'
    report_lines.append(
        f"65세 이상 인구는 {direction} {abs(int(senior_change)):,}명({senior_pct:.2f}%)으로 고령층 비중이 두드러집니다."
    )

    age_rows = dataset[(dataset['성별'] == '계')]
    age_rows = age_rows[~age_rows['연령별'].isin(['합계', '15~64세', '65세이상'])]
    age_pivot = age_rows.pivot(index='연령별', columns='시점', values='일반가구원')
    start_series = age_pivot[start_year]
    end_series = age_pivot[end_year]
    change_series = end_series - start_series
    pct_series = (change_series / start_series.replace(0, pd.NA)) * 100

    top_increase = pct_series.sort_values(ascending=False).head(3)
    increase_parts = [
        f"{label}: {pct:.2f}%" for label, pct in top_increase.items() if pd.notna(pct)
    ]
    if increase_parts:
        report_lines.append(
            f"증가 폭이 큰 연령대 TOP3은 {', '.join(increase_parts)} 순입니다."
        )

    decrease_candidates = pct_series[pct_series < 0].sort_values().head(3)
    decrease_parts = [
        f"{label}: {pct:.2f}%" for label, pct in decrease_candidates.items()
    ]
    if decrease_parts:
        report_lines.append(
            f"감소 폭이 큰 연령대는 {', '.join(decrease_parts)}입니다."
        )
    else:
        report_lines.append('감소한 연령대는 확인되지 않았습니다.')

    gender_rows = dataset[(dataset['연령별'] == '합계') & (dataset['성별'].isin(['남자', '여자']))]
    gender_pivot = gender_rows.pivot(index='성별', columns='시점', values='일반가구원')
    male_change, male_pct = describe_change(
        float(gender_pivot.loc['남자', start_year]),
        float(gender_pivot.loc['남자', end_year]),
    )
    female_change, female_pct = describe_change(
        float(gender_pivot.loc['여자', start_year]),
        float(gender_pivot.loc['여자', end_year]),
    )
    report_lines.append(
        "성별 변화: 남자 {:+,.0f}명({:+.2f}%), 여자 {:+,.0f}명({:+.2f}%).".format(
            male_change, male_pct, female_change, female_pct
        )
    )

    return report_lines


def print_trend_report(lines: List[str]) -> None:
    """보너스 과제 리포트를 출력한다."""
    print('보너스 리포트: 연령별 인구 변화 트렌드')
    for line in lines:
        print(f'- {line}')
    print()


def main() -> None:
    dataset = load_dataset(CSV_FILE)

    gender_year_table = get_gender_year_summary(dataset)
    gender_year_table = format_with_commas(gender_year_table)
    print_table_with_heading(
        '2015년 이후 남자 및 여자의 연도별 일반가구원 수',
        gender_year_table,
    )

    age_year_table = get_age_year_summary(dataset)
    age_year_table = format_with_commas(age_year_table)
    print_table_with_heading(
        '2015년 이후 연령별 일반가구원 수 (성별: 계)',
        age_year_table,
    )

    build_gender_age_plot(dataset, PLOT_FILE)
    print(f'연령별 추세 그래프가 {PLOT_FILE} 파일로 저장되었습니다.')
    print()

    trend_lines = create_trend_report(dataset)
    print_trend_report(trend_lines)


if __name__ == '__main__':
    main()
