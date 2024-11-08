import tkinter as tk
from datetime import datetime

class DigitalClock(tk.Tk):
    def __init__(self):
        super().__init__()

        # Window configuration
        self.title("Colorful Digital Clock")
        self.geometry("400x200")
        self.configure(bg="#2c3e50")

        # Clock Label
        self.time_label = tk.Label(
            self,
            font=("Helvetica", 48, "bold"),
            bg="#2c3e50",
            fg="#e74c3c"
        )
        self.time_label.pack(pady=30)

        # Day and Date Label
        self.date_label = tk.Label(
            self,
            font=("Helvetica", 20),
            bg="#2c3e50",
            fg="#ecf0f1"
        )
        self.date_label.pack(pady=5)

        # Start the clock
        self.update_clock()

    def update_clock(self):
        """Update the clock every second with the current time, date, and day."""
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S %p")
        current_date = now.strftime("%A, %B %d, %Y")

        # Set time and date to labels
        self.time_label.config(text=current_time)
        self.date_label.config(text=current_date)

        # Schedule the clock to update every 1000 milliseconds (1 second)
        self.after(1000, self.update_clock)

if __name__ == "__main__":
    clock = DigitalClock()
    clock.mainloop()
