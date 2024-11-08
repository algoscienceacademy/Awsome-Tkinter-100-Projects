import tkinter as tk

class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Colorful Calculator")
        self.geometry("400x600")
        self.resizable(False, False)

        self.result_var = tk.StringVar()

        # Display
        self.create_display()

        # Buttons
        self.create_buttons()

    def create_display(self):
        entry = tk.Entry(self, textvariable=self.result_var, font=("Arial", 24), bd=10, relief="sunken", justify="right", bg="#f0f0f0", fg="#333")
        entry.grid(row=0, column=0, columnspan=4, sticky="nsew")

    def create_buttons(self):
        button_data = [
            ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("/", 1, 3, "#ff7f7f"),
            ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("*", 2, 3, "#ff7f7f"),
            ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("-", 3, 3, "#ff7f7f"),
            ("0", 4, 0), (".", 4, 1), ("=", 4, 2, "#ff7f7f"), ("+", 4, 3, "#ff7f7f"),
            ("C", 5, 0, "#ff9f00"), ("sqrt", 5, 1, "#9f7fff"), ("^2", 5, 2, "#9f7fff")
        ]
        
        for item in button_data:
            text, row, col = item[:3]
            color = item[3] if len(item) > 3 else "#f0f0f0"
            button = tk.Button(self, text=text, font=("Arial", 20), bd=5, relief="raised", 
                               command=lambda t=text: self.on_button_click(t), 
                               bg=color, fg="black", activebackground="#ff4500", activeforeground="white")
            button.grid(row=row, column=col, sticky="nsew", ipadx=10, ipady=10)

        # Configure grid weights for resizing
        for i in range(6):
            self.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.grid_columnconfigure(i, weight=1)

    def on_button_click(self, button_text):
        current_text = self.result_var.get()

        if button_text == "=":
            try:
                # Evaluate the expression safely
                result = str(eval(current_text))
                self.result_var.set(result)
            except Exception:
                self.result_var.set("Error")
        elif button_text == "C":
            self.result_var.set("")  # Clear the display
        elif button_text == "sqrt":
            try:
                # Calculate square root
                result = str(eval(current_text)**0.5)
                self.result_var.set(result)
            except Exception:
                self.result_var.set("Error")
        elif button_text == "^2":
            try:
                # Square the number
                result = str(eval(current_text)**2)
                self.result_var.set(result)
            except Exception:
                self.result_var.set("Error")
        else:
            self.result_var.set(current_text + button_text)  # Add the button text to the current expression

if __name__ == "__main__":
    app = Calculator()
    app.mainloop()
