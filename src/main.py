

import argparse
from src.user import authenticate_user
from src.utils import generate_statistics



def main():
    parser = argparse.ArgumentParser(description="Secure Hospital Management System")
    parser.add_argument("-username", type=str, required=True, help="Username for login")
    parser.add_argument("-password", type=str, required=True, help="Password for login")
    args = parser.parse_args()

    # Authenticate user and get role
    user = authenticate_user(args.username, args.password)
    if not user:
        print("Access Denied: Invalid credentials.")
        return

    launch_user_interface(user)


def launch_user_interface(user):
    from src.utils import load_patients_data


    print(f"\nWelcome, {user.username}! You are logged in as a {user.role}.")

    # Load patient and notes data
    patients, column_order = load_patients_data("../Data/Patient_data.csv")
    notes_dict = load_notes_data("../Data/Notes.csv")

    # Handle role-specific access
    if user.role == "management":
        generate_statistics(patients)

    elif user.role == "admin":
        # Launch Admin GUI
        from src.admin_ui import AdminUI
        AdminUI(user)

    elif user.role in ["nurse", "clinician"]:
        while True:
            print("\nAvailable actions: add_patient, remove_patient, retrieve_patient, view_note, count_visits, Exit")
            action = input("Enter action: ").lower()

            if action == "exit":
                print("Session ended.")
                break

            user.perform_action(action, patients, column_order, notes_dict)

    else:
        print("Error: Unauthorized role.")


if __name__ == "__main__":
    main()
