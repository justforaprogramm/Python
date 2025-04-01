"""
round(number[, ndgits])

int, float
first -> int 
than -> print

everything with
+ - * / %
"""
x = float(input("What's x? "))
y = float(input("What's y? "))

z = x / y

print(f"{z:.2f}")




# with methods

def main():
    x = int(input("What's x? "))
    print("x squared is", square(x))
    
def square(n):
    return n ** 2


main()