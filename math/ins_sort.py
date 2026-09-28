"""insertion sort for sorting lists
"""

def insertion_sort(arr:list(int)) -> list(int):
    """insertion sort a bit shortend

    Args:
        arr (list): list to sort

    Returns:
        _type_: list in sorted order
    """
    for  i in range(1, len(arr)):
        while i and arr[i] < arr[i-1]:
            arr[i], arr[i-1] = arr[i-1], arr[i]
            i = i-1
    return arr

def insertion_sort_lambda(arr:list(int)) -> list(int):
    """using lambda but still insertion

    Args:
        arr (list): list to sort

    Returns:
        _type_: list in sorted order
    """
    # pylint: disable=C3001
    swap_left = lambda i: (arr.__setitem__(slice(i-1, i+1), [arr[i], arr[i-1]]), \
         swap_left(i-1)) if i > 0 and arr[i] < arr[i-1] else None

    for i in range(1, len(arr)):
        swap_left(i)
    return arr

print(insertion_sort([1,2,3,2,5,4]))
print(insertion_sort([5,4,3,2,1]))

print(insertion_sort_lambda([1,2,3,2,5,4]))
print(insertion_sort_lambda([5,4,3,2,1]))

#    543152
#    453152 (1)
#    345152 (2)
#    134552 (3)
#    134552 (0)
#    123455 (4) = 10 wenn man die innere anschaut(5 wenn man die for anschaut)
