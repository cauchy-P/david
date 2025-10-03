"""Analysis for the Kaggle Spaceship Titanic dataset using three CSV files."""
import locale
import os
from pathlib import Path
import sys
import warnings

LOCALE_ENV_VARS = (
    'LC_ALL',
    'LANG',
    'LC_CTYPE',
    'LC_NUMERIC',
    'LC_TIME',
    'LC_COLLATE',
    'LC_MONETARY',
    'LC_MESSAGES',
    'LC_PAPER',
    'LC_MEASUREMENT',
)


def configure_locale() -> None:
    """Set locale to a supported value to avoid GUI backend warnings."""
    preferred_values = [os.environ.get('LC_ALL'), os.environ.get('LANG'), '']
    for value in preferred_values:
        if value is None:
            continue
        try:
            locale.setlocale(locale.LC_ALL, value)
        except locale.Error:
            continue
        else:
            return

    for fallback in ('C.UTF-8', 'C'):
        try:
            locale.setlocale(locale.LC_ALL, fallback)
        except locale.Error:
            continue
        for variable in LOCALE_ENV_VARS:
            os.environ[variable] = fallback
        return


configure_locale()

warnings.filterwarnings(
    'ignore',
    message='The default of observed=False is deprecated',
    category=FutureWarning,
)

try:
    import matplotlib.pyplot as plt
except ModuleNotFoundError:
    plt = None

try:
    import pandas as pd
except ModuleNotFoundError as error:
    print('Pandas is required for this script. Install it before running the analysis.')
    raise SystemExit(1) from error

TRAIN_FILE = Path('train.csv')
TEST_FILE = Path('test.csv')
SUBMISSION_FILE = Path('sample_submission.csv')
MERGED_OUTPUT_FILE = Path('combined_passengers.csv')
AGE_GROUPS = ['10s', '20s', '30s', '40s', '50s', '60s', '70s']


def load_datasets() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load train, test, and submission datasets if all are present."""
    missing_files = [
        str(path)
        for path in (TRAIN_FILE, TEST_FILE, SUBMISSION_FILE)
        if not path.exists()
    ]
    if missing_files:
        print('Missing required files:')
        for filename in missing_files:
            print(f'  - {filename}')
        sys.exit(1)

    train_df = pd.read_csv(TRAIN_FILE)
    test_df = pd.read_csv(TEST_FILE)
    submission_df = pd.read_csv(SUBMISSION_FILE)
    return train_df, test_df, submission_df


def attach_submission_transport(test_df: pd.DataFrame, submission_df: pd.DataFrame) -> pd.DataFrame:
    """Attach Transported placeholder values from the sample submission to test data."""
    if 'PassengerId' not in test_df.columns:
        return test_df.copy()
    if 'PassengerId' not in submission_df.columns or 'Transported' not in submission_df.columns:
        return test_df.copy()

    merged = test_df.merge(
        submission_df[['PassengerId', 'Transported']],
        on='PassengerId',
        how='left',
        suffixes=('', '_submission'),
    )
    merged.rename(columns={'Transported': 'PredictedTransported'}, inplace=True)
    return merged


def combine_datasets(
    train_df: pd.DataFrame, test_df: pd.DataFrame
) -> pd.DataFrame:
    """Merge train and test datasets into a single DataFrame with source labels."""
    train_copy = train_df.copy()
    train_copy['Source'] = 'train'

    test_copy = test_df.copy()
    test_copy['Source'] = 'test'

    combined = pd.concat([train_copy, test_copy], ignore_index=True, sort=False)
    return combined


def save_combined_dataset(combined_df: pd.DataFrame) -> None:
    """Persist the merged train/test dataset to disk."""
    try:
        combined_df.to_csv(MERGED_OUTPUT_FILE, index=False)
        print(f'Saved merged dataset to {MERGED_OUTPUT_FILE}')
    except OSError as error:
        print(f'Could not save merged dataset: {error}')


def find_most_correlated_feature(train_df: pd.DataFrame) -> tuple[str, float]:
    """Find the feature most correlated with Transported in the train data."""
    if 'Transported' not in train_df.columns:
        return 'Transported column missing', 0.0

    numeric_df = train_df.select_dtypes(include=['number', 'bool']).copy()
    if numeric_df.empty:
        return 'No numeric features', 0.0

    numeric_df['Transported'] = train_df['Transported'].astype(int)
    correlation = (
        numeric_df.corr(numeric_only=True)['Transported']
        .drop(labels=['Transported'])
        .abs()
    )
    if correlation.empty:
        return 'No correlated features', 0.0

    best_feature = correlation.idxmax()
    return best_feature, float(correlation.loc[best_feature])


def add_age_group_column(df: pd.DataFrame) -> pd.DataFrame:
    """Return a filtered copy of df with an AgeGroup column for 10s-70s."""
    if 'Age' not in df.columns:
        return df.iloc[0:0].copy()

    copy = df[df['Age'].between(10, 79)].copy()
    if copy.empty:
        return copy

    copy['AgeGroup'] = copy['Age'].apply(lambda value: f'{int(value) // 10 * 10}s')
    copy = copy[copy['AgeGroup'].isin(AGE_GROUPS)]
    copy['AgeGroup'] = pd.Categorical(copy['AgeGroup'], categories=AGE_GROUPS, ordered=True)
    return copy


def plot_transport_by_age_group(train_df: pd.DataFrame) -> None:
    """Plot transported counts by age group for train data."""
    if plt is None:
        print('Matplotlib is not installed; skipping age group transport plot.')
        return
    if 'Transported' not in train_df.columns:
        return

    prepared = add_age_group_column(train_df)
    if prepared.empty:
        return

    prepared['Transported'] = prepared['Transported'].astype(bool)
    grouped = (
        prepared.groupby(['AgeGroup', 'Transported'], observed=False)
        .size()
        .unstack(fill_value=0)
    )

    ax = grouped.plot(kind='bar', figsize=(10, 6))
    ax.set_title('Transported counts by age group (train)')
    ax.set_xlabel('Age group')
    ax.set_ylabel('Passenger count')
    ax.legend(title='Transported', labels=['False', 'True'])
    plt.tight_layout()


def plot_age_distribution_by_destination(combined_df: pd.DataFrame) -> None:
    """Plot the passengers age-group distribution by destination across all data."""
    if plt is None:
        print('Matplotlib is not installed; skipping destination age distribution plot.')
        return
    if 'Destination' not in combined_df.columns:
        return

    prepared = add_age_group_column(combined_df)
    if prepared.empty:
        return

    grouped = (
        prepared.groupby(['Destination', 'AgeGroup'], observed=False)
        .size()
        .unstack(fill_value=0)
    )

    ax = grouped.T.plot(kind='bar', figsize=(12, 6))
    ax.set_title('Age group distribution by destination')
    ax.set_xlabel('Age group')
    ax.set_ylabel('Passenger count')
    ax.legend(title='Destination')
    plt.tight_layout()


def main() -> None:
    if plt is None:
        print('Matplotlib is required for plotting. Install it to see the graphs.')

    train_df, test_df, submission_df = load_datasets()
    test_with_submission = attach_submission_transport(test_df, submission_df)
    combined_df = combine_datasets(train_df, test_with_submission)
    save_combined_dataset(combined_df)

    total_rows = len(combined_df)
    print(f'Total merged rows: {total_rows}')

    best_feature, correlation = find_most_correlated_feature(train_df)
    print('Most correlated feature with Transported:')
    print(f'  Feature: {best_feature}')
    print(f'  Correlation: {correlation:.4f}')

    plot_transport_by_age_group(train_df)
    plot_age_distribution_by_destination(combined_df)

    if plt is not None:
        plt.show()


if __name__ == '__main__':
    main()
