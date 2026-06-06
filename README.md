# Ola Ride Insights: End-to-End Analytics Capstone

This project analyzes 103,024 Ola ride bookings from July 2024 to understand booking performance, revenue, cancellations, vehicle operations, payment behavior, and customer/driver ratings.

## Business Problem

Ola needs to understand why rides succeed or fail, which vehicle types generate stronger value, where demand is concentrated, and which cancellation patterns harm service reliability.

## Objectives

- Measure booking success, cancellation, and driver-not-found rates.
- Analyze revenue by vehicle type, payment method, and location.
- Identify pickup hotspots and operational risk areas.
- Study customer and driver ratings.
- Build SQL, Python, Power BI, and Streamlit deliverables for academic review.

## Dataset

Raw file: `data/raw/OLA_DataSet.xlsx`

Main sheet: `July`

Important columns:
- `Booking_ID`
- `Booking_Status`
- `Customer_ID`
- `Vehicle_Type`
- `Pickup_Location`
- `Drop_Location`
- `Booking_Value`
- `Payment_Method`
- `Ride_Distance`
- `Driver_Ratings`
- `Customer_Rating`
- Cancellation reason fields

## Project Structure

```text
Ola_Ride_Insights_Project/
├── data/
├── database/
├── notebooks/
├── python/
├── powerbi/
├── streamlit_app/
├── outputs/
├── requirements.txt
├── README.md
└── main.py
```

## How to Run

1. Install Python dependencies:

```bash
pip install -r requirements.txt
```

2. Clean and export the data:

```bash
python python/load_data.py
```

3. Run statistics:

```bash
python python/statistics_analysis.py
```

4. Start Streamlit:

```bash
streamlit run streamlit_app/app.py
```

5. For MySQL:
- Run `database/schema.sql`.
- Run `database/indexes.sql`.
- Clean data using Python.
- Update the CSV path in `database/data_import.sql`.
- Run `database/business_queries.sql`.

## Key KPIs

- Total bookings
- Successful bookings
- Success rate
- Cancellation rate
- Driver-not-found rate
- Total booking value
- Average booking value
- Average ride distance
- Average driver rating
- Average customer rating



