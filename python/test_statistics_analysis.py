"""
Unit tests for python/statistics_analysis.py

descriptive_statistics() takes a DataFrame directly and is tested that way.
run_statistics() and compare_successful_vs_cancelled_values() both read
CLEANED_FILE from disk rather than accepting a DataFrame parameter, so
those are tested by writing a real temporary CSV and monkeypatching the
default path argument.
"""

import pandas as pd
import pytest

from python import statistics_analysis as sa


class TestDescriptiveStatistics:
    def test_returns_all_expected_keys(self):
        df = pd.DataFrame({"booking_value": [100, 200, 300, 400, 500]})
        result = sa.descriptive_statistics(df, "booking_value")
        expected_keys = {
            "column", "count", "mean", "median", "mode", "range",
            "variance", "standard_deviation", "skewness", "kurtosis",
        }
        assert set(result.keys()) == expected_keys

    def test_correct_mean_and_median_for_known_values(self):
        df = pd.DataFrame({"booking_value": [100, 200, 300, 400, 500]})
        result = sa.descriptive_statistics(df, "booking_value")
        assert result["mean"] == 300.0
        assert result["median"] == 300.0

    def test_correct_range_for_known_values(self):
        df = pd.DataFrame({"ride_distance": [5, 10, 15, 20]})
        result = sa.descriptive_statistics(df, "ride_distance")
        assert result["range"] == 15.0

    def test_drops_nulls_before_calculating(self):
        df = pd.DataFrame({"driver_ratings": [4.0, None, 5.0, None, 3.0]})
        result = sa.descriptive_statistics(df, "driver_ratings")
        assert result["count"] == 3

    def test_column_name_is_preserved_in_output(self):
        df = pd.DataFrame({"customer_rating": [4.5, 4.0, 3.5]})
        result = sa.descriptive_statistics(df, "customer_rating")
        assert result["column"] == "customer_rating"

    def test_values_are_rounded_to_two_decimal_places(self):
        df = pd.DataFrame({"booking_value": [100, 233, 367]})
        result = sa.descriptive_statistics(df, "booking_value")
        # mean = 700/3 = 233.333... -> rounded to 233.33
        assert result["mean"] == 233.33

    def test_mode_returns_most_frequent_value(self):
        df = pd.DataFrame({"v_tat": [10, 10, 10, 20, 30]})
        result = sa.descriptive_statistics(df, "v_tat")
        assert result["mode"] == 10.0

    def test_constant_column_has_zero_variance_and_std(self):
        df = pd.DataFrame({"c_tat": [5, 5, 5, 5]})
        result = sa.descriptive_statistics(df, "c_tat")
        assert result["variance"] == 0.0
        assert result["standard_deviation"] == 0.0

    def test_all_numeric_outputs_are_python_floats_or_none(self):
        df = pd.DataFrame({"booking_value": [100, 200, 300]})
        result = sa.descriptive_statistics(df, "booking_value")
        for key, value in result.items():
            if key in {"column", "count"}:
                continue
            assert value is None or isinstance(value, float)


class TestRunStatistics:
    def test_only_includes_columns_present_in_csv(self, tmp_path):
        # Only two of the six expected numeric columns are present.
        csv_path = tmp_path / "cleaned.csv"
        pd.DataFrame(
            {
                "booking_value": [100, 200, 300],
                "ride_distance": [5, 10, 15],
                "unrelated_column": ["a", "b", "c"],
            }
        ).to_csv(csv_path, index=False)

        results = sa.run_statistics(path=csv_path)
        columns_found = {row["column"] for row in results}
        assert columns_found == {"booking_value", "ride_distance"}

    def test_returns_list_of_dicts(self, tmp_path):
        csv_path = tmp_path / "cleaned.csv"
        pd.DataFrame({"booking_value": [100, 200, 300]}).to_csv(csv_path, index=False)
        results = sa.run_statistics(path=csv_path)
        assert isinstance(results, list)
        assert all(isinstance(row, dict) for row in results)

    def test_no_matching_columns_returns_empty_list(self, tmp_path):
        csv_path = tmp_path / "cleaned.csv"
        pd.DataFrame({"totally_unrelated": [1, 2, 3]}).to_csv(csv_path, index=False)
        results = sa.run_statistics(path=csv_path)
        assert results == []


class TestCompareSuccessfulVsCancelledValues:
    def test_returns_expected_keys(self, tmp_path):
        csv_path = tmp_path / "cleaned.csv"
        pd.DataFrame(
            {
                "booking_status": ["Success", "Success", "Canceled by Driver", "Canceled by Customer"],
                "booking_value": [200, 250, 100, 120],
            }
        ).to_csv(csv_path, index=False)

        result = sa.compare_successful_vs_cancelled_values(path=csv_path)
        expected_keys = {
            "successful_avg_booking_value", "failed_avg_booking_value",
            "t_statistic", "p_value", "interpretation",
        }
        assert set(result.keys()) == expected_keys

    def test_correct_average_for_successful_rides(self, tmp_path):
        csv_path = tmp_path / "cleaned.csv"
        pd.DataFrame(
            {
                "booking_status": ["Success", "Success", "Canceled by Driver"],
                "booking_value": [100, 200, 50],
            }
        ).to_csv(csv_path, index=False)

        result = sa.compare_successful_vs_cancelled_values(path=csv_path)
        assert result["successful_avg_booking_value"] == 150.0

    def test_correct_average_for_non_successful_rides(self, tmp_path):
        csv_path = tmp_path / "cleaned.csv"
        pd.DataFrame(
            {
                "booking_status": ["Success", "Canceled by Driver", "Canceled by Customer"],
                "booking_value": [100, 50, 70],
            }
        ).to_csv(csv_path, index=False)

        result = sa.compare_successful_vs_cancelled_values(path=csv_path)
        # "failed" is anything NOT equal to "Success" -> average of 50, 70 = 60
        assert result["failed_avg_booking_value"] == 60.0

    def test_t_test_runs_when_scipy_available(self, tmp_path):
        csv_path = tmp_path / "cleaned.csv"
        pd.DataFrame(
            {
                "booking_status": ["Success"] * 5 + ["Canceled by Driver"] * 5,
                "booking_value": [500, 520, 510, 505, 515, 50, 55, 60, 45, 52],
            }
        ).to_csv(csv_path, index=False)

        result = sa.compare_successful_vs_cancelled_values(path=csv_path)
        # With scipy installed, t_statistic and p_value should be real numbers.
        assert result["t_statistic"] is not None
        assert result["p_value"] is not None
        assert isinstance(result["t_statistic"], float)
        assert isinstance(result["p_value"], float)

    def test_interpretation_flags_significant_difference_for_clearly_separated_groups(self, tmp_path):
        csv_path = tmp_path / "cleaned.csv"
        pd.DataFrame(
            {
                "booking_status": ["Success"] * 10 + ["Canceled by Driver"] * 10,
                "booking_value": [500] * 10 + [50] * 10,
            }
        ).to_csv(csv_path, index=False)

        result = sa.compare_successful_vs_cancelled_values(path=csv_path)
        assert "differs" in result["interpretation"]

    def test_falls_back_to_descriptive_only_when_scipy_unavailable(self, tmp_path, monkeypatch):
        csv_path = tmp_path / "cleaned.csv"
        pd.DataFrame(
            {
                "booking_status": ["Success", "Success", "Canceled by Driver"],
                "booking_value": [100, 200, 50],
            }
        ).to_csv(csv_path, index=False)

        monkeypatch.setattr(sa, "stats", None)
        result = sa.compare_successful_vs_cancelled_values(path=csv_path)

        assert result["t_statistic"] is None
        assert result["p_value"] is None
        assert "Install SciPy" in result["interpretation"]
        # Descriptive averages should still be computed even without scipy.
        assert result["successful_avg_booking_value"] == 150.0
