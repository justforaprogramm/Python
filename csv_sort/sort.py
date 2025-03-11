from pathlib import Path
from csv import reader

# with 200 files, 8000 students and 2000 students per file, programm needs (real:0,65s; user:0,625s ;sys:0,024s)
class StudentListManager:
    def __init__(self) -> None:
        """Initialize the manager with the file paths and an empty student dictionary."""
        self.path = Path(__file__).resolve().parent
        self.lists_dir = self.path / "lists"
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
        output_file = self.path / "list.txt"
        with output_file.open("w", encoding="utf-8") as f:
            for student, files in self.slist.items():
                f.write(f"{student}: {', '.join(files)}\n")

def main() -> None:
    """Main function that initializes and runs the student list manager."""
    manager = StudentListManager()
    manager.ensure_directory()
    manager.load_csv_files()
    manager.write_txt()

if __name__ == "__main__":
    main()