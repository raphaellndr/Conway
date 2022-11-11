"""This module contains the core of the app."""

import time
from enum import Enum

import typer

from .grid.grid import CellStatus, Grid


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


def _get_neighbors_by_status(
    grid: Grid, neighbors: set[tuple], *, status: CellStatus
) -> set[tuple]:
    """Sorts neighbors by their status.

    :param grid: grid containing the neighbors' values.
    :param neighbors: neighbors to check.
    :param status: status to check.
    :return: set of sorted neighbors.
    """
    status_neighbors: set[tuple] = {
        cell_neighbor for cell_neighbor in neighbors if grid.array[cell_neighbor] == status.value
    }
    return status_neighbors


def conway(
    grid_size: int = typer.Option(10, help="Size of the grid created."),
    initialization: Initialization = typer.Option(
        Initialization.RANDOM.value, help="Type of initialization."
    ),
) -> None:
    """TODO: write docstring"""

    grid = Grid(grid_size)

    grid.grid_init(initialization.value)

    living_cells: set[tuple] = grid.find_living_cells()

    tmp_living_cells: set[tuple] = living_cells.copy()
    while True:
        print(grid.array)

        start = time.time()
        for living_cell in tmp_living_cells:
            living_cell_neighbors: set[tuple] = grid.get_cell_neighbors(*living_cell)

            living_cell_living_neighbors: set[tuple] = _get_neighbors_by_status(
                grid, living_cell_neighbors, status=CellStatus.ALIVE
            )
            living_cell_dead_neighbors: set[tuple] = _get_neighbors_by_status(
                grid, living_cell_neighbors, status=CellStatus.DEAD
            )

            if len(living_cell_living_neighbors) < 2 or len(living_cell_living_neighbors) > 3:
                living_cells.remove(tuple(living_cell))

            for dead_neighbor in living_cell_dead_neighbors:
                dead_cell_neighbors: set[tuple] = grid.get_cell_neighbors(*dead_neighbor)

                dead_cell_living_neighbors: set[tuple] = _get_neighbors_by_status(
                    grid, dead_cell_neighbors, status=CellStatus.ALIVE
                )

                if len(dead_cell_living_neighbors) == 3:
                    living_cells.add(tuple(dead_neighbor))

        for cell in living_cells:
            grid.array[cell] = 1

        for cell in tmp_living_cells - living_cells:
            grid.array[cell] = 0

        tmp_living_cells = living_cells.copy()
        print(time.time() - start)


def run() -> None:
    """Typer entrypoint."""

    app = typer.Typer(no_args_is_help=True)
    app.command(name="conway")(conway)
    app()
