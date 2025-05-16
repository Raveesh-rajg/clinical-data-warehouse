# patient.py

class Note:
    def __init__(self, note_id="", note_type="", note_text=""):
        self.note_id = note_id
        self.note_type = note_type
        self.note_text = note_text

class Visit:
    def __init__(self, visit_id, visit_time, department, complaint, gender, race,
                 age, ethnicity, insurance, zip_code, note=None):
        self.visit_id = visit_id
        self.visit_time = visit_time
        self.department = department
        self.complaint = complaint
        self.gender = gender
        self.race = race
        self.age = int(age)
        self.ethnicity = ethnicity
        self.insurance = insurance
        self.zip_code = zip_code
        self.note = note if note else Note()

class Patient:
    def __init__(self, patient_id):
        self.patient_id = patient_id
        self.visits = []

    def add_visit(self, visit):
        self.visits.append(visit)

    def remove_all_visits(self):
        self.visits = []
