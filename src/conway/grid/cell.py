"""This module contains useful functions to get a cell's information."""

import numpy as np


def get_neighbors(array_shape: tuple, x: int, y: int) -> set[tuple]:
    """Gets cell's neighbors positions.

    :param array_shape: shape of the array containing the cell.
    :param x: cell's x index.
    :param y: cell's y index.
    :returns: set of neighbors positions.
    """
    neighbors: set[tuple] = set()

    for i in range(max(0, x - 1), min(x + 1, array_shape[0] - 1) + 1):
        for j in range(max(0, y - 1), min(y + 1, array_shape[0] - 1) + 1):
            if (i, j) == (x, y):
                pass
            else:
                neighbors.add((i, j))

    return neighbors


def find_living_cells(array: np.ndarray) -> set[tuple]:
    """Gets living cells positions.

    :param array: array to look for living cells into.
    :returns: set of positions.
    """
    return set(zip(*np.where(array == 1)))
