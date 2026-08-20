from datetime import datetime


class RideBooking:

    def __init__(self):

        self.vehicle_capacity = {
            "Bike": 1,
            "Sedan": 4,
            "SUV": 6,
            "Premium": 4
        }

        self.base_fare = {
            "Bike": 30,
            "Sedan": 60,
            "SUV": 100,
            "Premium": 150
        }

        self.distance_rate = {
            "Bike": 8,
            "Sedan": 15,
            "SUV": 20,
            "Premium": 30
        }

        self.drivers = {
            "Bike": ["D101", "D102"],
            "Sedan": ["D201", "D202"],
            "SUV": ["D301"],
            "Premium": ["D401"]
        }

        self.bookings = []

    def calculate_fare(
        self,
        distance,
        passengers,
        vehicle_type,
        booking_time,
        promo_discount=0
    ):

        self.validate_booking(
            distance,
            passengers,
            vehicle_type,
            booking_time
        )

        fare = self.base_fare[vehicle_type]

        fare += distance * self.distance_rate[vehicle_type]

        hour = booking_time.hour

        if 7 <= hour <= 10 or 17 <= hour <= 20:
            fare += fare * 0.20

        if hour >= 22 or hour < 6:
            fare += fare * 0.15

        if passengers > 1:
            fare += (passengers - 1) * 20

        if promo_discount < 0:
            promo_discount = 0

        if promo_discount > 30:
            promo_discount = 30

        fare = fare - fare * promo_discount / 100

        return round(fare, 2)

    def validate_booking(
        self,
        distance,
        passengers,
        vehicle_type,
        booking_time
    ):

        if distance <= 0:
            raise ValueError("Invalid distance")

        if vehicle_type not in self.vehicle_capacity:
            raise ValueError("Invalid vehicle type")

        if passengers <= 0:
            raise ValueError("Invalid passenger count")

        if passengers > self.vehicle_capacity[vehicle_type]:
            raise ValueError("Excessive passengers")

        if not isinstance(booking_time, datetime):
            raise ValueError("Invalid booking time")

    def assign_driver(self, vehicle_type):

        if vehicle_type not in self.drivers:
            raise ValueError("Invalid vehicle type")

        if len(self.drivers[vehicle_type]) == 0:
            raise ValueError("No driver available")

        driver = self.drivers[vehicle_type].pop(0)

        return driver

    def make_booking(
        self,
        customer_id,
        pickup,
        drop,
        distance,
        passengers,
        vehicle_type,
        booking_time,
        promo_discount=0
    ):

        fare = self.calculate_fare(
            distance,
            passengers,
            vehicle_type,
            booking_time,
            promo_discount
        )

        driver = self.assign_driver(vehicle_type)

        booking = {
            "customer_id": customer_id,
            "pickup": pickup,
            "drop": drop,
            "distance": distance,
            "passengers": passengers,
            "vehicle": vehicle_type,
            "time": booking_time,
            "fare": fare,
            "driver": driver
        }

        self.bookings.append(booking)

        return booking

    def add_driver(self, vehicle_type, driver_id):

        if vehicle_type not in self.drivers:
            raise ValueError("Invalid vehicle type")

        self.drivers[vehicle_type].append(driver_id)

        return True
