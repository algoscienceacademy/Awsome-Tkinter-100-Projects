import tkinter as tk
from tkinter import colorchooser

class DrawingApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Window configuration
        self.title("Colorful Drawing App")
        self.geometry("800x600")
        self.configure(bg="#34495e")

        # Canvas setup
        self.canvas = tk.Canvas(self, bg="white", width=700, height=500)
        self.canvas.pack(pady=20)

        # Initialize drawing parameters
        self.brush_color = "#000000"
        self.brush_size = 5

        # Bind mouse events
        self.canvas.bind("<B1-Motion>", self.paint)
        
        # Setup UI for controls
        self.create_controls()

    def create_controls(self):
        """Create controls for brush color, size, and clear button."""
        control_frame = tk.Frame(self, bg="#34495e")
        control_frame.pack(pady=10)

        # Brush size label and slider
        tk.Label(control_frame, text="Brush Size", fg="#ecf0f1", bg="#34495e", font=("Helvetica", 12)).grid(row=0, column=0, padx=5)
        size_slider = tk.Scale(control_frame, from_=1, to=20, orient="horizontal", command=self.change_brush_size, bg="#34495e", fg="#ecf0f1", length=150)
        size_slider.set(self.brush_size)
        size_slider.grid(row=0, column=1, padx=5)

        # Color picker button
        color_button = tk.Button(control_frame, text="Pick Color", command=self.pick_color, bg="#3498db", fg="white", font=("Helvetica", 10))
        color_button.grid(row=0, column=2, padx=5)

        # Clear canvas button
        clear_button = tk.Button(control_frame, text="Clear Canvas", command=self.clear_canvas, bg="#e74c3c", fg="white", font=("Helvetica", 10))
        clear_button.grid(row=0, column=3, padx=5)

    def change_brush_size(self, size):
        """Change brush size based on user input from slider."""
        self.brush_size = int(size)

    def pick_color(self):
        """Open color chooser dialog to change brush color."""
        color = colorchooser.askcolor()[1]
        if color:
            self.brush_color = color

    def paint(self, event):
        """Draw on canvas where the mouse is dragged."""
        x1, y1 = (event.x - self.brush_size), (event.y - self.brush_size)
        x2, y2 = (event.x + self.brush_size), (event.y + self.brush_size)
        self.canvas.create_oval(x1, y1, x2, y2, fill=self.brush_color, outline="")

    def clear_canvas(self):
        """Clear all drawings on the canvas."""
        self.canvas.delete("all")

if __name__ == "__main__":
    app = DrawingApp()
    app.mainloop()
