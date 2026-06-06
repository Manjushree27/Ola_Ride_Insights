# Ola Ride Insights Project Report

## 1. Business Understanding

Ola operates in a high-frequency ride-hailing environment where booking reliability, customer experience, driver availability, pricing, and cancellations directly affect revenue and brand trust. This project analyzes July ride bookings to support operational and business decisions.

## 2. Problem Statement

The business needs a clear view of ride booking performance and failure reasons. A high number of cancellations or driver-not-found cases can reduce customer satisfaction, while poor visibility into location and vehicle-level trends can weaken operational planning.

## 3. Stakeholders

- Operations managers
- City managers
- Driver management team
- Customer experience team
- Revenue and finance team
- Business intelligence team

## 4. Dataset Understanding

The dataset contains ride-level Ola booking records. Each record describes the ride date/time, booking status, customer, vehicle type, pickup/drop locations, turnaround time, cancellation reasons, booking value, payment method, ride distance, and ratings.

Initial dataset profile:
- Total records: 103,024
- Successful bookings: 63,967
- Canceled by driver: 18,434
- Canceled by customer: 10,499
- Driver not found: 10,124
- Raw booking value total: about Rs 56.53M

## 5. KPIs

- Booking success rate = successful bookings / total bookings
- Cancellation rate = canceled bookings / total bookings
- Driver-not-found rate = driver-not-found bookings / total bookings
- Revenue by vehicle type = sum of booking value for successful rides
- Average booking value = booking value / bookings
- Average ride distance = total ride distance / bookings
- Average driver rating and customer rating

## 6. Methodology

1. Understand dataset and business meaning.
2. Clean missing, duplicate, invalid, and inconsistent values.
3. Create a MySQL database schema.
4. Build SQL analytics queries from beginner to advanced level.
5. Perform EDA and statistics in Python.
6. Design Power BI dashboard pages.
7. Build a Streamlit dashboard for interactive analysis.
8. Document insights and viva preparation material.

## 7. Expected Insights

- Which booking statuses dominate the business.
- Which vehicle types generate the highest value.
- Where pickup demand is concentrated.
- Which cancellation reasons are most common.
- Whether ratings differ by vehicle type.
- Which operational areas need intervention.

## 8. Business Recommendations

- Prioritize driver allocation in high-demand pickup zones.
- Investigate top driver cancellation reasons and introduce driver-side controls.
- Reduce customer cancellations caused by pickup delays.
- Monitor driver-not-found locations as supply shortage indicators.
- Use vehicle-level revenue and ratings to optimize fleet strategy.

