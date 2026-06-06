# Viva Preparation

## SQL Questions

**Q1. Why did you create indexes?**  
Indexes improve filtering and grouping performance on frequently used columns such as booking date, booking status, vehicle type, pickup location, and payment method.

**Q2. Why is `booking_id` the primary key?**  
Each booking should be uniquely identifiable, so `booking_id` prevents duplicate ride records.

**Q3. What is the purpose of CTEs?**  
CTEs make complex SQL easier to read by breaking a query into named intermediate steps.

**Q4. Difference between `RANK` and `DENSE_RANK`?**  
`RANK` skips ranks after ties, while `DENSE_RANK` does not skip rank numbers.

## Python Questions

**Q1. Why did you clean the string value `null`?**  
The dataset stores missing values as text in some columns, so these values must be converted to real missing values.

**Q2. Why remove duplicate booking IDs?**  
Duplicate booking IDs can overstate bookings, revenue, and cancellation counts.

**Q3. Why are ratings set to null for unsuccessful rides?**  
Ratings logically apply only when a ride is completed successfully.

## Statistics Questions

**Q1. Why calculate mean and median?**  
Mean gives the average value, while median is more robust when extreme values exist.

**Q2. What does standard deviation show?**  
It shows how spread out values are around the mean.

**Q3. What does skewness show?**  
Skewness shows whether values are symmetrically distributed or pulled toward one side.

**Q4. What does kurtosis show?**  
Kurtosis indicates how heavy the tails of the distribution are compared with a normal distribution.

## Power BI Questions

**Q1. Why did you create multiple dashboard pages?**  
Separate pages make the dashboard easier to review by business theme: overview, revenue, customers, operations, ratings, cancellations, and executive summary.

**Q2. What slicers are useful?**  
Date, booking status, vehicle type, payment method, and pickup location are the most useful slicers.

## Streamlit Questions

**Q1. Why use Streamlit?**  
Streamlit allows a Python-based interactive dashboard without requiring web development frameworks.

**Q2. What does caching do?**  
Caching prevents repeated expensive data loading and cleaning when users interact with filters.

## Presentation Script

Good morning. My project is titled Ola Ride Insights. The objective is to analyze July ride booking data and identify patterns in booking success, cancellations, revenue, operations, and ratings. I used Python for data cleaning and statistics, MySQL for structured analytics, Power BI planning for business dashboard design, and Streamlit for an interactive dashboard. The main business value of this project is to help Ola understand where rides fail, which vehicle types perform well, and which operational areas need improvement.

