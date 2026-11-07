import csv
import random
import os
from faker import Faker

# Initialize the name generator
fake = Faker("de_DE")

# List of subjects
subjects = [
    "Mathematik", "Physik", "Chemie", "Biologie", "Informatik",
    "Englisch", "Deutsch", "Geschichte", "Erdkunde", "Kunst",
    "Musik", "Sport", "Politik", "Wirtschaft", "Philosophie",
    "Spanisch", "Französisch", "Latein", "Sozialkunde", "Religionslehre",
    "Umweltwissenschaften", "Astronomie", "Psychologie", "Soziologie", "Medienwissenschaften",
    "Ingenieurwissenschaften", "Statistik", "Gesundheitsbildung", "Theater", "Betriebswirtschaftslehre",
    "Designtechnik", "Fotografie", "Ethik", "Recht", "Anthropologie",
    "Robotik", "KünstlicheIntelligenz", "Cybersicherheit", "Programmierung", "Quantencomputing",
    "Spieleentwicklung", "KreativesSchreiben", "Poesieanalyse", "Literatur", "Linguistik",
    "Mythologie", "Archäologie", "ForensischeWissenschaften", "Meeresbiologie", "Genetik",
    "Astrophysik", "Pharmakologie", "Botanik", "Zoologie", "Meteorologie",
    "Ozeanografie", "Weltraumforschung", "Geologie", "Kartografie", "Animation",
    "3D-Modellierung", "Filmanalyse", "Toningenieurwesen", "Musikproduktion", "Theaterwissenschaft",
    "Modedesign", "KulinarischeKünste", "Gastgewerbe", "Sportwissenschaft", "Sportmanagement",
    "E-Sport", "Spieltheorie", "Kryptografie", "BlockchainTechnologie", "Nanotechnologie",
    "Neurowissenschaften", "KünstlichesLeben", "VirtuelleRealität", "ErweiterteRealität", "Bioinformatik",
    "Biomechanik", "Gentechnik", "Klimawissenschaften", "NachhaltigeEntwicklung", "Energietechnologie",
    "Luftfahrt", "Luft- und Raumfahrttechnik", "Automobiltechnik", "Stadtplanung", "SmartCities",
    "Landwirtschaft", "Forstwirtschaft", "Tiermedizin", "Alternativmedizin", "AstronautenTraining",
    "Überlebensfähigkeiten", "Militärwissenschaft", "Kulturwissenschaft", "Volkskunde", "Verschwörungstheorien",
    "Zukunftsforschung", "Mythbusting", "ExperimentellePhysik", "DeepLearning", "MenschlicheEnhancement"
]


# Number of students and files
num_students = 8000
num_files = 200
students_per_file = 2000

# Generate a list of unique random student names
students = list(set(fake.name() for _ in range(num_students)))

# Ensure each student appears in at least 30 different files
student_to_files = {s: set() for s in students}

# Create output directory for CSV files
output_dir = "csv_student_lists"
os.makedirs(output_dir, exist_ok=True)

# Create 100 CSV files with random subjects and _basis/_lk suffixes
csv_files = []
subject_variants = [f"{subject}_{level}" for subject in subjects for level in ["basis", "lk"]]
random.shuffle(subject_variants)  # Shuffle the subject names randomly
subject_variants = subject_variants[:num_files]  # Select exactly 100 unique file names

for subject_name in subject_variants:
    filename = f"{subject_name}.csv"
    file_path = os.path.join(output_dir, filename)
    csv_files.append(file_path)

    # Select 1000 random students for this file
    students_in_file = random.sample(students, k=students_per_file)

    # Update the file tracking for each student
    for s in students_in_file:
        student_to_files[s].add(file_path)

    # Write the CSV file
    with open(file_path, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Student"])
        for s in students_in_file:
            writer.writerow([s])

# Ensure each student appears in at least 30 different files
for s, files in student_to_files.items():
    missing = 30 - len(files)
    if missing > 0:
        available_files = list(set(csv_files) - files)
        extra_files = random.sample(available_files, k=missing)
        for ef in extra_files:
            with open(ef, mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([s])
            files.add(ef)

print(f"100 CSV files have been created in the folder '{output_dir}'.")
