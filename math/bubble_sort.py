"""bubble sort implementation
"""

def bubble_sort(arr:list(int)) -> list(int):
    """a bubblesort algorythm

    Args:
        arr (list): list to sort
    return:
        _type_ : sorted list
    """
    no_swap:int = 0
    for _ in range(len(arr)-1):
        if no_swap == len(arr):
            return arr
        no_swap = 0
        for i in range(len(arr)-1):
            if arr[i] > arr[i+1]:
                arr[i], arr[i+1] = arr[i+1], arr[i]
                no_swap = no_swap + 1
    return arr

print(bubble_sort([3,5,2,4,1]))
# print(bubble_sort(list(range(0, 10000))))
# print(bubble_sort(list(range(10000, 0, -1))))
# hat n² weil die innere ist n und außen auch n
