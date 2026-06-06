USE ola_ride_insights;

-- Recommended workflow:
-- 1. Run python/load_data.py to clean the Excel workbook and create data/cleaned/ola_bookings_cleaned.csv.
-- 2. Enable local file loading in MySQL if needed:
--    SET GLOBAL local_infile = 1;
-- 3. Update the file path below to your local absolute CSV path.

LOAD DATA LOCAL INFILE 'C:/path/to/Ola_Ride_Insights_Project/data/cleaned/ola_bookings_cleaned.csv'
INTO TABLE ola_bookings
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(booking_id, booking_date, booking_time, booking_status, customer_id, vehicle_type,
 pickup_location, drop_location, v_tat, c_tat, canceled_rides_by_customer,
 canceled_rides_by_driver, incomplete_rides, incomplete_rides_reason, booking_value,
 payment_method, ride_distance, driver_ratings, customer_rating, vehicle_image_url);

