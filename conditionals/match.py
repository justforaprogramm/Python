"""
switch case for python with switch => match
"""
name = input("What's your name? ").strip().capitalize() # the breaks are important

match name:
    case "Harry" | "Hermoine" | "Ron": # with logic syntax
        print("Gryffindor")
    case "Draco":
        print("Slytherin")
    case _:
        print("Who?")