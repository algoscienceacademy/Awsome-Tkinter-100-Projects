import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import font

class BasicNotepad(tk.Tk):
    def __init__(self):
        super().__init__()

        # Window configuration
        self.title("Basic Notepad")
        self.geometry("600x400")
        
        # Initialize variables
        self.current_file = None
        self.is_unsaved = False
        
        # Create menu and toolbar
        self.create_menu()
        self.create_toolbar()

        # Create text area widget
        self.create_text_area()

    def create_menu(self):
        """Create the main menu for the Notepad."""
        menu = tk.Menu(self)
        self.config(menu=menu)

        # File menu
        file_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)

        # Edit menu
        edit_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo", command=self.undo)
        edit_menu.add_command(label="Redo", command=self.redo)
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", command=self.cut)
        edit_menu.add_command(label="Copy", command=self.copy)
        edit_menu.add_command(label="Paste", command=self.paste)

    def create_toolbar(self):
        """Create the toolbar with text formatting options."""
        toolbar = tk.Frame(self)
        toolbar.pack(fill=tk.X)

        # Bold button
        bold_button = tk.Button(toolbar, text="B", command=self.toggle_bold, relief=tk.RAISED)
        bold_button.pack(side=tk.LEFT)

        # Italic button
        italic_button = tk.Button(toolbar, text="I", command=self.toggle_italic, relief=tk.RAISED)
        italic_button.pack(side=tk.LEFT)

        # Underline button
        underline_button = tk.Button(toolbar, text="U", command=self.toggle_underline, relief=tk.RAISED)
        underline_button.pack(side=tk.LEFT)

    def create_text_area(self):
        """Create the main text area widget."""
        self.text_area = tk.Text(self, wrap=tk.WORD)
        self.text_area.pack(fill=tk.BOTH, expand=True)
        self.text_area.bind("<KeyRelease>", self.set_unsaved_flag)

        # Set default font
        self.font = font.Font(self.text_area, family="Arial", size=12)
        self.text_area.config(font=self.font)

    def set_unsaved_flag(self, event=None):
        """Set the unsaved flag to True when the text area is modified."""
        if not self.is_unsaved:
            self.is_unsaved = True
            self.title(f"{'*' if self.is_unsaved else ''}Basic Notepad - {self.current_file or 'Untitled'}")

    def new_file(self):
        """Create a new file."""
        if self.is_unsaved:
            response = messagebox.askyesnocancel("Unsaved Changes", "You have unsaved changes. Do you want to save them?")
            if response == True:
                self.save_file()
            elif response == None:
                return

        self.text_area.delete(1.0, tk.END)
        self.current_file = None
        self.is_unsaved = False
        self.title("Basic Notepad - Untitled")

    def open_file(self):
        """Open an existing file."""
        if self.is_unsaved:
            response = messagebox.askyesnocancel("Unsaved Changes", "You have unsaved changes. Do you want to save them?")
            if response == True:
                self.save_file()
            elif response == None:
                return

        file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, content)
                self.current_file = file_path
                self.is_unsaved = False
                self.title(f"Basic Notepad - {file_path}")

    def save_file(self):
        """Save the current file."""
        if self.current_file:
            content = self.text_area.get(1.0, tk.END)
            with open(self.current_file, 'w') as file:
                file.write(content)
            self.is_unsaved = False
            self.title(f"Basic Notepad - {self.current_file}")
        else:
            self.save_as_file()

    def save_as_file(self):
        """Save the current file as a new file."""
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            content = self.text_area.get(1.0, tk.END)
            with open(file_path, 'w') as file:
                file.write(content)
            self.current_file = file_path
            self.is_unsaved = False
            self.title(f"Basic Notepad - {file_path}")

    def undo(self):
        """Undo the last action."""
        self.text_area.edit_undo()

    def redo(self):
        """Redo the last undone action."""
        self.text_area.edit_redo()

    def cut(self):
        """Cut selected text."""
        self.text_area.event_generate("<<Cut>>")

    def copy(self):
        """Copy selected text."""
        self.text_area.event_generate("<<Copy>>")

    def paste(self):
        """Paste text from clipboard."""
        self.text_area.event_generate("<<Paste>>")

    def toggle_bold(self):
        """Toggle bold text."""
        current_tags = self.text_area.tag_names("sel.first")
        if "bold" in current_tags:
            self.text_area.tag_remove("bold", "sel.first", "sel.last")
        else:
            self.text_area.tag_add("bold", "sel.first", "sel.last")
            self.text_area.tag_configure("bold", font=(self.font.actual("family"), self.font.actual("size"), "bold"))

    def toggle_italic(self):
        """Toggle italic text."""
        current_tags = self.text_area.tag_names("sel.first")
        if "italic" in current_tags:
            self.text_area.tag_remove("italic", "sel.first", "sel.last")
        else:
            self.text_area.tag_add("italic", "sel.first", "sel.last")
            self.text_area.tag_configure("italic", font=(self.font.actual("family"), self.font.actual("size"), "italic"))

    def toggle_underline(self):
        """Toggle underline text."""
        current_tags = self.text_area.tag_names("sel.first")
        if "underline" in current_tags:
            self.text_area.tag_remove("underline", "sel.first", "sel.last")
        else:
            self.text_area.tag_add("underline", "sel.first", "sel.last")
            self.text_area.tag_configure("underline", underline=True)


if __name__ == "__main__":
    app = BasicNotepad()
    app.mainloop()
