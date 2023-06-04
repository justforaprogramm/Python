students = ["Hermoine", "Harry", "Ron"]

#       v1      #
#gryffindors = []
#for student in students:
#    gryffindors.append({"name": student, "house": "Gryffindor"})

#       v2      #
#gryffindors = [{"name": student, "house": "Gryffindor"} for student in students]

#       v3      #
gryffindors = {student: "Gryffindor" for student in students}


#print for !# and #
print(gryffindors)


for i in range(len(students)):
    print(i + 1, students[i])
# now better v2
for i, student in enumerate(students):
    print(i + 1, students)