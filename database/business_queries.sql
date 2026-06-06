USE ola_ride_insights;

-- 1. Overall booking performance
SELECT
    COUNT(*) AS total_bookings,
    SUM(booking_status = 'Success') AS successful_bookings,
    ROUND(100 * SUM(booking_status = 'Success') / COUNT(*), 2) AS success_rate_pct,
    ROUND(SUM(booking_value), 2) AS total_booking_value,
    ROUND(AVG(booking_value), 2) AS avg_booking_value
FROM ola_bookings;

-- 2. Booking status distribution
SELECT booking_status, COUNT(*) AS bookings
FROM ola_bookings
GROUP BY booking_status
ORDER BY bookings DESC;

-- 3. Revenue by vehicle type
SELECT
    vehicle_type,
    COUNT(*) AS bookings,
    ROUND(SUM(booking_value), 2) AS revenue,
    ROUND(AVG(booking_value), 2) AS avg_fare
FROM ola_bookings
WHERE booking_status = 'Success'
GROUP BY vehicle_type
ORDER BY revenue DESC;

-- 4. Cancellation reasons by customer
SELECT canceled_rides_by_customer AS cancellation_reason, COUNT(*) AS rides
FROM ola_bookings
WHERE booking_status = 'Canceled by Customer'
  AND canceled_rides_by_customer IS NOT NULL
GROUP BY canceled_rides_by_customer
ORDER BY rides DESC;

-- 5. Cancellation reasons by driver
SELECT canceled_rides_by_driver AS cancellation_reason, COUNT(*) AS rides
FROM ola_bookings
WHERE booking_status = 'Canceled by Driver'
  AND canceled_rides_by_driver IS NOT NULL
GROUP BY canceled_rides_by_driver
ORDER BY rides DESC;

-- 6. Pickup hotspots
SELECT pickup_location, COUNT(*) AS bookings, ROUND(SUM(booking_value), 2) AS booking_value
FROM ola_bookings
GROUP BY pickup_location
ORDER BY bookings DESC
LIMIT 10;

-- 7. Payment method performance
SELECT
    COALESCE(payment_method, 'Not Applicable') AS payment_method,
    COUNT(*) AS rides,
    ROUND(SUM(booking_value), 2) AS booking_value
FROM ola_bookings
GROUP BY COALESCE(payment_method, 'Not Applicable')
ORDER BY rides DESC;

-- 8. Vehicle types with high cancellation burden
SELECT
    vehicle_type,
    COUNT(*) AS total_bookings,
    SUM(booking_status <> 'Success') AS failed_bookings,
    ROUND(100 * SUM(booking_status <> 'Success') / COUNT(*), 2) AS failure_rate_pct
FROM ola_bookings
GROUP BY vehicle_type
HAVING failure_rate_pct > 30
ORDER BY failure_rate_pct DESC;

-- 9. Daily booking trend with previous-day comparison
WITH daily AS (
    SELECT
        DATE(booking_date) AS ride_date,
        COUNT(*) AS bookings,
        SUM(booking_status = 'Success') AS successful_bookings,
        SUM(booking_value) AS booking_value
    FROM ola_bookings
    GROUP BY DATE(booking_date)
)
SELECT
    ride_date,
    bookings,
    successful_bookings,
    ROUND(booking_value, 2) AS booking_value,
    bookings - LAG(bookings) OVER (ORDER BY ride_date) AS booking_change_vs_previous_day
FROM daily
ORDER BY ride_date;

-- 10. Rank pickup locations by successful revenue
WITH pickup_revenue AS (
    SELECT
        pickup_location,
        COUNT(*) AS successful_rides,
        SUM(booking_value) AS revenue
    FROM ola_bookings
    WHERE booking_status = 'Success'
    GROUP BY pickup_location
)
SELECT
    pickup_location,
    successful_rides,
    ROUND(revenue, 2) AS revenue,
    RANK() OVER (ORDER BY revenue DESC) AS revenue_rank,
    DENSE_RANK() OVER (ORDER BY successful_rides DESC) AS volume_rank
FROM pickup_revenue
ORDER BY revenue_rank
LIMIT 20;

-- 11. Longest rides per vehicle type
WITH ranked_rides AS (
    SELECT
        booking_id,
        vehicle_type,
        pickup_location,
        drop_location,
        ride_distance,
        booking_value,
        ROW_NUMBER() OVER (PARTITION BY vehicle_type ORDER BY ride_distance DESC, booking_value DESC) AS ride_rank
    FROM ola_bookings
    WHERE booking_status = 'Success'
)
SELECT *
FROM ranked_rides
WHERE ride_rank <= 5
ORDER BY vehicle_type, ride_rank;

-- 12. Rating performance by vehicle type
SELECT
    vehicle_type,
    COUNT(*) AS rated_rides,
    ROUND(AVG(driver_ratings), 2) AS avg_driver_rating,
    ROUND(AVG(customer_rating), 2) AS avg_customer_rating
FROM ola_bookings
WHERE booking_status = 'Success'
GROUP BY vehicle_type
ORDER BY avg_driver_rating DESC, avg_customer_rating DESC;

