import csv
import tkinter as tk
from tkinter import messagebox

# File paths for the CSV files containing appointment and doctor data
appointment_file = "Data.csv"
doctor_file = "Doctors.csv"

class Data_Manager:
    """
    A class to manage reading and writing data to/from CSV files.
    This class provides static methods to handle doctor and appointment data.
    """
    
    @staticmethod
    def read_Doctors():
        """
        Reads doctor data from the CSV file and returns a list of dictionaries.
        Each dictionary contains details of a doctor including ID, Name, Specialty, Time, and Day.
        """
        with open(doctor_file, mode="r") as csvfile:
            reader = csv.reader(csvfile)
            return [{"ID": row[0], "Name": row[1], "Specialty": row[2], "time": row[3], "Day": row[4]} for row in reader if len(row) >= 5]
    
    @staticmethod
    def read_Appointments():
        """
        Reads appointment data from the CSV file and returns a list of dictionaries.
        Each dictionary contains details of an appointment.
        """
        with open(appointment_file, mode="r") as csvfile:
            reader = csv.DictReader(csvfile)
            return list(reader)
    
    @staticmethod
    def save_Appointment(patient_data):
        """
        Saves a new appointment to the CSV file.
        :param patient_data: A dictionary containing the patient's details and appointment information.
        """
        with open(appointment_file, mode="a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=patient_data.keys())
            writer.writerow(patient_data)
    
    @staticmethod
    def cancel_Appointment(telephone):
        """
        Cancels an appointment based on the patient's telephone number.
        :param telephone: The telephone number of the patient whose appointment is to be canceled.
        """
        lines = []
        with open(appointment_file, mode="r") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row and len(row) > 4 and row[4].lower() != telephone.lower():
                    lines.append(row)
        with open(appointment_file, mode="w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(lines)

class GUI:
    """
    A class to manage the graphical user interface (GUI) of the application.
    This class initializes the main window and provides methods to manage its contents.
    """
    
    def __init__(self, title, geometry):
        """
        Initializes the GUI window with a title and geometry.
        :param title: The title of the window.
        :param geometry: The size of the window in the format "widthxheight".
        """
        self.window = tk.Tk()
        self.window.title(title)
        self.window.geometry(geometry)
        self.window.resizable(False, False)
    
    def clear_window(self):
        """Clears all widgets from the window."""
        for widget in self.window.winfo_children():
            widget.destroy()

class Mainmenu:
    """
    A class to create and manage the main menu of the application.
    This class provides buttons to navigate to different functionalities like booking, viewing, and canceling appointments.
    """
    
    def __init__(self, uimanager):
        """
        Initializes the main menu.
        :param uimanager: An instance of the GUI class to manage the window.
        """
        self.uimanager = uimanager
        self.create_main_menu()
    
    def create_main_menu(self):
        """Creates the main menu with buttons for different actions."""
        self.uimanager.clear_window()
        tk.Button(self.uimanager.window, text="Book an Appointment", font=("Calibri", 18), command=self.book_appointment).pack(pady=20)
        tk.Button(self.uimanager.window, text="View Appointments", font=("Calibri", 18), command=self.view_appointments).pack(pady=20)
        tk.Button(self.uimanager.window, text="Cancel an Appointment", font=("Calibri", 18), command=self.cancel_appointment).pack(pady=20)
    
    def book_appointment(self):
        """Navigates to the book appointment interface."""
        self.uimanager.clear_window()
        BookAppointment(self.uimanager)
    
    def view_appointments(self):
        """Navigates to the view appointments interface."""
        self.uimanager.clear_window()
        ViewAppointments(self.uimanager, self)
    
    def cancel_appointment(self):
        """Navigates to the cancel appointment interface."""
        self.uimanager.clear_window()
        CancelAppointment(self.uimanager)

class BookAppointment:
    """
    A class to handle the booking of appointments.
    This class allows the user to select a specialty, day, and doctor, and then enter their details to book an appointment.
    """
    
    def __init__(self, uimanager):
        """
        Initializes the book appointment interface.
        :param uimanager: An instance of the GUI class to manage the window.
        """
        self.uimanager = uimanager
        self.doctors = Data_Manager.read_Doctors()
        self.selected_specialty = None
        self.display_specialties()
    
    def display_specialties(self):
        """Displays a list of specialties for the user to choose from."""
        specialties = sorted({doc["Specialty"] for doc in self.doctors})
        tk.Label(self.uimanager.window, text="Select a Specialty", font=("Arial", 16)).pack(pady=10)
        for specialty in specialties:
            tk.Button(self.uimanager.window, text=specialty, command=lambda sp=specialty: self.ask_for_day(sp)).pack(pady=5)
        tk.Button(self.uimanager.window, text="Go Back", command=self.go_back).pack()
    
    def ask_for_day(self, specialty):
        """
        Displays a list of available days for the selected specialty.
        :param specialty: The selected specialty.
        """
        self.selected_specialty = specialty
        self.uimanager.clear_window()
        tk.Label(self.uimanager.window, text="Select a Day of the Week", font=("Arial", 16)).pack(pady=10)
        days = sorted({doc["Day"] for doc in self.doctors if doc["Specialty"] == specialty})
        for day in days:
            tk.Button(self.uimanager.window, text=day, command=lambda d=day: self.display_doctors(specialty, d)).pack(pady=5)
        tk.Button(self.uimanager.window, text="Go Back", command=self.go_back).pack()
    
    def display_doctors(self, specialty, day):
        """
        Displays a list of available doctors for the selected specialty and day.
        :param specialty: The selected specialty.
        :param day: The selected day.
        """
        self.uimanager.clear_window()
        tk.Label(self.uimanager.window, text=f"Doctors Available for {specialty} on {day}", font=("Arial", 16)).pack(pady=10)
        for doctor in self.doctors:
            if doctor["Specialty"] == specialty and doctor["Day"] == day:
                info = f"{doctor['Name']} - {doctor['time']}"
                tk.Button(self.uimanager.window, text=info, command=lambda doc=doctor: self.enter_user_data(doc)).pack(pady=5)
        tk.Button(self.uimanager.window, text="Go Back", command=self.go_back).pack()
    
    def enter_user_data(self, doctor):
        """
        Navigates to the interface where the user can enter their details to book an appointment.
        :param doctor: The selected doctor.
        """
        self.uimanager.clear_window()
        EnterUserData(self.uimanager, doctor)
        tk.Button(self.uimanager.window, text="Go Back", command=self.go_back).pack()
    
    def go_back(self):
        """Returns to the main menu."""
        Mainmenu(uimanager).create_main_menu()

class EnterUserData:
    """
    A class to handle the input of user data for booking an appointment.
    This class provides a form for the user to enter their details and then saves the appointment.
    """
    
    def __init__(self, uimanager, doctor):
        """
        Initializes the user data entry form.
        :param uimanager: An instance of the GUI class to manage the window.
        :param doctor: The selected doctor for the appointment.
        """
        self.uimanager = uimanager
        self.doctor = doctor
        self.create_form()
    
    def create_form(self):
        """Creates a form for the user to enter their details."""
        tk.Label(self.uimanager.window, text="Enter Your Details", font=("Arial", 16)).pack(pady=10)
        tk.Label(self.uimanager.window, text="Name:").pack()
        self.name_entry = tk.Entry(self.uimanager.window)
        self.name_entry.pack()
        tk.Label(self.uimanager.window, text="Age:").pack()
        self.age_entry = tk.Entry(self.uimanager.window)
        self.age_entry.pack()
        tk.Label(self.uimanager.window, text="Email:").pack()
        self.email_entry = tk.Entry(self.uimanager.window)
        self.email_entry.pack()
        tk.Label(self.uimanager.window, text="Sex:").pack()
        self.sex_entry = tk.Entry(self.uimanager.window)
        self.sex_entry.pack()
        tk.Label(self.uimanager.window, text="Telephone:").pack()
        self.telephone_entry = tk.Entry(self.uimanager.window)
        self.telephone_entry.pack()
        tk.Button(self.uimanager.window, text="Submit", command=self.save_data).pack(pady=10)
    
    def save_data(self):
        """Saves the entered user data and books the appointment."""
        name = self.name_entry.get()
        age = self.age_entry.get()
        email = self.email_entry.get()
        sex = self.sex_entry.get()
        telephone = self.telephone_entry.get()
        if not name or not age or not email:
            messagebox.showwarning("Input Error", "All fields are required!")
            return

        # Check for existing appointment
        appointments = Data_Manager.read_Appointments()
        for row in appointments:
            if (row["Doctor ID"] == str(self.doctor["ID"]) and
                row["Doctor_Time"] == self.doctor["time"] and
                row["Day"] == self.doctor["Day"]):
                messagebox.showwarning("Booking Error", f"An appointment is already booked with Dr. {self.doctor['Name']} at {self.doctor['time']} on {self.doctor['Day']}.")
                return

        patient_data = {
            "name": name,
            "age": age,
            "E-mail": email,
            "Sex: M/F": sex,
            "Telephone": telephone,
            "Doctor ID": self.doctor["ID"],
            "Doctor_Name": self.doctor["Name"],
            "Doctor_Specialty": self.doctor["Specialty"],
            "Doctor_Time": self.doctor["time"],
            "Day": self.doctor["Day"]
        }
        Data_Manager.save_Appointment(patient_data)
        messagebox.showinfo("Success", "Appointment booked successfully!")
        self.uimanager.window.destroy()

class ViewAppointments:
    """
    A class to handle viewing existing appointments.
    This class allows the user to view their appointments by entering their name and telephone number.
    """
    
    def __init__(self, uimanager, main_menu):
        """
        Initializes the view appointments interface.
        :param uimanager: An instance of the GUI class to manage the window.
        :param main_menu: An instance of the Mainmenu class to return to the main menu.
        """
        self.uimanager = uimanager
        self.main_menu = main_menu
        self.create_form()
    
    def create_form(self):
        """Creates a form for the user to enter their details to view appointments."""
        tk.Label(self.uimanager.window, text="Enter Your Name", font=("Arial", 9)).pack()
        self.name_entry = tk.Entry(self.uimanager.window)
        self.name_entry.pack()
        tk.Label(self.uimanager.window, text="Enter Your Telephone", font=("Arial", 9)).pack()
        self.telephone_entry = tk.Entry(self.uimanager.window)
        self.telephone_entry.pack()
        tk.Button(self.uimanager.window, text="Check Appointments", command=self.check_appointments).pack(pady=10)
        tk.Button(self.uimanager.window, text="Go Back", command=self.go_back).pack()
    
    def check_appointments(self):
        """Checks and displays the appointments for the entered name and telephone number."""
        name = self.name_entry.get().strip()
        telephone = self.telephone_entry.get().strip()
        if not name:
            messagebox.showwarning("Input Error", "Name is required!")
            return

        appointments = Data_Manager.read_Appointments()
        filtered_appointments = [row for row in appointments if row["Telephone"].lower() == telephone.lower()]
        if filtered_appointments:
            appointment_info = "\n".join([f"Patient: {row['Name']}, Doctor: {row['Doctor_Name']}, Specialty: {row['Specialty']}, Time: {row['Doctor_Time']}, Day: {row['Day']}" for row in filtered_appointments])
            tk.Label(self.uimanager.window, text=f"Appointments for {name}:\n\n{appointment_info}", font=("Arial", 9), justify="left").pack()
        else:
            messagebox.showinfo("No Appointments", "No appointments found for this name.")
    
    def go_back(self):
        """Returns to the main menu."""
        self.main_menu.create_main_menu()

class CancelAppointment:
    """
    A class to handle the cancellation of appointments.
    This class allows the user to cancel their appointments by entering their name, age, and telephone number.
    """
    
    def __init__(self, uimanager):
        """
        Initializes the cancel appointment interface.
        :param uimanager: An instance of the GUI class to manage the window.
        """
        self.uimanager = uimanager
        self.create_form()
    
    def create_form(self):
        """Creates a form for the user to enter their details to cancel appointments."""
        tk.Label(self.uimanager.window, text="Enter Your Name", font=("Arial", 9)).pack()
        self.name_entry = tk.Entry(self.uimanager.window)
        self.name_entry.pack()
        tk.Label(self.uimanager.window, text="Enter Your Age", font=("Arial", 9)).pack()
        self.age_entry = tk.Entry(self.uimanager.window)
        self.age_entry.pack()
        tk.Label(self.uimanager.window, text="Enter Your Telephone", font=("Arial", 9)).pack()
        self.telephone_entry = tk.Entry(self.uimanager.window)
        self.telephone_entry.pack()
        tk.Button(self.uimanager.window, text="Cancel Appointments", command=self.cancel_appointments).pack(pady=10)
        tk.Button(self.uimanager.window, text="Go Back", command=self.go_back).pack()
    
    def cancel_appointments(self):
        """Cancels the appointments for the entered details."""
        name = self.name_entry.get().strip()
        age = self.age_entry.get().strip()
        telephone = self.telephone_entry.get().strip()
        if not name or not age or not telephone:
            messagebox.showwarning("Input Error", "All fields are required!")
            return

        Data_Manager.cancel_Appointment(telephone)
        messagebox.showinfo("Success", "Appointments canceled successfully!")
    
    def go_back(self):
        """Returns to the main menu."""
        Mainmenu(uimanager).create_main_menu()

# Initialize the GUI and start the main loop
uimanager = GUI("Doctor Appointment Scheduler", "600x400")
mainmenu = Mainmenu(uimanager)
uimanager.window.mainloop()