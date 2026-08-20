from RideBooking import RideBooking
from datetime import datetime


system = RideBooking()

normal_time = datetime(2026, 8, 20, 14, 0)

print("Test 1: Normal booking")

booking = system.make_booking(
    "C101",
    "VIT",
    "Katpadi",
    10,
    1,
    "Sedan",
    normal_time
)

assert booking["fare"] > 0
assert booking["driver"] is not None

print("PASS")


print("Test 2: Peak-hour booking")

peak_time = datetime(2026, 8, 20, 8, 0)

fare = system.calculate_fare(
    10,
    1,
    "Sedan",
    peak_time
)

normal_fare = system.calculate_fare(
    10,
    1,
    "Sedan",
    normal_time
)

assert fare > normal_fare

print("PASS")


print("Test 3: Night booking")

night_time = datetime(2026, 8, 20, 23, 0)

night_fare = system.calculate_fare(
    10,
    1,
    "Sedan",
    night_time
)

assert night_fare > normal_fare

print("PASS")


print("Test 4: Invalid distance")

try:
    system.calculate_fare(
        0,
        1,
        "Sedan",
        normal_time
    )

    assert False

except ValueError:
    assert True

print("PASS")


print("Test 5: Invalid passenger count")

try:
    system.calculate_fare(
        10,
        10,
        "Sedan",
        normal_time
    )

    assert False

except ValueError:
    assert True

print("PASS")


print("Test 6: Unavailable driver")

system.drivers["Bike"] = []

try:
    system.make_booking(
        "C102",
        "VIT",
        "Katpadi",
        5,
        1,
        "Bike",
        normal_time
    )

    assert False

except ValueError:
    assert True

print("PASS")


print("Test 7: Maximum discount")

fare = system.calculate_fare(
    10,
    1,
    "Sedan",
    normal_time,
    50
)

fare_30 = system.calculate_fare(
    10,
    1,
    "Sedan",
    normal_time,
    30
)

assert fare == fare_30

print("PASS")


print("Test 8: Multiple vehicle types")

bike = system.calculate_fare(
    10,
    1,
    "Bike",
    normal_time
)

suv = system.calculate_fare(
    10,
    2,
    "SUV",
    normal_time
)

premium = system.calculate_fare(
    10,
    2,
    "Premium",
    normal_time
)

assert bike > 0
assert suv > 0
assert premium > 0

print("PASS")


print("Test 9: Boundary fare values")

fare = system.calculate_fare(
    0.1,
    1,
    "Bike",
    normal_time
)

assert fare > 0

print("PASS")


print("Test 10: Driver allocation")

system.add_driver("Bike", "D999")

driver = system.assign_driver("Bike")

assert driver == "D999"

print("PASS")


print("All Ride Booking tests passed")
