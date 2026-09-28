"""selection sort with local experiment"""


def select_sort(a: list[int]):
    """sorting a with selection sort

    Args:
        a (list[int]): list to sort

    Returns:
        _type_: sorted list
    """
    for i in range(len(a) - 1, 0, -1):
        swap = 0
        for j in range(1, i + 1):
            if a[j] > a[swap]:
                swap = j
        a[i], a[swap] = a[swap], a[i]
    return a


def main():
    """try selection sort"""
    try:
        my_list = [
            int(x) for x in input("Input numbers separated by commas: ").split(",")
        ]
    except ValueError:
        my_list = [5, 3, 7, 2, 1]
        print(f"no valide numbers to enumerate, using:\n\t{my_list}")

    my_list = select_sort(my_list)

    print(f"sorted list is:\n\t{my_list}")


if __name__ == "__main__":
    main()
