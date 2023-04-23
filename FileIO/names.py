"""
docs.python.og/3/libraries/functions.html#open
docs.python.og/3/libraries/functions.html#sorted

sorted(iterable, /, *, key=None, reverse=False)
"""

#       makes name      #
name = input("what's your name? ")

with  open("names.txt", "a") as file:
    file.write(f"{name}\n")

#       read names        #
names = []

with open("names.txt") as file:
    for line in sorted(file):
        names.append(line.rstrip())

for name in sorted(names, reverse=True):
    print(f"hello, {name}")