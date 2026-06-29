"""
Unit tests for python/visualization.py

These functions build matplotlib figures from a DataFrame. We can't
meaningfully assert on rendered pixel content, but we CAN verify that:
- the functions run without raising on realistic input
- they return an actual matplotlib Figure
- the figure has the expected title/axis labels (real, checkable behavior)
- edge cases like an empty or single-category DataFrame don't crash
"""

import matplotlib

matplotlib.use("Agg")  # headless backend, no display needed

import matplotlib.pyplot as plt
import pandas as pd
import pytest

from python import visualization as viz


@pytest.fixture(autouse=True)
def close_figures_after_each_test():
    yield
    plt.close("all")


class TestPlotStatusDistribution:
    def test_returns_a_matplotlib_figure(self):
        df = pd.DataFrame(
            {
                "booking_status": [
                    "Success", "Success", "Canceled by Driver",
                    "Canceled by Customer", "Success",
                ]
            }
        )
        fig = viz.plot_status_distribution(df)
        assert isinstance(fig, plt.Figure)

    def test_title_and_axis_labels_are_set_correctly(self):
        df = pd.DataFrame({"booking_status": ["Success", "Success"]})
        fig = viz.plot_status_distribution(df)
        ax = fig.axes[0]
        assert ax.get_title() == "Booking Status Distribution"
        assert ax.get_xlabel() == "Bookings"
        assert ax.get_ylabel() == "Status"

    def test_single_status_category_does_not_raise(self):
        df = pd.DataFrame({"booking_status": ["Success"] * 5})
        fig = viz.plot_status_distribution(df)
        assert isinstance(fig, plt.Figure)

    def test_handles_multiple_distinct_statuses(self):
        df = pd.DataFrame(
            {
                "booking_status": [
                    "Success", "Canceled by Driver", "Canceled by Customer",
                    "Driver Not Found", "Incomplete",
                ]
            }
        )
        fig = viz.plot_status_distribution(df)
        assert isinstance(fig, plt.Figure)


class TestPlotRevenueByVehicle:
    def test_returns_a_matplotlib_figure(self):
        df = pd.DataFrame(
            {
                "booking_status": ["Success", "Success", "Canceled by Driver"],
                "vehicle_type": ["Bike", "Prime Sedan", "Bike"],
                "booking_value": [100, 300, 50],
            }
        )
        fig = viz.plot_revenue_by_vehicle(df)
        assert isinstance(fig, plt.Figure)

    def test_only_successful_bookings_are_included_in_revenue(self):
        # If non-successful rows were mistakenly included, the Bike total
        # would be 100 (failed) + 200 (success) = 300 instead of just 200.
        df = pd.DataFrame(
            {
                "booking_status": ["Success", "Canceled by Driver"],
                "vehicle_type": ["Bike", "Bike"],
                "booking_value": [200, 100],
            }
        )
        fig = viz.plot_revenue_by_vehicle(df)
        ax = fig.axes[0]
        # The single bar's width should reflect only the successful 200,
        # not 300.
        bar_widths = [patch.get_width() for patch in ax.patches]
        assert bar_widths == [200.0]

    def test_title_and_axis_labels_are_set_correctly(self):
        df = pd.DataFrame(
            {
                "booking_status": ["Success"],
                "vehicle_type": ["Bike"],
                "booking_value": [150],
            }
        )
        fig = viz.plot_revenue_by_vehicle(df)
        ax = fig.axes[0]
        assert ax.get_title() == "Successful Booking Value by Vehicle Type"
        assert ax.get_xlabel() == "Booking Value"
        assert ax.get_ylabel() == "Vehicle Type"

    def test_no_successful_bookings_does_not_raise(self):
        df = pd.DataFrame(
            {
                "booking_status": ["Canceled by Driver", "Canceled by Customer"],
                "vehicle_type": ["Bike", "Auto"],
                "booking_value": [50, 60],
            }
        )
        # Should produce an empty chart, not crash.
        fig = viz.plot_revenue_by_vehicle(df)
        assert isinstance(fig, plt.Figure)

    def test_revenue_is_summed_not_averaged_across_same_vehicle_type(self):
        df = pd.DataFrame(
            {
                "booking_status": ["Success", "Success"],
                "vehicle_type": ["Auto", "Auto"],
                "booking_value": [100, 150],
            }
        )
        fig = viz.plot_revenue_by_vehicle(df)
        ax = fig.axes[0]
        bar_widths = [patch.get_width() for patch in ax.patches]
        assert bar_widths == [250.0]
