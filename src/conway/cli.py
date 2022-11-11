"""This module contains the core of the app."""

import time

import numpy as np
import typer

from .grid.cell import CellStatus, find_living_cells, get_neighbors, get_neighbors_by_status
from .grid.grid import Grid, GridInitialization


def conway(
    grid_size: int = typer.Option(10, help="Size of the grid created."),
    initialization: GridInitialization = typer.Option(
        GridInitialization.RANDOM.value, help="Type of initialization."
    ),
) -> None:
    """TODO: write docstring"""

    grid = Grid(grid_size)

    grid_array: np.ndarray = grid.grid_init(initialization.value)

    living_cells: set[tuple] = find_living_cells(grid_array)
    tmp_living_cells: set[tuple] = living_cells.copy()

    while True:
        print(grid_array)

        start = time.time()
        for living_cell in tmp_living_cells:
            living_cell_neighbors: set[tuple] = get_neighbors(grid_array.shape, *living_cell)

            living_cell_living_neighbors: set[tuple] = get_neighbors_by_status(
                grid_array, living_cell_neighbors, status=CellStatus.ALIVE
            )
            living_cell_dead_neighbors: set[tuple] = get_neighbors_by_status(
                grid_array, living_cell_neighbors, status=CellStatus.DEAD
            )

            if len(living_cell_living_neighbors) < 2 or len(living_cell_living_neighbors) > 3:
                living_cells.remove(tuple(living_cell))

            for dead_neighbor in living_cell_dead_neighbors:
                dead_cell_neighbors: set[tuple] = get_neighbors(grid_array.shape, *dead_neighbor)

                dead_cell_living_neighbors: set[tuple] = get_neighbors_by_status(
                    grid_array, dead_cell_neighbors, status=CellStatus.ALIVE
                )

                if len(dead_cell_living_neighbors) == 3:
                    living_cells.add(tuple(dead_neighbor))

        for cell in living_cells:
            grid_array[cell] = 1

        for cell in tmp_living_cells - living_cells:
            grid_array[cell] = 0

        tmp_living_cells = living_cells.copy()
        print(time.time() - start)


def run() -> None:
    """Typer entrypoint."""

    app = typer.Typer(no_args_is_help=True)
    app.command(name="conway")(conway)
    app()
