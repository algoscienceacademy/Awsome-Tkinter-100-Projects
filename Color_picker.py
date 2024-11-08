import os
import tkinter as tk
from tkinter import filedialog, colorchooser


class NotepadClone(tk.Tk):
    def __init__(self):
        super().__init__()
        self.tabs = {}
        self.current_tab = None
        self.title("Notepad++ Clone with Color Picker")
        self.geometry("800x600")

        self.create_menu()
        self.new_file()  # Create a new file tab

    def create_menu(self):
        """Create the main menu for the editor."""
        menu = tk.Menu(self)
        self.config(menu=menu)

        file_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)

        edit_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo", command=self.undo)
        edit_menu.add_command(label="Redo", command=self.redo)
        edit_menu.add_separator()
        edit_menu.add_command(label="Find", command=self.find_text)
        edit_menu.add_command(label="Replace", command=self.replace_text)

        tools_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Pick Color", command=self.open_color_picker)

    def create_text_widget(self):
        """Create and return a text widget for the editor."""
        text_widget = tk.Text(self, wrap=tk.WORD)
        text_widget.pack(fill=tk.BOTH, expand=True)
        return text_widget

    def new_file(self):
        """Create a new file tab."""
        tab_name = "Untitled"
        self.tabs[tab_name] = {
            "text_widget": self.create_text_widget(),
            "tab_frame": tk.Frame(self),
        }
        self.current_tab = tab_name
        self.title(f"{tab_name} - Notepad++ Clone with Color Picker")

    def open_file(self):
        """Open an existing file in the editor."""
        file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                tab_name = os.path.basename(file_path)
                self.tabs[tab_name] = {
                    "text_widget": self.create_text_widget(),
                    "tab_frame": tk.Frame(self),
                }
                self.tabs[tab_name]["text_widget"].insert(tk.END, content)
                self.current_tab = tab_name
                self.title(f"{tab_name} - Notepad++ Clone with Color Picker")

    def save_file(self):
        """Save the current file."""
        if self.current_tab:
            tab_name = self.current_tab
            content = self.tabs[tab_name]["text_widget"].get(1.0, tk.END)
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
            if file_path:
                with open(file_path, 'w') as file:
                    file.write(content)
                self.title(f"{os.path.basename(file_path)} - Notepad++ Clone with Color Picker")

    def save_as_file(self):
        """Save the current file as a new file."""
        if self.current_tab:
            tab_name = self.current_tab
            content = self.tabs[tab_name]["text_widget"].get(1.0, tk.END)
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
            if file_path:
                with open(file_path, 'w') as file:
                    file.write(content)
                self.title(f"{os.path.basename(file_path)} - Notepad++ Clone with Color Picker")

    def undo(self):
        """Undo the last action."""
        self.tabs[self.current_tab]["text_widget"].edit_undo()

    def redo(self):
        """Redo the last undone action."""
        self.tabs[self.current_tab]["text_widget"].edit_redo()

    def find_text(self):
        """Find a specific text in the editor."""
        find_window = tk.Toplevel(self)
        find_window.title("Find Text")

        label_find = tk.Label(find_window, text="Find:")
        label_find.grid(row=0, column=0, padx=10, pady=10)

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

    def open_color_picker(self):
        """Open the color picker dialog and display the selected color."""
        color_code = colorchooser.askcolor(title="Choose Color")[1]
        if color_code:
            self.change_background_color(color_code)

    def change_background_color(self, color_code):
        """Change the background color of the text widget."""
        self.tabs[self.current_tab]["text_widget"].config(bg=color_code)


if __name__ == "__main__":
    app = NotepadClone()
    app.mainloop()
