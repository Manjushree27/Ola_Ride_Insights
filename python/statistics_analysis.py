import pandas as pd

try:
    from scipy import stats
except ImportError:
    stats = None

try:
    from .helper_functions import CLEANED_FILE
except ImportError:
    from helper_functions import CLEANED_FILE


def descriptive_statistics(df, column):
    values = df[column].dropna()
    return {
        "column": column,
        "count": int(values.count()),
        "mean": float(round(values.mean(), 2)),
        "median": float(round(values.median(), 2)),
        "mode": float(values.mode().iloc[0]) if not values.mode().empty else None,
        "range": float(round(values.max() - values.min(), 2)),
        "variance": float(round(values.var(), 2)),
        "standard_deviation": float(round(values.std(), 2)),
        "skewness": float(round(values.skew(), 2)),
        "kurtosis": float(round(values.kurtosis(), 2)),
    }


def run_statistics(path=CLEANED_FILE):
    df = pd.read_csv(path)
    numeric_columns = ["booking_value", "ride_distance", "v_tat", "c_tat", "driver_ratings", "customer_rating"]
    return [descriptive_statistics(df, column) for column in numeric_columns if column in df.columns]


def compare_successful_vs_cancelled_values(path=CLEANED_FILE):
    df = pd.read_csv(path)
    success = df.loc[df["booking_status"] == "Success", "booking_value"].dropna()
    failed = df.loc[df["booking_status"] != "Success", "booking_value"].dropna()
    if stats is None:
        return {
            "successful_avg_booking_value": float(round(success.mean(), 2)),
            "failed_avg_booking_value": float(round(failed.mean(), 2)),
            "t_statistic": None,
            "p_value": None,
            "interpretation": "Install SciPy to run the independent t-test. Descriptive comparison is still available.",
        }
    test = stats.ttest_ind(success, failed, equal_var=False)
    return {
        "successful_avg_booking_value": float(round(success.mean(), 2)),
        "failed_avg_booking_value": float(round(failed.mean(), 2)),
        "t_statistic": float(round(test.statistic, 4)),
        "p_value": float(round(test.pvalue, 4)),
        "interpretation": "Low p-value suggests booking value differs between successful and failed rides."
        if test.pvalue < 0.05
        else "No statistically significant booking value difference found at 5% significance.",
    }


if __name__ == "__main__":
    for row in run_statistics():
        print(row)
    print(compare_successful_vs_cancelled_values())
