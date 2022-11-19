"""This module contains the core of the app."""

import random
from multiprocessing import Pool

import numpy as np
import typer
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from .grid.cell import find_living_cells
from .grid.grid import Grid, GridInitialization, update_grid, update_positions


def _create_subsets(main_set: set[tuple], nb_subsets: int) -> list[set[tuple]]:
    """Creates `nb_subsets` subsets from a `main_set`.

    :param main_set: set to create the subsets from.
    :param nb_subsets: number of desired subsets.
    :return: list of subsets.
    """
    subsets: list[set[tuple]] = []
    subset_size: int = len(main_set) // nb_subsets
    for _ in range(nb_subsets - 1):
        subset: set[tuple] = set(random.sample(main_set, subset_size))
        main_set -= subset
        subsets.append(subset)

    subsets.append(main_set)
    return subsets


def _get_pool_result(result: list[tuple[set[tuple], set[tuple]]]) -> tuple[set, set]:
    """Gets pool result.

    :param result: result of the pool.
    :return: current and previous living cells.
    """
    living_cells = set()
    prev_living_cells = set()
    for res in result:
        living_cells.update(res[0])
        prev_living_cells.update(res[1])

    return living_cells, prev_living_cells


grid: Grid = Grid(200)
grid_array: np.ndarray = grid.grid_init(GridInitialization.RANDOM)
living_cells: set[tuple] = find_living_cells(grid_array)
prev_living_cells = living_cells.copy()


def conway(
    grid_size: int = typer.Option(10, help="Size of the grid created."),
    initialization: GridInitialization = typer.Option(
        GridInitialization.RANDOM.value, help="Type of initialization."
    ),
    jobs: int = typer.Option(1, help="Number of subprocesses used."),
) -> None:
    """TODO: write docstring"""

    fig = plt.figure()
    global grid_array
    im = plt.imshow(grid_array, cmap="binary")

    with Pool(jobs) as pool:

        def update_cells():
            global living_cells, prev_living_cells

            living_cells_subsets = _create_subsets(living_cells.copy(), jobs)
            args = [(grid_array, living_cells, subset) for subset in living_cells_subsets]

            result = pool.starmap(update_positions, args)

            living_cells, prev_living_cells = _get_pool_result(result)

        def update_array():
            global grid_array
            grid_array = update_grid(grid_array, living_cells, prev_living_cells)

        def animate(i, im):
            print("animating")
            update_cells()
            update_array()
            im.set_data(grid_array)
            return im

        _ = FuncAnimation(fig, animate, fargs=(im,), interval=0.001)
        plt.show()


def run() -> None:
    """Typer entrypoint."""

    app = typer.Typer(no_args_is_help=True)
    app.command(name="conway")(conway)
    app()
