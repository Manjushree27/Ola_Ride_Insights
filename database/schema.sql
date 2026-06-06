CREATE DATABASE IF NOT EXISTS ola_ride_insights;
USE ola_ride_insights;

DROP TABLE IF EXISTS ola_bookings;

CREATE TABLE ola_bookings (
    booking_id VARCHAR(20) NOT NULL,
    booking_date DATETIME NOT NULL,
    booking_time TIME NULL,
    booking_status VARCHAR(30) NOT NULL,
    customer_id VARCHAR(20) NOT NULL,
    vehicle_type VARCHAR(30) NOT NULL,
    pickup_location VARCHAR(80) NOT NULL,
    drop_location VARCHAR(80) NOT NULL,
    v_tat INT NULL,
    c_tat INT NULL,
    canceled_rides_by_customer VARCHAR(120) NULL,
    canceled_rides_by_driver VARCHAR(120) NULL,
    incomplete_rides VARCHAR(10) NULL,
    incomplete_rides_reason VARCHAR(120) NULL,
    booking_value DECIMAL(10,2) NOT NULL,
    payment_method VARCHAR(30) NULL,
    ride_distance DECIMAL(8,2) NOT NULL,
    driver_ratings DECIMAL(3,2) NULL,
    customer_rating DECIMAL(3,2) NULL,
    vehicle_image_url VARCHAR(255) NULL,
    PRIMARY KEY (booking_id),
    CONSTRAINT chk_booking_value CHECK (booking_value >= 0),
    CONSTRAINT chk_ride_distance CHECK (ride_distance >= 0),
    CONSTRAINT chk_driver_rating CHECK (driver_ratings IS NULL OR driver_ratings BETWEEN 1 AND 5),
    CONSTRAINT chk_customer_rating CHECK (customer_rating IS NULL OR customer_rating BETWEEN 1 AND 5)
);

