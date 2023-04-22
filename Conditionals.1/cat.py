"""
loops
"""


i = 0
while i < 3:
    print("meow")
    i += 1

#for i in [0, 1, 2] :
for _ in range(3) :
    print("woff")

print("meow\n" * 3, end="")

#       good solution       #
while True:
    n = int(input("What's n? "))
    if n > 0:
        break
    # continue, break

for _ in range(n):
    print("woff")

#       with def        #
def main():
    number = get_number()
    meow(number)

def get_number():
    while True:
        n1 = int(input("What's n? "))
        if n1 > 0:
            return n1

def meow(n):
    for _ in range(n):
        print("meow")

main()