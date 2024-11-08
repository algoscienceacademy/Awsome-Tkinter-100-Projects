import tkinter as tk
from tkinter import filedialog, messagebox
import re


class NotepadClone(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Notepad++ Clone")
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

        # Configure the root window's menu
        self.config(menu=menu_bar)

    def create_text_widget(self):
        """Create a new Text widget for editing."""
        text_widget = tk.Text(self.tab_container, wrap=tk.WORD, undo=True, font=("Arial", 12), bg="#ffffff", fg="#333333")
        text_widget.bind("<KeyRelease>", self.highlight_syntax)
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
            index = content.find(search_term)
            if index != -1:
                start = f"1.0+{index}c"
                end = f"1.0+{index+len(search_term)}c"
                self.tabs[self.current_tab]["text_widget"].tag_add("highlight", start, end)
                self.tabs[self.current_tab]["text_widget"].tag_configure("highlight", background="yellow", foreground="black")

        find_button = tk.Button(find_window, text="Find", command=find_next)
        find_button.grid(row=1, column=1, padx=10, pady=10)

        find_window.mainloop()

    def replace_text(self):
        """Replace specific text with another."""
        replace_window = tk.Toplevel(self)
        replace_window.title("Replace Text")

        label1 = tk.Label(replace_window, text="Find:")
        label1.grid(row=0, column=0, padx=10, pady=10)
        search_entry = tk.Entry(replace_window, width=30)
        search_entry.grid(row=0, column=1, padx=10, pady=10)

        label2 = tk.Label(replace_window, text="Replace:")
        label2.grid(row=1, column=0, padx=10, pady=10)
        replace_entry = tk.Entry(replace_window, width=30)
        replace_entry.grid(row=1, column=1, padx=10, pady=10)

        def replace():
            search_term = search_entry.get()
            replace_term = replace_entry.get()
            content = self.tabs[self.current_tab]["text_widget"].get(1.0, tk.END)
            new_content = content.replace(search_term, replace_term)
            self.tabs[self.current_tab]["text_widget"].delete(1.0, tk.END)
            self.tabs[self.current_tab]["text_widget"].insert(tk.END, new_content)
            replace_window.destroy()

        replace_button = tk.Button(replace_window, text="Replace", command=replace)
        replace_button.grid(row=2, column=1, padx=10, pady=10)

        replace_window.mainloop()

    def undo(self, event=None):
        """Undo the last operation."""
        self.tabs[self.current_tab]["text_widget"].undo()

    def redo(self, event=None):
        """Redo the undone operation."""
        self.tabs[self.current_tab]["text_widget"].redo()

    def highlight_syntax(self, event=None):
        """Simple Python syntax highlighting."""
        keywords = ["def", "class", "import", "from", "return", "if", "else", "for", "while"]
        text_widget = self.tabs[self.current_tab]["text_widget"]
        text_content = text_widget.get(1.0, tk.END)

        text_widget.tag_remove("keyword", 1.0, tk.END)
        for keyword in keywords:
            start_index = "1.0"
            while True:
                start_index = text_widget.search(keyword, start_index, stopindex=tk.END)
                if not start_index:
                    break
                end_index = f"{start_index}+{len(keyword)}c"
                text_widget.tag_add("keyword", start_index, end_index)
                start_index = end_index
            text_widget.tag_configure("keyword", foreground="blue")

    def close_tab(self, tab_name):
        """Close the tab."""
        self.tabs[tab_name]["text_widget"].destroy()
        self.tabs[tab_name]["tab_frame"].destroy()
        del self.tabs[tab_name]
        if self.tabs:
            self.current_tab = list(self.tabs.keys())[0]
        else:
            self.current_tab = None
        self.title(f"Notepad++ Clone")

if __name__ == "__main__":
    app = NotepadClone()
    app.mainloop()
