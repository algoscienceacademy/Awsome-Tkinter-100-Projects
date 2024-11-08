import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from PIL import Image, ImageDraw, ImageTk

class AdvancedDrawingApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Window configuration
        self.title("Advanced Drawing App")
        self.geometry("900x700")
        self.configure(bg="#34495e")

        # Initialize drawing parameters
        self.brush_color = "#000000"
        self.brush_size = 5
        self.tool = "Pencil"

        # PIL Image for drawing
        self.image = Image.new("RGB", (700, 500), "white")
        self.draw = ImageDraw.Draw(self.image)

        # Canvas setup
        self.canvas = tk.Canvas(self, bg="white", width=700, height=500)
        self.canvas.pack(pady=20)
        self.canvas_image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, anchor="nw", image=self.canvas_image)

        # Bind mouse events
        self.canvas.bind("<B1-Motion>", self.paint)
        self.canvas.bind("<Button-1>", self.start_draw)

        # Setup UI for toolbar
        self.create_toolbar()
        
        # Track initial drawing positions
        self.start_x, self.start_y = None, None

    def create_toolbar(self):
        """Create a toolbar with brush controls, shape tools, and file options."""
        toolbar = tk.Frame(self, bg="#34495e")
        toolbar.pack(pady=5)

        # Brush size label and slider
        tk.Label(toolbar, text="Brush Size", fg="#ecf0f1", bg="#34495e", font=("Helvetica", 10)).grid(row=0, column=0, padx=5)
        size_slider = tk.Scale(toolbar, from_=1, to=20, orient="horizontal", command=self.change_brush_size, bg="#34495e", fg="#ecf0f1", length=100)
        size_slider.set(self.brush_size)
        size_slider.grid(row=0, column=1, padx=5)

        # Color picker button
        color_button = tk.Button(toolbar, text="Pick Color", command=self.pick_color, bg="#3498db", fg="white", font=("Helvetica", 10))
        color_button.grid(row=0, column=2, padx=5)

        # Tool selection
        tools = ["Pencil", "Line", "Rectangle", "Oval", "Eraser"]
        self.tool_var = tk.StringVar(value=self.tool)
        for i, tool in enumerate(tools, start=3):
            tk.Radiobutton(toolbar, text=tool, variable=self.tool_var, value=tool, command=self.select_tool, bg="#34495e", fg="#ecf0f1", font=("Helvetica", 10)).grid(row=0, column=i, padx=5)

        # Clear canvas button
        clear_button = tk.Button(toolbar, text="Clear Canvas", command=self.clear_canvas, bg="#e74c3c", fg="white", font=("Helvetica", 10))
        clear_button.grid(row=0, column=len(tools)+3, padx=5)

        # Save and Open buttons
        save_button = tk.Button(toolbar, text="Save", command=self.save_image, bg="#2ecc71", fg="white", font=("Helvetica", 10))
        save_button.grid(row=1, column=0, columnspan=2, pady=5)
        open_button = tk.Button(toolbar, text="Open", command=self.open_image, bg="#f39c12", fg="white", font=("Helvetica", 10))
        open_button.grid(row=1, column=2, columnspan=2, pady=5)

    def change_brush_size(self, size):
        """Change brush size based on slider input."""
        self.brush_size = int(size)

    def pick_color(self):
        """Open a color chooser dialog to select brush color."""
        color = colorchooser.askcolor()[1]
        if color:
            self.brush_color = color

    def select_tool(self):
        """Set the selected tool from toolbar."""
        self.tool = self.tool_var.get()

    def start_draw(self, event):
        """Record the starting position for shapes and lines."""
        self.start_x, self.start_y = event.x, event.y

    def paint(self, event):
        """Draw on canvas based on the selected tool and mouse movement."""
        if self.tool == "Pencil":
            self.canvas.create_oval(event.x - self.brush_size, event.y - self.brush_size,
                                    event.x + self.brush_size, event.y + self.brush_size,
                                    fill=self.brush_color, outline="")
            self.draw.ellipse([event.x - self.brush_size, event.y - self.brush_size,
                               event.x + self.brush_size, event.y + self.brush_size], fill=self.brush_color)
        elif self.tool == "Line":
            self.clear_preview()
            self.canvas.create_line(self.start_x, self.start_y, event.x, event.y, fill=self.brush_color, width=self.brush_size)
        elif self.tool == "Rectangle":
            self.clear_preview()
            self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, outline=self.brush_color, width=self.brush_size)
        elif self.tool == "Oval":
            self.clear_preview()
            self.canvas.create_oval(self.start_x, self.start_y, event.x, event.y, outline=self.brush_color, width=self.brush_size)
        elif self.tool == "Eraser":
            self.canvas.create_oval(event.x - self.brush_size, event.y - self.brush_size,
                                    event.x + self.brush_size, event.y + self.brush_size,
                                    fill="white", outline="")
            self.draw.ellipse([event.x - self.brush_size, event.y - self.brush_size,
                               event.x + self.brush_size, event.y + self.brush_size], fill="white")

    def clear_preview(self):
        """Clears preview shapes during drawing actions."""
        self.canvas.delete("preview")

    def clear_canvas(self):
        """Clear all drawings on the canvas and reset the PIL image."""
        self.canvas.delete("all")
        self.image = Image.new("RGB", (700, 500), "white")
        self.draw = ImageDraw.Draw(self.image)

    def save_image(self):
        """Save the drawing as an image file."""
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All Files", "*.*")])
        if file_path:
            self.image.save(file_path)
            messagebox.showinfo("Image Saved", f"Your image has been saved as {file_path}")

    def open_image(self):
        """Open an existing image file and display it on the canvas."""
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")])
        if file_path:
            self.image = Image.open(file_path).resize((700, 500), Image.ANTIALIAS)
            self.canvas_image = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, anchor="nw", image=self.canvas_image)
            self.draw = ImageDraw.Draw(self.image)
            messagebox.showinfo("Image Loaded", f"Image {file_path} loaded successfully.")

if __name__ == "__main__":
    app = AdvancedDrawingApp()
    app.mainloop()
