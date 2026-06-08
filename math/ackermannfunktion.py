"""
ackermann.py
------------
Demonstrates the Ackermann function using an object-oriented approach.
The Ackermann function is a classic example of a recursive function that is
not primitive recursive and grows faster than any primitive recursive function.
"""
from functools import lru_cache
from sys import setrecursionlimit

setrecursionlimit(10**6)

class Ackermann:
    """
    Computes the Ackermann function for two non-negative integers m and n.

    The Ackermann function is defined as:
        ack(0, n)    = n + 1
        ack(m, 0)    = ack(m - 1, 1)        for m > 0
        ack(m, n)    = ack(m - 1, ack(m, n - 1))  for m > 0 and n > 0

    Attributes:
        m (int):      First non-negative integer input.
        n (int):      Second non-negative integer input.
        result (int): Computed result of ack(m, n).
    """

    def __init__(self, m: int, n: int) -> None:
        """
        Initialise the Ackermann instance and immediately compute the result.

        Args:
            m (int): First argument – controls recursion depth.
            n (int): Second argument – starting value.

        Raises:
            ValueError: If either m or n is negative.
        """
        # Validate that both inputs are non-negative integers
        if m < 0 or n < 0:
            raise ValueError("m and n must be non-negative integers.")

        self.m: int = m  # First input value
        self.n: int = n  # Second input value
        self.result: int = self._calc(m, n)  # Precomputed result

    @lru_cache(maxsize=None)
    def _calc(self, m: int, n: int) -> int:
        """
        Recursively compute the Ackermann function for the given m and n.

        Args:
            m (int): Current value of the first argument.
            n (int): Current value of the second argument.

        Returns:
            int: The result of ack(m, n).
        """
        if m == 0:
            # Base case: return the successor of n
            return n + 1
        if n == 0:
            # If n is exhausted, decrement m and reset n to 1
            return self._calc(m - 1, 1)
        # General case: double recursion
        inner_result: int = self._calc(m, n - 1)
        return self._calc(m - 1, inner_result)

    def __str__(self) -> str:
        """
        Return a human-readable representation of the computation.

        Returns:
            str: A string in the format 'ack(m, n) = result'.
        """
        return f"ack({self.m}, {self.n}) = {self.result}"

    def compute(self, m: int, n: int) -> int:
        """
        Public interface to compute the Ackermann function for arbitrary inputs.

        Args:
            m (int): First non-negative integer argument.
            n (int): Second non-negative integer argument.

        Returns:
            int: The result of ack(m, n).
        """
        return self._calc(m, n)


if __name__ == "__main__":
    # Test cases covering edge cases and moderately large values
    test_cases: list[tuple[int, int]] = [
        (0, 0),  # Smallest possible input
        (0, 5),  # Base case with larger n
        (1, 1),  # Simple recursive case
        (2, 3),  # Moderate depth
        (3, 4),  # Deeper recursion – result: 125
        (4, 1),  # Exceeds Python's default recursion limit
    ]

    for test_case in test_cases:
        m_val: int = test_case[0]  # First argument for this test case
        n_val: int = test_case[1]  # Second argument for this test case
        try:
            ackermann_instance = Ackermann(m_val, n_val)
            print(ackermann_instance)
        except RecursionError:
            # ack(4, x) and beyond grow too fast for Python's call stack
            print(f"ack({m_val}, {n_val}) = recursion limit exceeded")
