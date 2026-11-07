"""docs.python.org
   docs.python.org/3/tutorial
   docs.python.org/3/library
   docs.python.org/3/reference
   docs.python.org/3/howto
"""
students =[
    {"name": "Hermione", "house": "Gryffindor"},
    {"name": "Harry" ,"house": "Gryffindor"},
    {"name": "Ron", "house": "Gryffindor"},
    {"name": "Draco", "house": "Slytherin"},
    {"name": "Padma", "house": "Ravenclaw"},
]

houses = set()
for student in students:
    houses.add(student["house"])

for house in sorted(houses):
    print(house)