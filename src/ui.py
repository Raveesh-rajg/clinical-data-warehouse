import tkinter as tk
from tkinter import messagebox
from src.user import authenticate_user
from src.clinician_ui import ClinicianUI
from src.admin_ui import AdminUI
from src.management_ui import ManagementUI


class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login - Clinical Data Warehouse")
        self.root.geometry("420x250")
        self.root.configure(bg="#e6f2ff")
        self.root.resizable(False, False)

        # Title
        tk.Label(root, text="Welcome to Clinical Data Warehouse",
                 font=("Helvetica", 16, "bold"), bg="#e6f2ff", fg="#003366").pack(pady=(20, 10))

        # Username
        tk.Label(root, text="Username:", font=("Arial", 12), bg="#e6f2ff").pack()
        self.username_entry = tk.Entry(root, font=("Arial", 12), width=30, bd=2, relief="groove")
        self.username_entry.pack(pady=(2, 10))

        # Password
        tk.Label(root, text="Password:", font=("Arial", 12), bg="#e6f2ff").pack()
        self.password_entry = tk.Entry(root, show="*", font=("Arial", 12), width=30, bd=2, relief="groove")
        self.password_entry.pack(pady=(2, 15))

        # Login Button
        login_button = tk.Button(root, text="Login", font=("Arial", 11, "bold"),
                                 bg="#007acc", fg="white", width=18, height=2,
                                 activebackground="#005f99", command=self.authenticate)
        login_button.pack()

    def authenticate(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        user = authenticate_user(username, password)

        if user:
            messagebox.showinfo("Login Successful", f"Welcome {username}! Role: {user.role}")
            self.root.destroy()  # Close login window

            # Launch GUI based on role
            if user.role in ["clinician", "nurse"]:
                ClinicianUI(user)
            elif user.role == "admin":
                AdminUI(user)
            elif user.role == "management":
                ManagementUI(user)
            else:
                messagebox.showerror("Access Denied", f"Unknown role: {user.role}")
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")
            log_failed_attempt(username)

def log_failed_attempt(username):
    from datetime import datetime
    with open("../outputs/usage_log.csv", "a", encoding='utf-8') as log_file:
        log_file.write(f"{username},unknown,{datetime.now()},FAILED LOGIN\n")

# Entry point to run login UI
def start_ui():
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()

if __name__ == "__main__":
    print("Starting the login window...")
    start_ui()
