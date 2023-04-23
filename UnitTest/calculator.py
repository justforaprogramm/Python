"""
pytest
docs.pytest.org
"""
def main():
    x = int(input("What's pow of? "))
    y = int(input("^"))
    print(f"{x} to the power of {y} is", square(x, y))

def square(n, p):
    r = pow(n, p)
    return r

if __name__ == "__main__":
    main()