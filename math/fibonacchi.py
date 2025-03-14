from functools import cache
from sys import setrecursionlimit

setrecursionlimit(10**6)

def main():
    try:
        n = int(input('enter fib num:'))
    except ValueError:
        print('what wasn\'t a number!')
        exit()
    res = fib(n)
    print(f'your fib number is {res}!')

@cache
def fib(x:int) -> int:
    
    if x <= 1:
        return x
    return fib(x-1) + fib(x-2)

if __name__ == '__main__':
    main()