import tkinter as tk
from tkinter import messagebox

class TodoApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Colorful To-Do List")
        self.geometry("400x500")
        self.resizable(False, False)

        self.tasks = []

        # Display title
        self.create_title()

        # Listbox to show tasks
        self.create_task_list()

        # Entry for new task
        self.create_task_entry()

        # Buttons for adding, removing, and clearing tasks
        self.create_buttons()

    def create_title(self):
        title = tk.Label(self, text="To-Do List", font=("Arial", 30), bg="#ff7f7f", fg="white", pady=20)
        title.pack(fill="x")

    def create_task_list(self):
        self.listbox = tk.Listbox(self, height=10, width=50, font=("Arial", 18), bd=5, selectmode=tk.SINGLE, bg="#f0f0f0", fg="#333")
        self.listbox.pack(padx=20, pady=20)

    def create_task_entry(self):
        self.task_entry = tk.Entry(self, font=("Arial", 18), bd=5, width=40, bg="#f9f9f9", fg="#333")
        self.task_entry.pack(pady=10)

    def create_buttons(self):
        add_button = tk.Button(self, text="Add Task", font=("Arial", 18), bd=5, relief="raised", bg="#7f9f7f", fg="white", command=self.add_task)
        add_button.pack(pady=5, padx=10, fill="x")

        remove_button = tk.Button(self, text="Remove Task", font=("Arial", 18), bd=5, relief="raised", bg="#ff7f7f", fg="white", command=self.remove_task)
        remove_button.pack(pady=5, padx=10, fill="x")

        clear_button = tk.Button(self, text="Clear All", font=("Arial", 18), bd=5, relief="raised", bg="#ff9f00", fg="white", command=self.clear_tasks)
        clear_button.pack(pady=5, padx=10, fill="x")

    def add_task(self):
        task = self.task_entry.get()
        if task != "":
            self.tasks.append(task)
            self.update_task_list()
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Please enter a task!")

    def remove_task(self):
        try:
            selected_task_index = self.listbox.curselection()[0]
            self.tasks.pop(selected_task_index)
            self.update_task_list()
        except IndexError:
            messagebox.showwarning("Selection Error", "Please select a task to remove!")

    def clear_tasks(self):
        self.tasks.clear()
        self.update_task_list()

    def update_task_list(self):
        self.listbox.delete(0, tk.END)
        for task in self.tasks:
            self.listbox.insert(tk.END, task)


if __name__ == "__main__":
    app = TodoApp()
    app.mainloop()
