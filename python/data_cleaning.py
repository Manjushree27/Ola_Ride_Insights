import datetime as dt

import pandas as pd

try:
    from .helper_functions import CLEANED_FILE, RAW_FILE, ensure_output_dirs, normalize_text
except ImportError:
    from helper_functions import CLEANED_FILE, RAW_FILE, ensure_output_dirs, normalize_text


RENAME_MAP = {
    "Date": "booking_date",
    "Time": "booking_time",
    "Booking_ID": "booking_id",
    "Booking_Status": "booking_status",
    "Customer_ID": "customer_id",
    "Vehicle_Type": "vehicle_type",
    "Pickup_Location": "pickup_location",
    "Drop_Location": "drop_location",
    "V_TAT": "v_tat",
    "C_TAT": "c_tat",
    "Canceled_Rides_by_Customer": "canceled_rides_by_customer",
    "Canceled_Rides_by_Driver": "canceled_rides_by_driver",
    "Incomplete_Rides": "incomplete_rides",
    "Incomplete_Rides_Reason": "incomplete_rides_reason",
    "Booking_Value": "booking_value",
    "Payment_Method": "payment_method",
    "Ride_Distance": "ride_distance",
    "Driver_Ratings": "driver_ratings",
    "Customer_Rating": "customer_rating",
    "Vehicle Images": "vehicle_image_url",
}


def load_raw_data(path=RAW_FILE):
    df = pd.read_excel(path, sheet_name="July")
    unnamed_cols = [col for col in df.columns if str(col).startswith("Unnamed") or pd.isna(col)]
    df = df.drop(columns=unnamed_cols, errors="ignore")
    return df.rename(columns=RENAME_MAP)


def parse_time(value):
    if pd.isna(value):
        return None
    if isinstance(value, dt.time):
        return value
    text = str(value).strip()
    parsed = pd.to_datetime(text, format="%H:%M:%S", errors="coerce")
    return None if pd.isna(parsed) else parsed.time()


def clean_ola_data(df):
    df = df.copy()
    for column in df.select_dtypes(include="object").columns:
        df[column] = df[column].map(normalize_text)

    df["booking_date"] = pd.to_datetime(df["booking_date"], errors="coerce")
    df["booking_time"] = df["booking_time"].map(parse_time)

    numeric_columns = [
        "v_tat",
        "c_tat",
        "booking_value",
        "ride_distance",
        "driver_ratings",
        "customer_rating",
    ]
    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    before = len(df)
    df = df.drop_duplicates(subset=["booking_id"])
    duplicate_count = before - len(df)

    required_columns = [
        "booking_id",
        "booking_date",
        "booking_status",
        "customer_id",
        "vehicle_type",
        "pickup_location",
        "drop_location",
        "booking_value",
        "ride_distance",
    ]
    df = df.dropna(subset=required_columns)

    df = df[df["booking_value"].between(0, 10000)]
    df = df[df["ride_distance"].between(0, 100)]
    df.loc[df["booking_status"] != "Success", ["driver_ratings", "customer_rating", "payment_method"]] = None

    report = {
        "rows_after_cleaning": len(df),
        "duplicates_removed": duplicate_count,
        "missing_values": df.isna().sum().to_dict(),
        "booking_status_counts": df["booking_status"].value_counts().to_dict(),
    }
    return df, report


def save_cleaned_data():
    ensure_output_dirs()
    raw = load_raw_data()
    cleaned, report = clean_ola_data(raw)
    cleaned.to_csv(CLEANED_FILE, index=False)
    return CLEANED_FILE, report


if __name__ == "__main__":
    output_path, cleaning_report = save_cleaned_data()
    print(f"Cleaned data saved to: {output_path}")
    print(cleaning_report)
