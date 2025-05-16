import tkinter as tk
from PIL import Image, ImageTk
from src.utils import load_patients_data, generate_statistics


class ManagementUI:
    def __init__(self, user):
        self.user = user
        self.root = tk.Tk()
        self.root.title("Clinical Data Warehouse - Management Dashboard")
        self.root.geometry("720x580")
        self.root.configure(bg="#f4f8fb")
        self.root.resizable(False, False)

        # Header
        tk.Label(self.root, text="Clinical Data Warehouse", font=("Helvetica", 16, "bold"), bg="#f4f8fb").pack(pady=(15, 0))
        tk.Label(self.root, text=f"Welcome, {user.username} (Management)", font=("Arial", 12), bg="#f4f8fb").pack(pady=(0, 20))

        # Load data and generate chart
        self.patients, _ = load_patients_data("data/Patient_data.csv")
        generate_statistics(self.patients)  # generates visits_by_year.png

        try:
            img = Image.open("outputs/visits_by_year.png")
            img = img.resize((640, 400), Image.Resampling.LANCZOS)
            self.photo = ImageTk.PhotoImage(img)

            img_label = tk.Label(self.root, image=self.photo, bg="#f4f8fb")
            img_label.pack(pady=10)
        except Exception as e:
            tk.Label(self.root, text=f"Error loading image: {e}", fg="red", bg="#f4f8fb").pack(pady=10)

        # Exit button
        tk.Button(self.root, text="Exit", width=15, height=2, bg="#007acc", fg="white", font=("Arial", 10),
                  command=self.root.quit).pack(pady=20)

        self.root.mainloop()
