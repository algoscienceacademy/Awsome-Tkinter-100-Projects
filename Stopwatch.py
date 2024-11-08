import tkinter as tk
from tkinter import font

class StopwatchApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Main window configuration
        self.title("Colorful Stopwatch")
        self.geometry("400x300")
        self.configure(bg="#2c3e50")
        self.resizable(False, False)

        # Stopwatch state
        self.running = False
        self.time_elapsed = 0  # time in seconds

        # Display label
        self.time_display = tk.Label(
            self, text="00:00:00", font=("Helvetica", 48), fg="#ecf0f1", bg="#2c3e50"
        )
        self.time_display.pack(pady=40)

        # Control buttons
        button_font = font.Font(size=16, weight="bold")
        button_frame = tk.Frame(self, bg="#2c3e50")
        button_frame.pack()

        self.start_button = tk.Button(
            button_frame, text="Start", font=button_font, bg="#27ae60", fg="white", width=8,
            command=self.start
        )
        self.start_button.grid(row=0, column=0, padx=10, pady=10)

        self.stop_button = tk.Button(
            button_frame, text="Stop", font=button_font, bg="#e74c3c", fg="white", width=8,
            command=self.stop, state="disabled"
        )
        self.stop_button.grid(row=0, column=1, padx=10, pady=10)

        self.reset_button = tk.Button(
            button_frame, text="Reset", font=button_font, bg="#f39c12", fg="white", width=8,
            command=self.reset, state="disabled"
        )
        self.reset_button.grid(row=0, column=2, padx=10, pady=10)

    def update_time(self):
        if self.running:
            self.time_elapsed += 1
            # Calculate minutes, seconds, and centiseconds
            minutes = self.time_elapsed // 6000
            seconds = (self.time_elapsed // 100) % 60
            centiseconds = self.time_elapsed % 100

            # Update time display
            self.time_display.config(
                text=f"{minutes:02}:{seconds:02}:{centiseconds:02}"
            )

            # Schedule the next update
            self.after(10, self.update_time)

    def start(self):
        if not self.running:
            self.running = True
            self.start_button.config(state="disabled")
            self.stop_button.config(state="normal")
            self.reset_button.config(state="normal")
            self.update_time()

    def stop(self):
        if self.running:
            self.running = False
            self.start_button.config(state="normal")
            self.stop_button.config(state="disabled")

    def reset(self):
        self.running = False
        self.time_elapsed = 0
        self.time_display.config(text="00:00:00")
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.reset_button.config(state="disabled")

if __name__ == "__main__":
    app = StopwatchApp()
    app.mainloop()
