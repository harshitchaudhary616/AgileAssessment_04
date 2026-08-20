class ICUAllocation:

    def __init__(self, beds):

        if beds < 0:
            raise ValueError("Invalid bed count")

        self.total_beds = beds
        self.available_beds = beds

        self.patients = {}
        self.waiting_list = []
        self.allocations = {}

    def validate_patient(
        self,
        patient_id,
        age,
        oxygen,
        heart_rate,
        blood_pressure,
        temperature
    ):

        if patient_id in self.patients:
            raise ValueError("Duplicate patient ID")

        if age <= 0 or age > 120:
            raise ValueError("Invalid age")

        if oxygen < 0 or oxygen > 100:
            raise ValueError("Invalid oxygen level")

        if heart_rate <= 0 or heart_rate > 250:
            raise ValueError("Invalid heart rate")

        if temperature < 25 or temperature > 45:
            raise ValueError("Invalid temperature")

        if not isinstance(blood_pressure, str):
            raise ValueError("Invalid blood pressure")

    def calculate_priority(
        self,
        oxygen,
        heart_rate,
        blood_pressure,
        temperature,
        conditions
    ):

        score = 0

        systolic = int(blood_pressure.split("/")[0])

        if oxygen < 90:
            score += 40
        elif oxygen < 94:
            score += 25

        if heart_rate > 120 or heart_rate < 50:
            score += 25
        elif heart_rate > 100:
            score += 10

        if systolic < 90:
            score += 20
        elif systolic < 100:
            score += 10

        if temperature >= 39:
            score += 15
        elif temperature >= 38:
            score += 5

        score += len(conditions) * 5

        if score >= 60:
            priority = "CRITICAL"
        elif score >= 40:
            priority = "HIGH"
        elif score >= 20:
            priority = "MEDIUM"
        else:
            priority = "LOW"

        return score, priority

    def add_patient(
        self,
        patient_id,
        age,
        oxygen,
        heart_rate,
        blood_pressure,
        temperature,
        conditions,
        emergency=False
    ):

        self.validate_patient(
            patient_id,
            age,
            oxygen,
            heart_rate,
            blood_pressure,
            temperature
        )

        score, priority = self.calculate_priority(
            oxygen,
            heart_rate,
            blood_pressure,
            temperature,
            conditions
        )

        patient = {
            "age": age,
            "oxygen": oxygen,
            "heart_rate": heart_rate,
            "blood_pressure": blood_pressure,
            "temperature": temperature,
            "conditions": conditions,
            "score": score,
            "priority": priority,
            "emergency": emergency
        }

        self.patients[patient_id] = patient

        return priority

    def allocate_beds(self):

        unallocated = []

        patients = []

        for patient_id in self.patients:

            if patient_id not in self.allocations:
                patients.append(
                    (
                        patient_id,
                        self.patients[patient_id]
                    )
                )

        patients.sort(
            key=lambda x: (
                x[1]["emergency"],
                x[1]["score"]
            ),
            reverse=True
        )

        for patient_id, patient in patients:

            if self.available_beds > 0:

                self.allocations[patient_id] = "ICU-BED"

                self.available_beds -= 1

            else:

                if patient_id not in self.waiting_list:
                    self.waiting_list.append(patient_id)

                unallocated.append(patient_id)

        return unallocated

    def get_patient_priority(self, patient_id):

        if patient_id not in self.patients:
            raise ValueError("Patient not found")

        return self.patients[patient_id]["priority"]
