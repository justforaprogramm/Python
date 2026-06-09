"""a function to compare which string is greater, by each element
"""

def lex_greater(a:str, b:str) -> bool:
    """use builtin > to compare stings

    args:
        a (str): origin string 
        b (str): comperisan string

    Returns:
        bool: a greater -> true else false
    """
    return a > b

def lex_greater_rec(a:str, b:str) -> bool:
    """use Recursive to compare stings

    args:
        a (str): origin string 
        b (str): comperisan string

    Returns:
        bool: a greater -> true else false
    """
    if a[0] > b[0]:
        return True

    if a[0] < b[0]:
        return False
    try:
        return lex_greater_rec(a[1:], b[1:])
    except IndexError:
        if len(a) > len(b):
            return True
        return False

def lex_greater_iter(a: str, b: str) -> bool:
    """use Iterative to compare stings

    args:
        a (str): origin string 
        b (str): comperisan string

    Returns:
        bool: a greater -> true else false
    """
    min_len = min(len(a), len(b))

    for i in range(min_len):
        if a[i] > b[i]:
            return True
        return False

    return len(a) > len(b)

def main() -> None:
    """get user input and display output
    """
    left:str = input("Enter String1: ")
    right:str = input("Enter String2: ")

    print(f"Built-in: {lex_greater(left, right)} \
        | Iterative: {lex_greater_iter(left, right)} \
        | Recursive: {lex_greater_rec(left, right)}")

if __name__ == '__main__':
    main()

# theoretical minima
# left = input("Enter String1: ")
# right = input("Enter String2: ")
# print(left > right)
