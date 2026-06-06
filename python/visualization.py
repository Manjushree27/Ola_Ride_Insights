import matplotlib.pyplot as plt
import seaborn as sns


def plot_status_distribution(df):
    fig, ax = plt.subplots(figsize=(9, 5))
    sns.countplot(data=df, y="booking_status", order=df["booking_status"].value_counts().index, ax=ax)
    ax.set_title("Booking Status Distribution")
    ax.set_xlabel("Bookings")
    ax.set_ylabel("Status")
    return fig


def plot_revenue_by_vehicle(df):
    successful = df[df["booking_status"] == "Success"]
    revenue = successful.groupby("vehicle_type", as_index=False)["booking_value"].sum()
    revenue = revenue.sort_values("booking_value", ascending=False)
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=revenue, x="booking_value", y="vehicle_type", ax=ax)
    ax.set_title("Successful Booking Value by Vehicle Type")
    ax.set_xlabel("Booking Value")
    ax.set_ylabel("Vehicle Type")
    return fig

