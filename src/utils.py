import csv
import os
import random
import matplotlib.pyplot as plt
from datetime import datetime
from src.patient import Patient, Visit, Note

def load_patients_data(file_path="data/Patient_data.csv"):
    patients = {}
    if not os.path.exists(file_path):
        print("Error: Patient data file not found.")
        return patients, []

    with open(file_path, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        column_order = reader.fieldnames
        for row in reader:
            pid = row["Patient_ID"].strip().upper()
            if pid not in patients:
                patients[pid] = Patient(pid)

            note = Note(row.get("Note_ID", ""), row.get("Note_type", ""))
            visit = Visit(
                row["Visit_ID"], row["Visit_time"], row["Visit_department"],
                row["Chief_complaint"], row["Gender"], row["Race"], row["Age"],
                row["Ethnicity"], row["Insurance"], row["Zip_code"], note
            )
            patients[pid].add_visit(visit)
    return patients, column_order

def load_notes_data(file_path="data/Notes.csv"):
    notes_dict = {}
    with open(file_path, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            notes_dict[str(row["Note_ID"])] = row["Note_text"]
    return notes_dict

def add_patient(patients, file_path="data/Patient_data.csv", patient_id=None, column_order=None):
    patient_id = patient_id.strip().upper()
    new = False
    if patient_id not in patients:
        print("New patient. Collecting full data.")
        patients[patient_id] = Patient(patient_id)
        new = True
    else:
        print("Existing patient. Adding a new visit.")

    visit_id = random.randint(100000, 999999)
    visit_time = datetime.now().strftime("%Y-%m-%d")
    department = input("Department: ")
    complaint = input("Chief Complaint: ")
    gender = input("Gender: ")
    race = input("Race: ")
    age = input("Age: ")
    ethnicity = input("Ethnicity: ")
    insurance = input("Insurance: ")
    zip_code = input("Zip Code: ")

    note_id = str(random.randint(100000, 999999))
    note_type = input("Note Type (Oncology, Discharge, etc.): ")
    note = Note(note_id, note_type)

    visit = Visit(visit_id, visit_time, department, complaint, gender, race, age,
                  ethnicity, insurance, zip_code, note)
    patients[patient_id].add_visit(visit)

    with open(file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=column_order)
        writer.writeheader()
        for pid, patient in patients.items():
            for v in patient.visits:
                writer.writerow({
                    "Patient_ID": pid,
                    "Visit_ID": v.visit_id,
                    "Visit_time": v.visit_time,
                    "Visit_department": v.department,
                    "Race": v.race,
                    "Gender": v.gender,
                    "Ethnicity": v.ethnicity,
                    "Age": v.age,
                    "Zip_code": v.zip_code,
                    "Insurance": v.insurance,
                    "Chief_complaint": v.complaint,
                    "Note_ID": v.note.note_id,
                    "Note_type": v.note.note_type
                })
    print("Patient visit added successfully.")

def remove_patient(patients, file_path="data/Patient_data.csv", patient_id=None, column_order=None):
    patient_id = patient_id.strip().upper()
    if patient_id not in patients:
        print("Patient ID not found.")
        return
    del patients[patient_id]
    print(f"Patient {patient_id} removed.")

    with open(file_path, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=column_order)
        writer.writeheader()
        for pid, patient in patients.items():
            for v in patient.visits:
                writer.writerow({
                    "Patient_ID": pid,
                    "Visit_ID": v.visit_id,
                    "Visit_time": v.visit_time,
                    "Visit_department": v.department,
                    "Race": v.race,
                    "Gender": v.gender,
                    "Ethnicity": v.ethnicity,
                    "Age": v.age,
                    "Zip_code": v.zip_code,
                    "Insurance": v.insurance,
                    "Chief_complaint": v.complaint,
                    "Note_ID": v.note.note_id,
                    "Note_type": v.note.note_type
                })

def retrieve_patient(patients, patient_id, output_file, column_order):
    patient_id = patient_id.strip().upper()
    if patient_id not in patients:
        print("Patient ID not found.")
        return
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=column_order)
        writer.writeheader()
        for v in patients[patient_id].visits:
            writer.writerow({
                "Patient_ID": patient_id,
                "Visit_ID": v.visit_id,
                "Visit_time": v.visit_time,
                "Visit_department": v.department,
                "Race": v.race,
                "Gender": v.gender,
                "Ethnicity": v.ethnicity,
                "Age": v.age,
                "Zip_code": v.zip_code,
                "Insurance": v.insurance,
                "Chief_complaint": v.complaint,
                "Note_ID": v.note.note_id,
                "Note_type": v.note.note_type
            })
    print(f"Patient {patient_id}'s data saved to {output_file}.")

def count_visits(patients, input_date):
    def normalize_date(date_str):
        try_formats = [
            "%Y-%m-%d", "%Y/%m/%d", "%m/%d/%Y", "%Y.%m.%d", "%m-%d-%Y",
        ]
        for fmt in try_formats:
            try:
                return datetime.strptime(date_str.strip(), fmt).date()
            except ValueError:
                continue
        return None

    target_date = normalize_date(input_date)
    if not target_date:
        result = "Invalid input date. Please use a format like YYYY-MM-DD."
        print(result)
        return result

    count = 0
    for patient in patients.values():
        for visit in patient.visits:
            visit_date = normalize_date(visit.visit_time)
            if visit_date == target_date:
                count += 1

    result = f"Total visits on {target_date.isoformat()}: {count}"
    print(result)
    return result

def view_note(patients, notes_dict, date):
    try:
        target_date = datetime.strptime(date.strip(), "%Y-%m-%d").date()
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return

    print(f"Clinical notes for visits on {date}:")
    found = False
    for p in patients.values():
        for v in p.visits:
            visit_date = None
            for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%Y/%m/%d"):
                try:
                    visit_date = datetime.strptime(v.visit_time.strip(), fmt).date()
                    break
                except ValueError:
                    continue

            if visit_date == target_date:
                note_id = str(v.note.note_id)
                print(f"Note ID: {note_id} | Note Type: {v.note.note_type}")
                print(notes_dict.get(note_id, "Note text not available."))
                print("------------------------------------------------")
                found = True
    if not found:
        print("No notes found for this date.")

def generate_statistics(patients):
    print("\n-- Management Statistics --")

    visit_counts_by_year = {}
    for p in patients.values():
        for v in p.visits:
            year = v.visit_time.split("-")[0] if "-" in v.visit_time else v.visit_time.split("/")[2]
            visit_counts_by_year[year] = visit_counts_by_year.get(year, 0) + 1

    print("\nTotal Visits by Year:")
    for year in sorted(visit_counts_by_year):
        print(f"{year}: {visit_counts_by_year[year]} visits")

    years = sorted(visit_counts_by_year)
    counts = [visit_counts_by_year[y] for y in years]

    plt.figure(figsize=(10, 5))
    plt.bar(years, counts)
    plt.title("Total Visits by Year")
    plt.xlabel("Year")
    plt.ylabel("Number of Visits")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout(pad=2.0)
    plt.savefig("outputs/visits_by_year.png")
    print("Bar chart saved as 'outputs/visits_by_year.png'.")
