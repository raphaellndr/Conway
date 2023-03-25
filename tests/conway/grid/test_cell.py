import numpy as np
import pytest

from src.conway.grid.cell import get_neighbors, find_living_cells


@pytest.mark.parametrize(
    "array_shape,x,y,res_neighbors",
    [
        ((3, 3), 1, 1, {(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)}),
        ((3, 3), 0, 1, {(0, 0), (0, 2), (1, 0), (1, 1), (1, 2)}),
        ((3, 3), 0, 0, {(0, 1), (1, 0), (1, 1)}),
    ],
)
def test_get_neighbors(
    array_shape: tuple, x: int, y: int, res_neighbors: set[tuple[int, int]]
) -> None:
    neighbors = get_neighbors(array_shape, x, y)
    assert neighbors == res_neighbors


@pytest.mark.parametrize(
    "array,res_living_cells",
    [
        (
            np.asarray(
                [
                    [0, 1, 0],
                    [0, 1, 0],
                    [0, 1, 0],
                ]
            ),
            {(0, 1), (1, 1), (2, 1)},
        ),
        (
            np.asarray(
                [
                    [1, 0, 0, 0, 1],
                    [0, 0, 0, 0, 0],
                    [0, 1, 1, 1, 0],
                    [0, 0, 0, 0, 0],
                    [1, 0, 0, 0, 1],
                ]
            ),
            {(0, 0), (0, 4), (2, 1), (2, 2), (2, 3), (4, 0), (4, 4)},
        ),
    ],
)
def test_find_living_cells(array: np.ndarray, res_living_cells: set[tuple]) -> None:
    living_cells = find_living_cells(array)
    assert living_cells == res_living_cells
