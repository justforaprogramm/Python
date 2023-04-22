#       list        #
# students = ["Hermoine", "Harry", "Ron", "Draco"]

#for i in range(len(students)):
#    print(i + 1, students[i])

students = {
    "Hermoine": "Gryffindor",
    "Harry": "Gryffindor",
    "Ron": "Gryffindor",
    "Draco": "Slytherin"
}
# print(student["Harry"])

for student in students:
    print(student, students[student], sep=",")