def main() -> None:
    f = lambda x: x ** 2
    
    print(f(2))

    print(f(5))

    x = int(input('give number: '))
    print(f(x))

    g = lambda x, a, b :  a * x + b
    print(g(5, 2, 3))


if __name__ == "__main__":
    main()