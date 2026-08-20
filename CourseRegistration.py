class CourseRegistration:

    def __init__(self):

        self.courses = {
            "DBMS": {
                "credits": 4,
                "prerequisite": "Programming",
                "capacity": 30,
                "semester": 4,
                "time": "10:00"
            },

            "AI": {
                "credits": 4,
                "prerequisite": "Data Structures",
                "capacity": 30,
                "semester": 5,
                "time": "11:00"
            },

            "ML": {
                "credits": 3,
                "prerequisite": "Statistics",
                "capacity": 25,
                "semester": 5,
                "time": "10:00"
            },

            "Cloud": {
                "credits": 3,
                "prerequisite": "Networking",
                "capacity": 25,
                "semester": 4,
                "time": "12:00"
            }
        }

        self.registrations = {}

    def register_student(
        self,
        student_id,
        program,
        semester,
        courses,
        completed_courses,
        max_credits=24
    ):

        if student_id not in self.registrations:
            self.registrations[student_id] = []

        selected = self.registrations[student_id]

        total_credits = 0

        for course in selected:
            total_credits += self.courses[course]["credits"]

        for course in courses:

            if course not in self.courses:
                raise ValueError("Invalid course")

            if course in selected:
                raise ValueError("Duplicate registration")

            course_data = self.courses[course]

            if course_data["semester"] != semester:
                raise ValueError("Semester restriction")

            prerequisite = course_data["prerequisite"]

            if prerequisite not in completed_courses:
                raise ValueError(
                    "Missing prerequisite for " + course
                )

            if total_credits + course_data["credits"] > max_credits:
                raise ValueError("Credit limit exceeded")

            if self._course_full(course):
                raise ValueError("Course capacity full")

            for registered_course in selected:

                if self.courses[registered_course]["time"] == course_data["time"]:
                    raise ValueError("Timetable clash")

            selected.append(course)

            total_credits += course_data["credits"]

        return total_credits

    def _course_full(self, course):

        count = 0

        for student in self.registrations:

            if course in self.registrations[student]:
                count += 1

        return count >= self.courses[course]["capacity"]

    def get_registered_credits(self, student_id):

        if student_id not in self.registrations:
            return 0

        total = 0

        for course in self.registrations[student_id]:
            total += self.courses[course]["credits"]

        return total

    def get_courses(self, student_id):

        if student_id not in self.registrations:
            return []

        return self.registrations[student_id]
