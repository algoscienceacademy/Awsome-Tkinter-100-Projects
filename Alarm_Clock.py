import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import time
import threading
import os
from playsound import playsound # Install this via: pip install playsound

class AlarmClockApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Configure main window
        self.title("Colorful Alarm Clock")
        self.geometry("400x300")
        self.configure(bg="#34495e")

        # Current time display
        self.current_time_label = tk.Label(
            self, text="", font=("Helvetica", 32), fg="#ecf0f1", bg="#34495e"
        )
        self.current_time_label.pack(pady=20)
        
        # Alarm time input
        input_frame = tk.Frame(self, bg="#34495e")
        input_frame.pack(pady=10)
        
        tk.Label(input_frame, text="Hour", font=("Helvetica", 14), fg="#ecf0f1", bg="#34495e").grid(row=0, column=0, padx=5)
        tk.Label(input_frame, text="Minute", font=("Helvetica", 14), fg="#ecf0f1", bg="#34495e").grid(row=0, column=1, padx=5)
        
        self.hour_entry = tk.Entry(input_frame, width=4, font=("Helvetica", 18), justify="center")
        self.hour_entry.grid(row=1, column=0, padx=5)
        
        self.minute_entry = tk.Entry(input_frame, width=4, font=("Helvetica", 18), justify="center")
        self.minute_entry.grid(row=1, column=1, padx=5)
        
        # Set Alarm Button
        self.set_alarm_button = tk.Button(
            self, text="Set Alarm", font=("Helvetica", 14), bg="#27ae60", fg="white", command=self.set_alarm
        )
        self.set_alarm_button.pack(pady=20)

        # Alarm message
        self.alarm_message_label = tk.Label(self, text="", font=("Helvetica", 14), fg="#f39c12", bg="#34495e")
        self.alarm_message_label.pack(pady=10)

        # Start updating current time
        self.update_current_time()

    def update_current_time(self):
        """Updates the current time display every second."""
        current_time = datetime.now().strftime("%H:%M:%S")
        self.current_time_label.config(text=current_time)
        self.after(1000, self.update_current_time)

    def set_alarm(self):
        """Sets the alarm based on user input."""
        try:
            alarm_hour = int(self.hour_entry.get())
            alarm_minute = int(self.minute_entry.get())
            if 0 <= alarm_hour <= 23 and 0 <= alarm_minute <= 59:
                self.alarm_time = f"{alarm_hour:02}:{alarm_minute:02}:00"
                self.alarm_message_label.config(text=f"Alarm set for {self.alarm_time}")
                # Start the alarm thread
                threading.Thread(target=self.check_alarm).start()
            else:
                messagebox.showerror("Invalid Input", "Please enter a valid time (0-23 for hours, 0-59 for minutes).")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid time.")

    def check_alarm(self):
        """Checks if the current time matches the alarm time."""
        while True:
            current_time = datetime.now().strftime("%H:%M:%S")
            if current_time == self.alarm_time:
                self.trigger_alarm()
                break
            time.sleep(1)

    def trigger_alarm(self):
        """Triggers the alarm with a message and sound."""
        messagebox.showinfo("Alarm!", "Time's up!")
        # Play sound (Make sure alarm_sound.wav is in the same directory as the script)
        if os.path.exists("Blow.wav"):
            playsound("Blow.wav")
        else:
            print("Sound file not found.")

if __name__ == "__main__":
    app = AlarmClockApp()
    app.mainloop()
