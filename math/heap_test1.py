"""playing with heap"""
from pprint import pprint

class Heap:
    """edit a heap"""

    @staticmethod
    def pprint(lst):
        """Pretty-prints a list structurally as a binary heap tree.

        Args:
            lst (list): The list representation of the heap.

        Returns:
            None: Prints the tree layout directly to the console.
        """
        if not lst:
            print("Empty Heap")
            return

        import math
        
        n = len(lst)
        height = math.floor(math.log2(n)) + 1
        max_width = (2 ** height) * 4  # Formatting spacing multiplier

        print("\n--- Visual Heap Structure ---")
        index = 0
        for level in range(height):
            # Calculate elements on the current level
            level_elements = 2 ** level
            # Form spaces around elements to center them
            spacing = max_width // level_elements
            
            row_str = ""
            for _ in range(level_elements):
                if index < n:
                    # Center the element string within its allocated spacing block
                    row_str += f"{lst[index]}".center(spacing)
                    index += 1
                else:
                    break
            print(row_str)
            print()  # Vertical spacing between levels
        print("-----------------------------\n")

    @staticmethod
    def to_heap(lst):
        """Converts a regular list into a Max-Heap.

        Args:
            lst (list): The unsorted input list of integers.

        Returns:
            list: The structurally modified list satisfying the Max-Heap property.
        """
        n = len(lst)
        # Build a maxheap: start from the last non-leaf node and heapify up to the root
        for i in range(n // 2 - 1, -1, -1):
            Heap._heapify(lst, n, i)
        return lst

    @staticmethod
    def sort(lst):
        """Sorts the heapified list using the Heap Sort algorithm.

        Args:
            lst (list): A valid max-heap list.

        Returns:
            list: The fully sorted list in ascending order.
        """
        n = len(lst)
        # One by one extract elements from the heap
        for i in range(n - 1, 0, -1):
            # Move current root to the end
            lst[i], lst[0] = lst[0], lst[i]
            # Call max heapify on the reduced heap
            Heap._heapify(lst, i, 0)
        return lst

    @staticmethod
    def to_list(lst):
        """Returns the sorted list (already in list format).

        Args:
            lst (list): input list

        Returns:
            list: output input list
        """
        return lst

    @staticmethod
    def _heapify(lst, n, i):
        """Helper method to maintain the Max-Heap property.

        Args:
            lst (list): The list containing the heap data.
            n (int): The total size of the heap slice to consider.
            i (int): The current root index to heapify down from.

        Returns:
            None: Modifies the list in-place.
        """
        largest = i  # Initialize largest as root
        left = 2 * i + 1  # left child = 2*i + 1
        right = 2 * i + 2  # right child = 2*i + 2

        # See if left child of root exists and is greater than root
        if left < n and lst[left] > lst[largest]:
            largest = left

        # See if right child of root exists and is greater than root
        if right < n and lst[right] > lst[largest]:
            largest = right

        # Change root, if needed
        if largest != i:
            lst[i], lst[largest] = lst[largest], lst[i]  # swap
            # Heapify the root.
            Heap._heapify(lst, n, largest)


def main():
    """try a heap sorting"""
    try:
        user_input = input("Input numbers separated by commas: ")
        if not user_input.strip():
            raise ValueError
        my_list = [int(x) for x in user_input.split(",")]
    except ValueError:
        my_list = [5, 3, 7, 2, 1]
        print(f"No valid numbers to enumerate, using default:\n\t{my_list}")

    # Processing using the Heap class
    my_list = Heap.to_heap(my_list)
    Heap.pprint(my_list)
    my_list = Heap.sort(my_list)
    Heap.pprint(my_list)
    my_list = Heap.to_list(my_list)

    print(f"Sorted list is:\n\t{my_list}")


if __name__ == "__main__":
    main()
