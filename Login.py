import tkinter as tk
from tkinter import messagebox

class LoginApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Window setup
        self.title("Login Page")
        self.geometry("500x400")
        self.config(bg="#f7f7f7")  # Light background color for a modern look
        self.resizable(False, False)

        # Title Frame
        title_frame = tk.Frame(self, bg="#6a1b9a", bd=10, relief="ridge")
        title_frame.pack(pady=20, fill="x")

        # Title label
        title = tk.Label(title_frame, text="Welcome Back!", font=("Helvetica", 28, "bold"), fg="white", bg="#6a1b9a")
        title.pack(pady=10)

        # Form Frame for user inputs
        form_frame = tk.Frame(self, bg="#f7f7f7", pady=20)
        form_frame.pack(pady=10, padx=30)

        # Username label and entry
        username_label = tk.Label(form_frame, text="Username:", font=("Helvetica", 16), fg="#6a1b9a", bg="#f7f7f7")
        username_label.grid(row=0, column=0, sticky="w", pady=10)
        self.username_entry = tk.Entry(form_frame, font=("Helvetica", 14), width=25, bg="#e8eaf6", relief="flat", bd=2)
        self.username_entry.grid(row=0, column=1, pady=10, padx=5)

        # Password label and entry
        password_label = tk.Label(form_frame, text="Password:", font=("Helvetica", 16), fg="#6a1b9a", bg="#f7f7f7")
        password_label.grid(row=1, column=0, sticky="w", pady=10)
        self.password_entry = tk.Entry(form_frame, font=("Helvetica", 14), width=25, show="*", bg="#e8eaf6", relief="flat", bd=2)
        self.password_entry.grid(row=1, column=1, pady=10, padx=5)

        # Button Frame
        button_frame = tk.Frame(self, bg="#f7f7f7")
        button_frame.pack(pady=20)

        # Login button
        login_button = tk.Button(button_frame, text="Login", font=("Helvetica", 16, "bold"), width=12, fg="white", bg="#6a1b9a",
                                 activebackground="#4a0072", activeforeground="white", relief="flat", command=self.login)
        login_button.pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == "admin" and password == "password":
            messagebox.showinfo("Login Successful", "Welcome to the system!")
        else:
            messagebox.showerror("Login Failed", "Invalid username or password. Try again.")

if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()
