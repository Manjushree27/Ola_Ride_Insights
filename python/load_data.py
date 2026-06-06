try:
    from .data_cleaning import save_cleaned_data
except ImportError:
    from data_cleaning import save_cleaned_data


def main():
    output_path, report = save_cleaned_data()
    print("Ola data cleaning completed.")
    print(f"CSV export: {output_path}")
    print(f"Rows after cleaning: {report['rows_after_cleaning']}")
    print(f"Duplicates removed: {report['duplicates_removed']}")


if __name__ == "__main__":
    main()
