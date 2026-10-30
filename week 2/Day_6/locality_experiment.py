"""
Day 6 - CPU Cache Locality Experiment

Compares row-wise and column-wise traversal of a Python 2D list.
Note: Python nested lists are lists of references to separate row lists,
so this is an educational experiment, not a pure hardware-cache benchmark.
"""
import time 


def create_matrix(rows: int, cols: int) -> list[list[int]]:
    """Create a rows x cols matrix containing integers."""
    return [[row * cols + col for col in range(cols)] for row in range(rows)]

def row_wise_sum(matrix: list[list[int]]) -> int:
    """Visit every element from left to right, one row at a time."""
    total = 0

    for row in matrix:
        for value in row:
            total += value

    return total

def column_wise_sum(matrix: list[list[int]]) -> int:
    """Visit every element from top to bottom, one column at a time."""
    total = 0

    for col in range(len(matrix[0])):
        for row in matrix:
            total += row[col]

    return total

def measure_time(function, matrix: list[list[int]]) -> float:
    """Measure the time taken to execute a function."""
    start_time = time.time()
    function(matrix)
    end_time = time.time()
    return end_time - start_time

def main():
    rows, cols = 1000, 1000
    matrix = create_matrix(rows, cols)

    row_time = measure_time(row_wise_sum, matrix)
    print(f"Row-wise sum time: {row_time:.6f} seconds")

    col_time = measure_time(column_wise_sum, matrix)
    print(f"Column-wise sum time: {col_time:.6f} seconds")

    print(f"Matrix size: {rows} x {cols}")
    print(f"Row-wise sum: {row_time:.6f} seconds")
    print(f"Row-wise time: {row_time:.6f} seconds")
    print(f"Column-wise sum: {col_time:.6f} seconds")
    print(f"Column-wise time: {col_time:.6f} seconds")

    if row_time == col_time:
        print("Both traversal methods produced the same result.")
    else:
        print("Warning: the traversal results do not match.")


if __name__ == "__main__":
    main()