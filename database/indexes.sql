USE ola_ride_insights;

CREATE INDEX idx_booking_date ON ola_bookings (booking_date);
CREATE INDEX idx_booking_status ON ola_bookings (booking_status);
CREATE INDEX idx_vehicle_type ON ola_bookings (vehicle_type);
CREATE INDEX idx_pickup_location ON ola_bookings (pickup_location);
CREATE INDEX idx_payment_method ON ola_bookings (payment_method);
CREATE INDEX idx_status_vehicle ON ola_bookings (booking_status, vehicle_type);

