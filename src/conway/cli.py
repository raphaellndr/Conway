"""This module contains the core of the app."""


import numpy as np
import typer

from .grid.cell import find_living_cells
from .grid.grid import Grid, GridInitialization, update_grid
from .transform.array import split


def conway(
    grid_size: int = typer.Option(10, help="Size of the grid created."),
    initialization: GridInitialization = typer.Option(
        GridInitialization.RANDOM.value, help="Type of initialization."
    ),
    jobs: int = typer.Option(None, help="Number of subprocesses used."),
) -> None:
    """TODO: write docstring"""

    grid = Grid(grid_size)

    grid_array: np.ndarray = grid.grid_init(initialization.value)

    chunks: list[np.ndarray] = split(grid_array, jobs)

    for chunk in chunks:
        print(chunk)

    living_cells: set[tuple] = find_living_cells(grid_array)
    tmp_living_cells: set[tuple] = living_cells.copy()

    while True:
        print(grid_array)

        grid_array, tmp_living_cells = update_grid(grid_array, living_cells, tmp_living_cells)


def run() -> None:
    """Typer entrypoint."""

    app = typer.Typer(no_args_is_help=True)
    app.command(name="conway")(conway)
    app()
