"""
docs.python.org/3/library/csv.html
"""
import csv

students = []

with open("students.csv") as file:
    reader = csv.DictReader(file)
    for row in reader:
        students.append({row})#({"name": row["name"], "home": row["home"], "house": row["house"]})

for student in sorted(students, key=lambda student: student["name"]):
    print(f"{student['name']} is from {student['home']} and lives in {student ['house']}")