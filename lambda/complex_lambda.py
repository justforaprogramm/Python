def main(n):
    return lambda x : x ** n

if __name__ == "__main__":
    double = main(2)
    print(double(4))