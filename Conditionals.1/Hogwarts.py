#       list 1D       #
students = ["Hermoine", "Harry", "Ron", "Draco"]

for i in range(len(students)):
    print(i + 1, students[i])
print()

#       list 2D     #
stdents = {
    "Hermoine": "Gryffindor",
    "Harry": "Gryffindor",
    "Ron": "Gryffindor",
    "Draco": "Slytherin"
}
# print(student["Harry"])

for student in stdents:
    print(student, stdents[student], sep=", ")
print()

#       list 3D     #
studets = [
    {"name": "Hermoine", "house": "Gryffendor", "patronus": "Otter"},
    {"name": "Harry", "house": "Gryffendor", "patronus": "Stag"},
    {"name": "Ron", "house": "Gryffendor", "patronus": "Jack Russel terrier"},
    {"name": "Draco", "house": "Slyterin", "patronus": None}
]

for studet in studets:
    print(studet["name"], studet["house"], studet["patronus"], sep=", ")
print()


#       print bracked       #
def main():
    print_square(3)

def print_square(size):
    for _ in range(size):
        print_row(size)

def print_colum(height):
    print("#\n" * height, end="")
    
def print_row(width):
    print("#" * width)


main()