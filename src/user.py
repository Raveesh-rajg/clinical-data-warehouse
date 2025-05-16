import csv
from datetime import datetime
from src.utils import (
    add_patient,
    remove_patient,
    retrieve_patient,
    count_visits,
    view_note
)

class User:
    def __init__(self, username, role):
        self.username = username
        self.role = role

    def perform_action(self, action, patients, column_order, notes_dict):
        if self.role not in ["nurse", "clinician"]:
            print("Access Denied: You are not authorized to perform this action.")
            return

        if action == "add_patient":
            patient_id = input("Enter Patient ID: ")
            add_patient(patients, "data/Patient_data.csv", patient_id, column_order)
        elif action == "remove_patient":
            patient_id = input("Enter Patient ID: ")
            remove_patient(patients, "data/Patient_data.csv", patient_id, column_order)
        elif action == "retrieve_patient":
            patient_id = input("Enter Patient ID: ")
            output_file = input("Enter output CSV filename (e.g., my_export.csv): ")
            retrieve_patient(patients, patient_id, f"outputs/{output_file}", column_order)
        elif action == "count_visits":
            date = input("Enter date (YYYY-MM-DD): ")
            count_visits(patients, date)
        elif action == "view_note":
            date = input("Enter date (YYYY-MM-DD): ")
            view_note(patients, notes_dict, date)
        else:
            print("Invalid action.")

def authenticate_user(username, password, credentials_file="data/Credentials.csv"):
    try:
        with open(credentials_file, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row["username"] == username and row["password"] == password:
                    # Log successful login
                    with open("outputs/usage_log.csv", "a", encoding="utf-8") as log_file:
                        log_file.write(f"{username},{row['role']},{datetime.now()},SUCCESS\n")
                    return User(username, row["role"])
    except FileNotFoundError:
        print("[ERROR] Credentials file not found.")

    # Log failed login
    with open("outputs/usage_log.csv", "a", encoding="utf-8") as log_file:
        log_file.write(f"{username},unknown,{datetime.now()},FAILED LOGIN\n")

    return None
