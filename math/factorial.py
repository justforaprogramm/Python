from sys import setrecursionlimit
import math

class factorial():
    def __init__(self) -> None:
        setrecursionlimit(10**6)
        self.input = int(input('enter int to applay factorial: '))
        self.out = factorial.calculate(self.input)
    
    @staticmethod
    def calculate(n) -> int:
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result
    
    def __str__(self) -> str:
        exponent = int(math.log10(self.out))
        mantisse = self.out // (10 ** exponent)
        return f"the factorial of {self.input} is equal to {mantisse} × 10^{exponent}."

if __name__ == '__main__':
    print(factorial())