"""This module contains the core of the app."""

import time
from enum import Enum

import numpy as np
import typer

from .grid.grid import Grid


class Initialization(Enum):
    """All possible initializations."""

    RANDOM = "random"

    BLOCK = "block"
    BEEHIVE = "beehive"
    LOAF = "loaf"
    BOAT = "boat"
    TUB = "tub"

    BEACON = "beacon"
    BLINKER = "blinker"
    TOAD = "toad"
    PULSAR = "pulsar"
    PENTA_DECATHLON = "penta_decathlon"

    GLIDER = "glider"
    LWSS = "lwss"
    MWSS = "mwss"
    HWSS = "hwss"


def conway(
    grid_size: int = typer.Option(10, help="Size of the grid created."),
    initialization: Initialization = typer.Option(
        Initialization.RANDOM.value, help="Type of initialization."
    ),
) -> None:
    """TODO: write docstring"""
    grid = Grid(grid_size)

    grid.grid_init(initialization.value)

    tmp_array: np.ndarray = grid.array.copy()
    while True:
        print(grid.array)
        start = time.time()
        living_cells: np.ndarray = grid.find_living_cells()

        for living_cell in living_cells:
            living_cell_neighbors: set[tuple[int, int]] = grid.get_cell_neighbors(*living_cell)

            living_cell_living_neighbors: set[tuple[int, int]] = {
                cell_neighbor
                for cell_neighbor in living_cell_neighbors
                if grid.array[cell_neighbor] == 1
            }
            living_cell_dead_neighbors: set[tuple[int, int]] = {
                cell_neighbor
                for cell_neighbor in living_cell_neighbors
                if grid.array[cell_neighbor] == 0
            }

            if len(living_cell_living_neighbors) < 2 or len(living_cell_living_neighbors) > 3:
                tmp_array[tuple(living_cell)] = 0

            for dead_neighbor in living_cell_dead_neighbors:
                dead_cell_neighbors: set[tuple[int, int]] = grid.get_cell_neighbors(*dead_neighbor)

                dead_cell_living_neighbors: set[tuple[int, int]] = {
                    cell_neighbor
                    for cell_neighbor in dead_cell_neighbors
                    if grid.array[cell_neighbor] == 1
                }

                if len(dead_cell_living_neighbors) == 3:
                    tmp_array[tuple(dead_neighbor)] = 1

        grid.array = tmp_array
        tmp_array = grid.array.copy()
        print(time.time() - start)


def run() -> None:
    """Typer entrypoint."""

    app = typer.Typer(no_args_is_help=True)
    app.command(name="conway")(conway)
    app()
