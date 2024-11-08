import tkinter as tk
from tkinter import font, messagebox
import time

class CountdownTimerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Configure the main window
        self.title("Colorful Countdown Timer")
        self.geometry("400x350")
        self.configure(bg="#34495e")
        self.resizable(False, False)

        # Timer settings
        self.time_left = 0
        self.running = False

        # Display Label
        self.time_display = tk.Label(
            self, text="00:00", font=("Helvetica", 48), fg="#ecf0f1", bg="#34495e"
        )
        self.time_display.pack(pady=20)

        # Set Time Entry
        entry_frame = tk.Frame(self, bg="#34495e")
        entry_frame.pack(pady=10)

        self.hours_entry = tk.Entry(entry_frame, width=3, font=("Helvetica", 24), justify="center")
        self.hours_entry.insert(0, "00")
        self.hours_entry.grid(row=0, column=0, padx=5)

        self.minutes_entry = tk.Entry(entry_frame, width=3, font=("Helvetica", 24), justify="center")
        self.minutes_entry.insert(0, "00")
        self.minutes_entry.grid(row=0, column=1, padx=5)

        self.seconds_entry = tk.Entry(entry_frame, width=3, font=("Helvetica", 24), justify="center")
        self.seconds_entry.insert(0, "00")
        self.seconds_entry.grid(row=0, column=2, padx=5)

        # Buttons
        button_font = font.Font(size=14, weight="bold")
        button_frame = tk.Frame(self, bg="#34495e")
        button_frame.pack(pady=20)

        self.start_button = tk.Button(
            button_frame, text="Start", font=button_font, bg="#27ae60", fg="white", width=8,
            command=self.start
        )
        self.start_button.grid(row=0, column=0, padx=10)

        self.pause_button = tk.Button(
            button_frame, text="Pause", font=button_font, bg="#e74c3c", fg="white", width=8,
            command=self.pause, state="disabled"
        )
        self.pause_button.grid(row=0, column=1, padx=10)

        self.reset_button = tk.Button(
            button_frame, text="Reset", font=button_font, bg="#f39c12", fg="white", width=8,
            command=self.reset, state="disabled"
        )
        self.reset_button.grid(row=0, column=2, padx=10)

    def update_display(self):
        minutes, seconds = divmod(self.time_left, 60)
        hours, minutes = divmod(minutes, 60)
        self.time_display.config(text=f"{hours:02}:{minutes:02}:{seconds:02}")

    def countdown(self):
        if self.running and self.time_left > 0:
            self.time_left -= 1
            self.update_display()
            self.after(1000, self.countdown)
        elif self.time_left == 0:
            messagebox.showinfo("Time's up!", "The countdown has finished!")
            self.reset()

    def start(self):
        if not self.running:
            try:
                # Convert entered time to seconds
                hours = int(self.hours_entry.get())
                minutes = int(self.minutes_entry.get())
                seconds = int(self.seconds_entry.get())
                self.time_left = hours * 3600 + minutes * 60 + seconds

                if self.time_left <= 0:
                    raise ValueError("Time must be greater than 0")

                self.running = True
                self.start_button.config(state="disabled")
                self.pause_button.config(state="normal")
                self.reset_button.config(state="normal")
                self.countdown()
            except ValueError:
                messagebox.showerror("Invalid input", "Please enter valid numbers for hours, minutes, and seconds.")

    def pause(self):
        if self.running:
            self.running = False
            self.start_button.config(state="normal")
            self.pause_button.config(state="disabled")

    def reset(self):
        self.running = False
        self.time_left = 0
        self.update_display()
        self.start_button.config(state="normal")
        self.pause_button.config(state="disabled")
        self.reset_button.config(state="disabled")

if __name__ == "__main__":
    app = CountdownTimerApp()
    app.mainloop()
