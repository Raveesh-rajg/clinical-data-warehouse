import tkinter as tk
from tkinter import messagebox
from src.utils import load_patients_data, count_visits

class AdminUI:
    def __init__(self, user):
        self.user = user
        self.patients, _ = load_patients_data("data/Patient_data.csv")

        self.root = tk.Tk()
        self.root.title("Clinical Data Warehouse - Admin Panel")
        self.root.geometry("420x300")
        self.root.configure(bg="#f0f4f8")
        self.root.resizable(False, False)

        # Header
        tk.Label(self.root, text="Clinical Data Warehouse", font=("Helvetica", 16, "bold"), bg="#f0f4f8").pack(pady=10)
        tk.Label(self.root, text=f"Welcome, {user.username} (Admin)", font=("Arial", 12), bg="#f0f4f8").pack()

        # Instruction
        tk.Label(self.root, text="Enter a date to count visits (YYYY-MM-DD):", font=("Arial", 11), bg="#f0f4f8").pack(pady=(15, 0))

        # Entry box
        self.date_entry = tk.Entry(self.root, font=("Arial", 12), width=25)
        self.date_entry.pack(pady=5)

        # Count Button
        count_button = tk.Button(
            self.root, text="Count Visits", font=("Arial", 11, "bold"),
            bg="#007acc", fg="white", width=20, command=self.count_visits_gui
        )
        count_button.pack(pady=10)

        # Result Label
        self.result_label = tk.Label(self.root, text="", font=("Arial", 12), bg="#f0f4f8", fg="black")
        self.result_label.pack(pady=10)

        # Exit Button
        exit_button = tk.Button(
            self.root, text="Exit", font=("Arial", 11, "bold"),
            bg="#d9534f", fg="white", width=20, height=2, command=self.root.quit
        )
        exit_button.pack(pady=10)

        self.root.mainloop()

    def count_visits_gui(self):
        date_input = self.date_entry.get().strip()
        if not date_input:
            messagebox.showwarning("Input Required", "Please enter a date in YYYY-MM-DD format.")
            return

        result = count_visits(self.patients, date_input)
        if result.lower().startswith("invalid"):
            messagebox.showerror("Invalid Date", result)
        else:
            self.result_label.config(text=result)
