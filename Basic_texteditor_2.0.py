import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import subprocess
import os
import sys


class NotepadClone(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Notepad++ Clone with Run System")
        self.geometry("800x600")
        self.configure(bg="#f5f5f5")

        # Set up the main menu
        self.create_menu()

        # Create the tab container (for multiple open files)
        self.tab_container = tk.Frame(self)
        self.tab_container.pack(fill=tk.BOTH, expand=True)

        # Tab tracking
        self.tabs = {}
        self.current_tab = None

        # Output pane for program results (like terminal output)
        self.output_pane = None

        # Create an empty tab on start
        self.new_file()

    def create_menu(self):
        """Create the menu bar for file operations, editing, etc."""
        menu_bar = tk.Menu(self)

        # File menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        # Edit menu
        edit_menu = tk.Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="Find", command=self.find_text)
        edit_menu.add_command(label="Replace", command=self.replace_text)
        edit_menu.add_separator()
        edit_menu.add_command(label="Undo", command=self.undo)
        edit_menu.add_command(label="Redo", command=self.redo)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)

        # Run menu (to run the code)
        run_menu = tk.Menu(menu_bar, tearoff=0)
        run_menu.add_command(label="Run Code", command=self.run_code)
        menu_bar.add_cascade(label="Run", menu=run_menu)

        # Configure the root window's menu
        self.config(menu=menu_bar)
        

    def create_text_widget(self):
        """Create a new Text widget for editing."""
        text_widget = tk.Text(self.tab_container, wrap=tk.WORD, undo=True, font=("Arial", 12), bg="#ffffff", fg="#333333")

        text_widget.bind("<Control-z>", self.undo)
        text_widget.bind("<Control-y>", self.redo)
        return text_widget

    def new_file(self):
        """Create a new tab with an empty file."""
        tab_name = f"Untitled {len(self.tabs) + 1}"
        text_widget = self.create_text_widget()
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tab_frame = tk.Frame(self.tab_container, bg="#d3d3d3", height=30)
        tab_label = tk.Label(tab_frame, text=tab_name, bg="#d3d3d3", fg="black")
        tab_label.pack(side=tk.LEFT, padx=5)

        close_button = tk.Button(tab_frame, text="x", bg="#ff0000", fg="white", command=lambda: self.close_tab(tab_name))
        close_button.pack(side=tk.RIGHT, padx=5)
        tab_frame.pack(fill=tk.X, side=tk.TOP)

        self.tabs[tab_name] = {"text_widget": text_widget, "file_path": None, "tab_frame": tab_frame}
        self.current_tab = tab_name
        self.title(f"Notepad++ Clone - {tab_name}")

    def open_file(self):
        """Open a file and load it into the current tab."""
        file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            try:
                with open(file_path, "r") as file:
                    content = file.read()
                    self.tabs[self.current_tab]["text_widget"].delete(1.0, tk.END)
                    self.tabs[self.current_tab]["text_widget"].insert(tk.END, content)
                self.tabs[self.current_tab]["file_path"] = file_path
                self.title(f"Notepad++ Clone - {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Could not open file: {e}")

    def save_file(self):
        """Save the current tab to its current file path."""
        file_path = self.tabs[self.current_tab]["file_path"]
        if file_path:
            self._save_content(file_path)
        else:
            self.save_file_as()

    def save_file_as(self):
        """Save the current tab to a new file."""
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            self._save_content(file_path)
            self.tabs[self.current_tab]["file_path"] = file_path
            self.title(f"Notepad++ Clone - {file_path}")

    def _save_content(self, file_path):
        """Helper method to save the content of the current tab."""
        try:
            with open(file_path, "w") as file:
                content = self.tabs[self.current_tab]["text_widget"].get(1.0, tk.END)
                file.write(content.strip())
        except Exception as e:
            messagebox.showerror("Error", f"Could not save file: {e}")

    def run_code(self):
        """Run the code in the current tab."""
        content = self.tabs[self.current_tab]["text_widget"].get(1.0, tk.END).strip()

        if not content:
            messagebox.showwarning("No Content", "The file is empty. Please add code to run.")
            return

        file_extension = self.tabs[self.current_tab]["file_path"][-3:] if self.tabs[self.current_tab]["file_path"] else "txt"

        if file_extension == "py":  # For Python files
            self.execute_python(content)
        elif file_extension == "cpp":  # For C++ files
            self.compile_and_run_cpp(content)
        else:
            messagebox.showerror("Unsupported", "Currently, only Python and C++ are supported for execution.")

    def execute_python(self, content):
        """Execute Python code."""
        try:
            output = subprocess.run([sys.executable, "-c", content], capture_output=True, text=True)
            self.display_output(output.stdout + "\n" + output.stderr)
        except Exception as e:
            messagebox.showerror("Execution Error", f"Error running code: {e}")

    def compile_and_run_cpp(self, content):
        """Compile and run C++ code."""
        temp_file = "temp.cpp"
        with open(temp_file, "w") as f:
            f.write(content)

        try:
            # Compile the C++ code
            compile_command = ["g++", temp_file, "-o", "temp.out"]
            subprocess.run(compile_command, capture_output=True, text=True)

            # Run the compiled executable
            run_command = ["./temp.out"]
            output = subprocess.run(run_command, capture_output=True, text=True)
            self.display_output(output.stdout + "\n" + output.stderr)

            # Clean up
            os.remove(temp_file)
            os.remove("temp.out")
        except Exception as e:
            messagebox.showerror("Execution Error", f"Error compiling or running C++ code: {e}")

    def display_output(self, output):
        """Display the output in the output pane."""
        if not self.output_pane:
            self.output_pane = scrolledtext.ScrolledText(self, height=10, wrap=tk.WORD, font=("Arial", 10))
            self.output_pane.pack(fill=tk.BOTH, expand=True)

        self.output_pane.delete(1.0, tk.END)  # Clear the previous output
        self.output_pane.insert(tk.END, output)  # Insert the new output

    def find_text(self):
        """Search for a specific text in the editor."""
        find_window = tk.Toplevel(self)
        find_window.title("Find Text")

        label = tk.Label(find_window, text="Find:")
        label.grid(row=0, column=0, padx=10, pady=10)

        search_entry = tk.Entry(find_window, width=30)
        search_entry.grid(row=0, column=1, padx=10, pady=10)

        def find_next():
            search_term = search_entry.get()
            content = self.tabs[self.current_tab]["text_widget"].get(1.0, tk.END)
            start_index = content.find(search_term)
            if start_index != -1:
                self.tabs[self.current_tab]["text_widget"].tag_add("highlight", f"1.0 + {start_index} chars", f"1.0 + {start_index + len(search_term)} chars")
                self.tabs[self.current_tab]["text_widget"].tag_configure("highlight", background="yellow")

        find_button = tk.Button(find_window, text="Find Next", command=find_next)
        find_button.grid(row=1, column=0, columnspan=2, pady=10)

        find_window.mainloop()

    def replace_text(self):
        """Replace a specific text in the editor."""
        replace_window = tk.Toplevel(self)
        replace_window.title("Replace Text")

        label_find = tk.Label(replace_window, text="Find:")
        label_find.grid(row=0, column=0, padx=10, pady=10)

        search_entry = tk.Entry(replace_window, width=30)
        search_entry.grid(row=0, column=1, padx=10, pady=10)

        label_replace = tk.Label(replace_window, text="Replace with:")
        label_replace.grid(row=1, column=0, padx=10, pady=10)

        replace_entry = tk.Entry(replace_window, width=30)
        replace_entry.grid(row=1, column=1, padx=10, pady=10)

        def replace():
            search_term = search_entry.get()
            replace_term = replace_entry.get()
            content = self.tabs[self.current_tab]["text_widget"].get(1.0, tk.END)
            updated_content = content.replace(search_term, replace_term)

            self.tabs[self.current_tab]["text_widget"].delete(1.0, tk.END)
            self.tabs[self.current_tab]["text_widget"].insert(tk.END, updated_content)

        replace_button = tk.Button(replace_window, text="Replace", command=replace)
        replace_button.grid(row=2, column=0, columnspan=2, pady=10)

        replace_window.mainloop()

    def undo(self):
        """Undo the last action."""
        self.tabs[self.current_tab]["text_widget"].edit_undo()

    def redo(self):
        """Redo the last undone action."""
        self.tabs[self.current_tab]["text_widget"].edit_redo()

    def close_tab(self, tab_name):
        """Close the current tab."""
        self.tabs[tab_name]["text_widget"].destroy()
        self.tabs[tab_name]["tab_frame"].destroy()
        del self.tabs[tab_name]

        if self.tabs:
            self.current_tab = list(self.tabs.keys())[0]
        else:
            self.current_tab = None

        self.title("Notepad++ Clone with Run System")


if __name__ == "__main__":
    app = NotepadClone()
    app.mainloop()
