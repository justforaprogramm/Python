"""a function to compare which string is greater, by each element
"""

def lexGreater(A:str, B:str) -> bool:
    """use builtin > to compare stings

    Args:
        A (str): origin string 
        B (str): comperisan string

    Returns:
        bool: A greater -> true else false
    """
    return A > B

def lexGreaterRec(A:str, B:str) -> bool:
    """use Recursive to compare stings

    Args:
        A (str): origin string 
        B (str): comperisan string

    Returns:
        bool: A greater -> true else false
    """
    if A[0] > B[0]:
        return True

    if A[0] < B[0]:
        return False
    try:
        return lexGreaterRec(A[1:], B[1:])
    except IndexError:
        if len(A) > len(B):
                return True
        else:
            return False

def lexGreaterIter(A: str, B: str) -> bool:
    """use Iterative to compare stings

    Args:
        A (str): origin string 
        B (str): comperisan string

    Returns:
        bool: A greater -> true else false
    """
    min_len = min(len(A), len(B))
    
    for i in range(min_len):
        if A[i] > B[i]:
            return True
        if A[i] < B[i]:
            return False

    return len(A) > len(B)

def main() -> None:
    """get user input and display output
    """
    left:str = input("Enter String1: ") 
    right:str = input("Enter String2: ")

    print(f"Built-in: {lexGreater(left, right)} | Iterative: {lexGreaterIter(left, right)} | Recursive: {lexGreaterRec(left, right)}")

if __name__ == '__main__':
    main()

# theoretical minima
# left = input("Enter String1: ") 
# right = input("Enter String2: ")
# print(left > right)
