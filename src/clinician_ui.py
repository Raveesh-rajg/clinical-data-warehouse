import tkinter as tk
from tkinter import messagebox, simpledialog
from src.utils import load_patients_data, load_notes_data, count_visits
from src.patient import Patient, Visit, Note  # moved to top for consistency


class ClinicianUI:
    def __init__(self, user):
        self.user = user
        self.patients, self.column_order = load_patients_data("data/Patient_data.csv")
        self.notes_dict = load_notes_data("data/Notes.csv")

        self.root = tk.Tk()
        self.root.title("Clinical Data Warehouse - Clinician Panel")
        self.root.geometry("480x500")
        self.root.configure(bg="#f4f8fb")
        self.root.resizable(False, False)

        tk.Label(self.root, text="Clinical Data Warehouse", font=("Helvetica", 16, "bold"), bg="#f4f8fb").pack(pady=(15, 0))
        tk.Label(self.root, text=f"Welcome, {user.username} (Clinician)", font=("Arial", 12), bg="#f4f8fb").pack(pady=(0, 20))

        actions = [
            ("Add Patient", self.add_patient),
            ("Remove Patient", self.remove_patient),
            ("Retrieve Patient", self.retrieve_patient),
            ("View Note", self.view_note),
            ("Count Visits", self.count_visits_gui),
            ("Save to File", self.save_to_file),
            ("Exit", self.root.quit)
        ]

        for text, command in actions:
            tk.Button(self.root, text=text, font=("Arial", 11),
                      width=24, height=2, bg="#007acc", fg="white",
                      command=command).pack(pady=6)

        self.result_label = tk.Label(self.root, text="", font=("Arial", 11), bg="#f4f8fb")
        self.result_label.pack(pady=15)

        self.root.mainloop()

    def count_visits_gui(self):
        date_input = simpledialog.askstring("Count Visits", "Enter date (YYYY-MM-DD):")
        if not date_input:
            return
        result = count_visits(self.patients, date_input)
        self.result_label.config(text=result)

    def add_patient(self):
        import uuid

        name = simpledialog.askstring("Add Patient", "Enter patient name:")
        if not name:
            return

        age_str = simpledialog.askstring("Add Patient", "Enter patient age:")
        if not age_str or not age_str.isdigit():
            messagebox.showerror("Invalid Input", "Age must be a number.")
            return
        age = int(age_str)

        gender = simpledialog.askstring("Add Patient", "Enter patient gender (M/F):")
        if gender not in ['M', 'F', 'm', 'f']:
            messagebox.showerror("Invalid Input", "Gender must be M or F.")
            return

        visit_id = str(uuid.uuid4())[:8].upper()
        patient_id = str(uuid.uuid4())[:8].upper()
        visit_time = simpledialog.askstring("Visit Time", "Enter visit date (e.g., 2020-04-10):")
        department = simpledialog.askstring("Department", "Enter department:")
        complaint = simpledialog.askstring("Complaint", "Enter chief complaint:")
        race = simpledialog.askstring("Race", "Enter race:")
        ethnicity = simpledialog.askstring("Ethnicity", "Enter ethnicity:")
        insurance = simpledialog.askstring("Insurance", "Enter insurance provider:")
        zip_code = simpledialog.askstring("ZIP Code", "Enter ZIP code:")

        visit = Visit(
            visit_id, visit_time, department, complaint,
            gender.upper(), race, age, ethnicity, insurance, zip_code
        )

        note_id = str(uuid.uuid4())[:6].upper()
        note = Note(note_id, "General", "Initial visit entry.")
        visit.note = note

        patient = Patient(patient_id)
        patient.add_visit(visit)
        self.patients[patient_id] = patient

        messagebox.showinfo("Success", f"Patient added:\nID: {patient_id}\nVisit ID: {visit_id}\nNote ID: {note_id}")

    def remove_patient(self):
        patient_id = simpledialog.askstring("Remove Patient", "Enter Patient ID to remove:")
        if not patient_id:
            return

        patient_id = patient_id.strip().upper()
        if patient_id not in self.patients:
            messagebox.showerror("Not Found", f"No patient found with ID: {patient_id}")
            return

        confirm = messagebox.askyesno("Confirm Deletion", f"Delete patient {patient_id}?")
        if confirm:
            del self.patients[patient_id]
            messagebox.showinfo("Removed", f"Patient {patient_id} removed.")

    def retrieve_patient(self):
        patient_id = simpledialog.askstring("Retrieve Patient", "Enter Patient ID:")
        if not patient_id:
            return

        patient = self.patients.get(patient_id.upper())
        if not patient:
            messagebox.showerror("Not Found", f"No patient found with ID: {patient_id}")
            return

        if not patient.visits:
            messagebox.showinfo("No Visits", f"Patient {patient_id} has no recorded visits.")
            return

        info_lines = [f"Patient ID: {patient_id}", f"Total Visits: {len(patient.visits)}", ""]
        for i, visit in enumerate(patient.visits, 1):
            info_lines.extend([
                f"Visit {i}:",
                f"  Visit ID: {visit.visit_id}",
                f"  Visit Time: {visit.visit_time}",
                f"  Department: {visit.department}",
                f"  Complaint: {visit.complaint}",
                f"  Gender: {visit.gender}",
                f"  Age: {visit.age}",
                f"  Race: {visit.race}",
                f"  Ethnicity: {visit.ethnicity}",
                f"  Insurance: {visit.insurance}",
                f"  ZIP Code: {visit.zip_code}",
                ""
            ])
        messagebox.showinfo("Patient Details", "\n".join(info_lines))

    def view_note(self):
        visit_id = simpledialog.askstring("View Note", "Enter Visit ID:")
        if not visit_id:
            return

        visit_id = visit_id.strip().upper()

        for patient in self.patients.values():
            for visit in patient.visits:
                if visit.visit_id.upper() == visit_id:
                    if visit.note and (visit.note.note_text or visit.note.note_id):
                        note = visit.note
                        messagebox.showinfo(
                            "Note Details",
                            f"Note ID: {note.note_id}\n"
                            f"Note Type: {note.note_type}\n"
                            f"Note Text:\n{note.note_text}"
                        )
                        return
                    else:
                        messagebox.showinfo("No Note", f"No note attached to visit {visit_id}")
                        return
        messagebox.showerror("Not Found", f"No visit found with ID: {visit_id}")

    def save_to_file(self):
        import csv
        try:
            with open("outputs/saved_patients.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([
                    "Patient_ID", "Visit_ID", "Visit_time", "Department", "Complaint",
                    "Gender", "Race", "Age", "Ethnicity", "Insurance", "Zip_code", "Note_ID"
                ])
                for patient_id, patient in self.patients.items():
                    for visit in patient.visits:
                        writer.writerow([
                            patient_id,
                            visit.visit_id,
                            visit.visit_time,
                            visit.department,
                            visit.complaint,
                            visit.gender,
                            visit.race,
                            visit.age,
                            visit.ethnicity,
                            visit.insurance,
                            visit.zip_code,
                            visit.note.note_id if visit.note else ""
                        ])
            messagebox.showinfo("Success", "Patient data saved to 'outputs/saved_patients.csv'.")
        except Exception as e:
            messagebox.showerror("Error", f"File save failed:\n{str(e)}")
