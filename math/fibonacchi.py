"""fibbonachi recursive and iterative
"""

from functools import lru_cache, wraps
from sys import setrecursionlimit

setrecursionlimit(10**6)


def verbose_wrapper(func):
    """
    Decorator that adds an optional verbose mode to a Fibonacci function.

    Wraps a function of signature f(x: int) -> int and injects a `verbose`
    parameter. When verbose=True, prints the result of each call in the
    format '-> fib(x) = result'.

    Args:
        func: A callable with signature (x: int) -> int.

    Returns:
        Wrapped function with signature (x: int, verbose: bool = False) -> int.
    """

    @wraps(func)
    def inner(x: int, verbose: bool = False) -> int:
        result = func(x)
        if verbose:
            print(f"-> fib({x}) = {result}")
        return result

    return inner


@lru_cache(maxsize=None)
def fib_rec(x: int) -> int:
    """
    Compute the x-th Fibonacci number recursively with memoization.

    Uses @lru_cache to avoid redundant recomputation. Subsequent calls
    with the same argument are O(1).

    Args:
        x: Non-negative integer index into the Fibonacci sequence.

    Returns:
        The x-th Fibonacci number (0-indexed: fib(0)=0, fib(1)=1).
    """
    return x if x < 2 else fib_rec(x - 1) + fib_rec(x - 2)


@verbose_wrapper
def fib(x: int) -> int:
    """
    Compute the x-th Fibonacci number iteratively.

    Runs in O(n) time and O(1) space. Decorated with verbose_wrapper,
    so the actual signature becomes fib(x, verbose=False).

    Args:
        x: Non-negative integer index into the Fibonacci sequence.

    Returns:
        The x-th Fibonacci number (0-indexed: fib(0)=0, fib(1)=1).
    """
    if x < 2: return x
    a, b = 0, 1
    for _ in range(2, x + 1):
        a, b = b, a + b
    return b


def main():
    """
    Entry point: prompt the user for input and compute a Fibonacci number.

    Workflow:
        1. Read a non-negative integer n from stdin.
        2. Let the user choose between iterative and recursive algorithms.
        3. Optionally print all Fibonacci numbers from fib(0) to fib(n).
        4. Print the final result with the algorithm name.
    """
    try:
        n = int(input("Enter fib num: "))
    except ValueError:
        print("That wasn't a number!")
        return

    algo_choice = (
        input("Choose algorithm - iterative or recursive? (iter/rec): ").strip().lower()
    )

    if algo_choice in ("rec", "recursive"):
        fib_func = fib_rec
        algo_name = "Recursive (with cache)"
        is_rec = True
    else:
        fib_func = fib
        algo_name = "Iterative"
        is_rec = False

    debug = input("Show all numbers up to this point? (yes/no): ").strip().lower()
    show_debug = debug in ("yes", "y")

    if show_debug:
        print(f"\n--- Debug: Computing up to {n} ({algo_name}) ---")

        if is_rec:
            for i in range(n + 1):
                print(f"fib({i}) = {fib_rec(i)}")
        else:
            for i in range(n + 1):
                fib_func(i, verbose=True)

        print("--------------------------------------------------")

    res = fib_rec(n) if is_rec else fib_func(n)
    print(f"Your fib number is {res}! (Calculated using: {algo_name})")


if __name__ == "__main__":
    main()
