from ICUAllocation import ICUAllocation


print("Test 1: Critical patient")

icu = ICUAllocation(3)

icu.add_patient(
    "P101",
    60,
    80,
    140,
    "80/60",
    39.5,
    ["Heart Disease"]
)

assert icu.get_patient_priority("P101") == "CRITICAL"

print("PASS")


print("Test 2: Normal patient")

icu.add_patient(
    "P102",
    30,
    98,
    75,
    "120/80",
    36.8,
    []
)

assert icu.get_patient_priority("P102") == "LOW"

print("PASS")


print("Test 3: Emergency case")

icu.add_patient(
    "P103",
    50,
    95,
    100,
    "110/70",
    37,
    [],
    emergency=True
)

icu.allocate_beds()

assert "P103" in icu.allocations

print("PASS")


print("Test 4: No ICU beds")

icu2 = ICUAllocation(1)

icu2.add_patient(
    "P201",
    60,
    80,
    140,
    "80/60",
    39.5,
    ["Heart Disease"]
)

icu2.add_patient(
    "P202",
    40,
    98,
    75,
    "120/80",
    36.8,
    []
)

icu2.allocate_beds()

assert len(icu2.waiting_list) == 1

print("PASS")


print("Test 5: Duplicate patient")

try:
    icu.add_patient(
        "P101",
        30,
        98,
        80,
        "120/80",
        37,
        []
    )

    assert False

except ValueError:
    assert True

print("PASS")


print("Test 6: Invalid oxygen")

try:
    icu.add_patient(
        "P104",
        30,
        150,
        80,
        "120/80",
        37,
        []
    )

    assert False

except ValueError:
    assert True

print("PASS")


print("Test 7: Invalid heart rate")

try:
    icu.add_patient(
        "P105",
        30,
        98,
        300,
        "120/80",
        37,
        []
    )

    assert False

except ValueError:
    assert True

print("PASS")


print("Test 8: Priority boundary")

score, priority = icu.calculate_priority(
    93,
    105,
    "100/70",
    38,
    []
)

assert priority in ["MEDIUM", "HIGH"]

print("PASS")


print("Test 9: Multiple patients competing for beds")

icu3 = ICUAllocation(2)

icu3.add_patient(
    "P301",
    60,
    80,
    140,
    "80/60",
    39.5,
    []
)

icu3.add_patient(
    "P302",
    50,
    85,
    130,
    "85/60",
    39,
    []
)

icu3.add_patient(
    "P303",
    30,
    98,
    70,
    "120/80",
    37,
    []
)

icu3.allocate_beds()

assert len(icu3.allocations) == 2
assert len(icu3.waiting_list) == 1

print("PASS")


print("All ICU tests passed")
