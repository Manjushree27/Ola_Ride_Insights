from python.data_cleaning import save_cleaned_data
from python.statistics_analysis import run_statistics


def main():
    cleaned_path, report = save_cleaned_data()
    print(f"Cleaned dataset created: {cleaned_path}")
    print(f"Rows after cleaning: {report['rows_after_cleaning']}")
    print("Statistics summary:")
    for row in run_statistics(cleaned_path):
        print(row)


if __name__ == "__main__":
    main()

