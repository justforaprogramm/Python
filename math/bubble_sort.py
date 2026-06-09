"""bubble sort implementation
"""

def bubble_sort(arr:list(int)) -> list(int):
    """a bubblesort algorythm

    Args:
        arr (list): list to sort
    return:
        _type_ : sorted list
    """
    for _ in range(len(arr)-1):
        for i in range(len(arr)-1):
            if arr[i] > arr[i+1]:
                arr[i], arr[i+1] = arr[i+1], arr[i]
    return arr

print(bubble_sort([3,5,2,4,1]))
# hat n² weil die innere ist n und außen auch n
