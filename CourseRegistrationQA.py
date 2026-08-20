from CourseRegistration import CourseRegistration


system = CourseRegistration()


completed = [
    "Programming",
    "Data Structures",
    "Statistics",
    "Networking"
]


print("Test 1: Valid registration")

credits = system.register_student(
    "S101",
    "M.Tech",
    4,
    ["DBMS"],
    completed
)

assert credits == 4

print("PASS")


print("Test 2: Missing prerequisite")

try:

    system.register_student(
        "S102",
        "M.Tech",
        4,
        ["DBMS"],
        []
    )

    assert False

except ValueError:
    assert True

print("PASS")


print("Test 3: Credit limit violation")

try:

    system.register_student(
        "S103",
        "M.Tech",
        4,
        ["DBMS", "Cloud"],
        completed,
        max_credits=5
    )

    assert False

except ValueError:
    assert True

print("PASS")


print("Test 4: Timetable conflict")

try:

    system.register_student(
        "S104",
        "M.Tech",
        5,
        ["AI", "ML"],
        completed
    )

    assert False

except ValueError:
    assert True

print("PASS")


print("Test 5: Full course")

system.courses["DBMS"]["capacity"] = 1

try:

    system.register_student(
        "S105",
        "M.Tech",
        4,
        ["DBMS"],
        completed
    )

    assert False

except ValueError:
    assert True

print("PASS")


print("Test 6: Duplicate registration")

try:

    system.register_student(
        "S101",
        "M.Tech",
        4,
        ["DBMS"],
        completed
    )

    assert False

except ValueError:
    assert True

print("PASS")


print("Test 7: Invalid course")

try:

    system.register_student(
        "S106",
        "M.Tech",
        4,
        ["CyberSecurity"],
        completed
    )

    assert False

except ValueError:
    assert True

print("PASS")


print("Test 8: Semester restriction")

try:

    system.register_student(
        "S107",
        "M.Tech",
        3,
        ["DBMS"],
        completed
    )

    assert False

except ValueError:
    assert True

print("PASS")


print("Test 9: Boundary credit value")

system.courses["DBMS"]["capacity"] = 30

system.register_student(
    "S108",
    "M.Tech",
    4,
    ["DBMS"],
    completed,
    max_credits=4
)

assert system.get_registered_credits("S108") == 4

print("PASS")


print("Test 10: Total registered credits")

assert system.get_registered_credits("S101") == 4

print("PASS")


print("All Course Registration tests passed")
