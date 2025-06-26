from functools import cache
from sys import setrecursionlimit

setrecursionlimit(10**6)

def main():
    try:
        n = int(input('enter ^n num:'))
    except ValueError:
        print('what wasn\'t a number!')
        exit()
    res:int = pot(n)
    print(f'your 2^{n} number is {res:_}!')

@cache
def pot(x:int) -> int:
    return 2 **x

if __name__ == '__main__':
    main()