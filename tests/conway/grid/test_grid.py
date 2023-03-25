import numpy as np
import pytest

from conway.grid.cell import find_living_cells
from src.conway.grid.grid import update_positions, update_grid, Grid


@pytest.mark.parametrize(
    "structure,subset_living_cells,res_subset_living_cells",
    [
        ("blinker", {(1, 0)}, {(0, 1), (2, 1)}),
        ("beacon", {(1, 0)}, {(1, 0)}),
        ("toad", {(1, 2)}, {(0, 2), (2, 3)}),
    ],
)
def test_update_positions(
    structure: str, subset_living_cells: set[tuple], res_subset_living_cells: set[tuple]
) -> None:
    grid = Grid(4).grid_init(structure)
    living_cells = find_living_cells(grid)
    subset_living_cells, _ = update_positions(grid, living_cells, subset_living_cells)

    assert subset_living_cells == res_subset_living_cells


@pytest.mark.parametrize(
    "living_cells,prev_living_cells,res_array",
    [
        (
            {(0, 0)},
            {(0, 0), (0, 3), (3, 0), (3, 3)},
            np.asarray(
                [
                    [1, 0, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0],
                ]
            ),
        ),
        (
            {(1, 1), (1, 2), (2, 1), (2, 2)},
            {(0, 0), (0, 3), (3, 0), (3, 3)},
            np.asarray(
                [
                    [0, 0, 0, 0],
                    [0, 1, 1, 0],
                    [0, 1, 1, 0],
                    [0, 0, 0, 0],
                ]
            ),
        ),
    ],
)
def test_update_grid(
    living_cells: set[tuple], prev_living_cells: set[tuple], res_array: np.ndarray
) -> None:
    array = np.asarray(
        [
            [1, 0, 0, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [1, 0, 0, 1],
        ]
    )
    array = update_grid(array, living_cells, prev_living_cells)
    assert np.array_equiv(array, res_array)


@pytest.mark.parametrize(
    "structure,res_grid",
    [
        (
            "blinker",
            np.asarray(
                [
                    [0, 0, 0, 0],
                    [1, 1, 1, 0],
                    [0, 0, 0, 0],
                    [0, 0, 0, 0],
                ]
            ),
        ),
        (
            "beacon",
            np.asarray(
                [
                    [1, 1, 0, 0],
                    [1, 1, 0, 0],
                    [0, 0, 1, 1],
                    [0, 0, 1, 1],
                ]
            ),
        ),
        (
            "tub",
            np.asarray(
                [
                    [0, 1, 0, 0],
                    [1, 0, 1, 0],
                    [0, 1, 0, 0],
                    [0, 0, 0, 0],
                ]
            ),
        ),
    ],
)
def test_grid_initialization(structure: str, res_grid: np.ndarray) -> None:
    grid = Grid(4).grid_init(structure)
    assert np.array_equiv(grid, res_grid)
