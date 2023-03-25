"""This module contains the core of the app."""

import random
from multiprocessing import Pool, cpu_count
from typing import Generator

import numpy as np
import typer
from matplotlib import pyplot as plt, animation

from .grid.cell import find_living_cells
from .grid.grid import Grid, GridInitialization, update_grid, update_positions


def _create_subsets(main_set: set[tuple], nb_subsets: int) -> list[set[tuple]]:
    """Creates ``nb_subsets`` subsets from ``main_set``.

    :param main_set: sets to create subsets from.
    :param nb_subsets: number of subsets to create.
    :return: list of subsets.
    """
    subsets: list[set[tuple]] = []
    subset_size = len(main_set) // nb_subsets
    for _ in range(nb_subsets - 1):
        subset: set[tuple] = set(random.sample(main_set, subset_size))
        main_set -= subset
        subsets.append(subset)
    subsets.append(main_set)
    return subsets


def _generate_grid(
    grid_array: np.ndarray,
    jobs: int,
) -> Generator[np.ndarray, None, None]:
    """Yields a new grid accordingly to Conway's rules.

    :param grid_array: array to update.
    :param jobs: numbers of workers (jobs) to use.
    :yield: updated grid.
    """
    living_cells: set[tuple] = find_living_cells(grid_array)
    living_cells_subsets = _create_subsets(living_cells.copy(), jobs)

    with Pool(jobs) as pool:
        while grid_array.any():
            yield grid_array

            args = [(grid_array, living_cells, subset) for subset in living_cells_subsets]

            result = pool.starmap(update_positions, args)

            living_cells = set()
            prev_living_cells = set()
            for res in result:
                living_cells.update(res[0])
                prev_living_cells.update(res[1])

            grid_array = update_grid(grid_array, living_cells, prev_living_cells)

            living_cells_subsets = _create_subsets(living_cells.copy(), jobs)


def _animate(frames: np.ndarray) -> None:
    """Plot frames."""
    plt.clf()
    plt.imshow(frames, cmap="binary")


def conway(
    grid_size: int = typer.Option(10, help="Size of the grid created."),
    initialization: GridInitialization = typer.Option(
        GridInitialization.RANDOM.value, help="Type of initialization."
    ),
    jobs: int = typer.Option(1, help="Number of subprocesses used."),
) -> None:
    """Creates a grid and initializes it with a structure (or with random cells). Animates the grid
    according to Conway's rules.

    :param grid_size: size of the grid to create.
    :param initialization: type of initialization (random or a specific structure).
    :param jobs: numbers of workers (jobs) to use.
    """
    if jobs > cpu_count():
        raise ValueError(f"Maximum of jobs possible is {cpu_count()} but {jobs} were given")

    grid: Grid = Grid(grid_size)
    grid_array: np.ndarray = grid.grid_init(initialization.value)

    generator = _generate_grid(grid_array=grid_array, jobs=jobs)
    fig = plt.figure()
    _ = animation.FuncAnimation(fig, _animate, frames=generator, repeat=False, interval=0.01)
    plt.show()


def run() -> None:
    """Typer entrypoint."""
    app = typer.Typer(no_args_is_help=True)
    app.command(name="conway")(conway)
    app()
