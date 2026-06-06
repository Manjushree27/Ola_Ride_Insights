from pathlib import Path
import sys

import pandas as pd
import plotly.express as px
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT / "python"))

from data_cleaning import clean_ola_data, load_raw_data


st.set_page_config(page_title="Ola Ride Insights", layout="wide")


@st.cache_data
def load_dashboard_data():
    df, _ = clean_ola_data(load_raw_data())
    df["ride_date"] = pd.to_datetime(df["booking_date"]).dt.date
    return df


df = load_dashboard_data()

st.title("Ola Ride Insights")

with st.sidebar:
    st.header("Filters")
    status = st.multiselect("Booking Status", sorted(df["booking_status"].dropna().unique()))
    vehicle = st.multiselect("Vehicle Type", sorted(df["vehicle_type"].dropna().unique()))
    payment = st.multiselect("Payment Method", sorted(df["payment_method"].dropna().unique()))
    date_range = st.date_input(
        "Ride Date Range",
        value=(df["ride_date"].min(), df["ride_date"].max()),
        min_value=df["ride_date"].min(),
        max_value=df["ride_date"].max(),
    )

filtered = df.copy()
if status:
    filtered = filtered[filtered["booking_status"].isin(status)]
if vehicle:
    filtered = filtered[filtered["vehicle_type"].isin(vehicle)]
if payment:
    filtered = filtered[filtered["payment_method"].isin(payment)]
if isinstance(date_range, tuple) and len(date_range) == 2:
    filtered = filtered[(filtered["ride_date"] >= date_range[0]) & (filtered["ride_date"] <= date_range[1])]

total_bookings = len(filtered)
successful = filtered[filtered["booking_status"] == "Success"]
success_rate = (len(successful) / total_bookings * 100) if total_bookings else 0
total_value = filtered["booking_value"].sum()
avg_distance = filtered["ride_distance"].mean()
avg_driver_rating = successful["driver_ratings"].mean()

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Bookings", f"{total_bookings:,}")
col2.metric("Success Rate", f"{success_rate:.1f}%")
col3.metric("Booking Value", f"Rs {total_value:,.0f}")
col4.metric("Avg Distance", f"{avg_distance:.1f} km")
col5.metric("Driver Rating", f"{avg_driver_rating:.2f}" if pd.notna(avg_driver_rating) else "N/A")

tab_overview, tab_revenue, tab_operations, tab_ratings, tab_cancellations = st.tabs(
    ["Overview", "Revenue", "Operations", "Ratings", "Cancellations"]
)

with tab_overview:
    left, right = st.columns(2)
    status_counts = filtered["booking_status"].value_counts().reset_index()
    status_counts.columns = ["booking_status", "bookings"]
    left.plotly_chart(
        px.bar(status_counts, x="bookings", y="booking_status", orientation="h", title="Booking Status Distribution"),
        use_container_width=True,
    )

    daily = filtered.groupby("ride_date", as_index=False).agg(bookings=("booking_id", "count"), value=("booking_value", "sum"))
    right.plotly_chart(px.line(daily, x="ride_date", y="bookings", title="Daily Booking Trend"), use_container_width=True)

with tab_revenue:
    vehicle_revenue = (
        successful.groupby("vehicle_type", as_index=False)
        .agg(revenue=("booking_value", "sum"), bookings=("booking_id", "count"), avg_fare=("booking_value", "mean"))
        .sort_values("revenue", ascending=False)
    )
    st.plotly_chart(px.bar(vehicle_revenue, x="vehicle_type", y="revenue", title="Revenue by Vehicle Type"), use_container_width=True)
    st.dataframe(vehicle_revenue, use_container_width=True)

with tab_operations:
    left, right = st.columns(2)
    top_pickups = filtered["pickup_location"].value_counts().head(15).reset_index()
    top_pickups.columns = ["pickup_location", "bookings"]
    left.plotly_chart(px.bar(top_pickups, x="bookings", y="pickup_location", orientation="h", title="Top Pickup Locations"), use_container_width=True)

    vehicle_ops = filtered.groupby("vehicle_type", as_index=False).agg(avg_distance=("ride_distance", "mean"), avg_v_tat=("v_tat", "mean"), avg_c_tat=("c_tat", "mean"))
    right.plotly_chart(px.scatter(vehicle_ops, x="avg_distance", y="avg_v_tat", size="avg_c_tat", color="vehicle_type", title="Distance vs Vehicle Turnaround Time"), use_container_width=True)

with tab_ratings:
    rating_summary = (
        successful.groupby("vehicle_type", as_index=False)
        .agg(driver_rating=("driver_ratings", "mean"), customer_rating=("customer_rating", "mean"), rides=("booking_id", "count"))
        .sort_values("driver_rating", ascending=False)
    )
    st.plotly_chart(px.bar(rating_summary, x="vehicle_type", y=["driver_rating", "customer_rating"], barmode="group", title="Average Ratings by Vehicle Type"), use_container_width=True)
    st.dataframe(rating_summary, use_container_width=True)

with tab_cancellations:
    left, right = st.columns(2)
    customer_cancel = filtered["canceled_rides_by_customer"].dropna().value_counts().head(10).reset_index()
    customer_cancel.columns = ["reason", "rides"]
    driver_cancel = filtered["canceled_rides_by_driver"].dropna().value_counts().head(10).reset_index()
    driver_cancel.columns = ["reason", "rides"]
    left.plotly_chart(px.bar(customer_cancel, x="rides", y="reason", orientation="h", title="Customer Cancellation Reasons"), use_container_width=True)
    right.plotly_chart(px.bar(driver_cancel, x="rides", y="reason", orientation="h", title="Driver Cancellation Reasons"), use_container_width=True)

