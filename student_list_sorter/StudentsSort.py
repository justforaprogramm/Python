import tkinter as tk
from tkinter import filedialog, ttk
import os
from pathlib import Path
from csv import reader

class StudentListManager:
    def __init__(self, input_path, output_path, output_filename) -> None:
        """Initialize the manager with the file paths and an empty student dictionary."""
        self.lists_dir = Path(input_path)
        self.output_file = Path(output_path) / output_filename
        self.slist = {}

    def ensure_directory(self) -> None:
        """Ensures that the 'lists' directory exists."""
        if not self.lists_dir.exists():
            self.lists_dir.mkdir()
            exit()

    def load_csv_files(self) -> None:
        """Loads all student names from CSV files in the 'lists' folder."""
        files = [file for file in self.lists_dir.iterdir() if file.suffix == ".csv"]

        for file in files:
            with file.open("r", encoding="utf-8") as csvfile:
                read = reader(csvfile)
                for row in read:
                    for name in row:
                        self.add_student(name.strip().title(), file.stem)

    def add_student(self, student: str, file: str) -> None:
        """Adds a student to the dictionary with the corresponding file name."""
        self.slist.setdefault(student, []).append(file)

    def write_txt(self) -> None:
        """Writes the student dictionary to a text file."""
        with self.output_file.open("w", encoding="utf-8") as f:
            for student, files in self.slist.items():
                f.write(f"{student}: {', '.join(files)}\n")

class StudentListApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student List Manager")
        self.root.geometry("400x350")

        self.create_widgets()

    def create_widgets(self):
        self.frame = ttk.Frame(self.root)
        self.frame.pack(expand=True, fill="both", padx=10, pady=10)

        self.input_frame = ttk.Frame(self.frame)
        self.input_frame.pack(pady=5, fill="x")
        self.input_button = ttk.Button(self.input_frame, text="Browse", command=self.select_input_path)
        self.input_button.pack(side="left")
        self.input_entry = ttk.Entry(self.input_frame, width=40)
        self.input_entry.pack(side="left", expand=True, fill="x")

        self.output_frame = ttk.Frame(self.frame)
        self.output_frame.pack(pady=5, fill="x")
        self.output_button = ttk.Button(self.output_frame, text="Browse", command=self.select_output_path)
        self.output_button.pack(side="left")
        self.output_entry = ttk.Entry(self.output_frame, width=25)
        self.output_entry.insert(0, os.getcwd())
        self.output_entry.pack(side="left", expand=True, fill="x")
        self.output_name_entry = ttk.Entry(self.output_frame, width=15)
        self.output_name_entry.insert(0, "lists.txt")
        self.output_name_entry.pack(side="left")

        self.process_button = ttk.Button(self.frame, text="Sort Lists", command=self.process_lists)
        self.process_button.pack(pady=10)

    def select_input_path(self):
        path = filedialog.askdirectory()
        if path:
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, path)

    def select_output_path(self):
        path = filedialog.askdirectory()
        if path:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, path)

    def process_lists(self):
        input_path = self.input_entry.get()
        output_path = self.output_entry.get()
        output_filename = self.output_name_entry.get()
        
        if input_path and output_path and output_filename:
            manager = StudentListManager(input_path, output_path, output_filename)
            manager.ensure_directory()
            manager.load_csv_files()
            manager.write_txt()
            print("Processing complete!")

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentListApp(root)
    root.mainloop()