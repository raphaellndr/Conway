"""This module contains the core of the app."""

import ctypes
import time
from copy import deepcopy
from multiprocessing import Manager, Pool, Array, Lock
from multiprocessing import synchronize
from multiprocessing.sharedctypes import SynchronizedArray

import numpy as np
import typer
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from .grid.cell import find_living_cells
from .grid.grid import Grid, GridInitialization, update_grid, update_positions


GRID_ARRAY: SynchronizedArray


def _create_subsets(main_set: list[tuple], nb_subsets: int) -> list[set[tuple]]:
    """Creates `nb_subsets` subsets from a `main_set`.

    :param main_set: set to create the subsets from.
    :param nb_subsets: number of desired subsets.
    :return: list of subsets.
    """
    subsets: list[set[tuple]] = []
    subset_size: int = len(main_set) // nb_subsets
    for _ in range(nb_subsets - 1):
        subset: set[tuple] = main_set[:subset_size]
        main_set = main_set[subset_size:]
        subsets.append(subset)

    subsets.append(set(main_set))
    return subsets


def _init_worker(array: Array) -> None:
    global GRID_ARRAY
    GRID_ARRAY = array


def _main_worker(
    main_event: synchronize.Event,
    subset_event: synchronize.Event,
    living_cells: list,
    array_shape: list[int],
    fps: int,
) -> None:
    global GRID_ARRAY

    grid_array = np.reshape(np.array(GRID_ARRAY, dtype=np.int32), array_shape)

    start_time = time.time()
    expected_time = 1000 / fps

    while True:
        prev_living_cells = set(deepcopy(living_cells))
        print(f"main worker prev living cells {sorted(prev_living_cells)}")
        print("_main_worker working")
        subset_event.set()
        print("_main_worker waiting")
        main_event.wait()
        main_event.clear()

        # Remove duplicates before updating the grid
        living_cells[:] = list(set(living_cells))

        print(f"main worker living cells {sorted(living_cells)}")
        print(f"main worker prev living cells {sorted(prev_living_cells)}")

        loaded_living_cells = set(living_cells)
        grid_array = update_grid(
            grid_array, living_cells=loaded_living_cells, prev_living_cells=prev_living_cells
        )

        GRID_ARRAY[:] = grid_array.flat[:]

        elapsed_time = time.time() - start_time
        time.sleep(max(0.0, expected_time - elapsed_time) / 1000)
        print(elapsed_time)


def _subset_worker(
    main_event: synchronize.Event,
    subset_event: synchronize.Event,
    barrier: synchronize.Barrier,
    lock: Lock,
    living_cells: list,
    index: int,
    nb_subset_workers: int,
    array_shape: list[int],
) -> None:
    global GRID_ARRAY

    grid_array = np.reshape(np.array(GRID_ARRAY, dtype=np.int32), array_shape)

    while True:
        print(f"_subset_worker{index} waiting")
        subset_event.wait()
        print(f"_subset_worker{index} working")

        loaded_living_cells = deepcopy(living_cells)
        subset_living_cells = _create_subsets(loaded_living_cells, nb_subset_workers)[index]
        print(f"_subset_worker{index} subset {subset_living_cells}")

        subset_living_cells, prev_living_cells = update_positions(
            grid_array,
            living_cells=set(loaded_living_cells),
            subset_living_cells=subset_living_cells,
        )
        print(f"_subset_worker{index} updated subset {subset_living_cells}")

        with lock:
            print(f"_subset_worker{index} living_cells {living_cells}")
            living_cells += list(subset_living_cells)
            print(f"_subset_worker{index} living_cells {living_cells}")

        print(f"_subset_worker{index} waiting for colleagues")
        if barrier.wait() == 0:
            # Notify main worker that all subset workers have finished
            main_event.set()
        subset_event.clear()


def _animation_worker(array_shape: list[int]) -> None:
    global GRID_ARRAY

    grid_array = np.reshape(np.array(GRID_ARRAY, dtype=np.int32), array_shape)

    def animate(frame_number, imm):
        array = np.reshape(np.array(GRID_ARRAY, dtype=np.int32), array_shape)
        imm.set_data(array)
        return imm

    fig = plt.figure()
    im = plt.imshow(grid_array, cmap="binary")
    _ = FuncAnimation(fig, animate, fargs=(im,), interval=0.01)
    plt.show()


def conway(
    grid_size: int = typer.Option(10, help="Size of the grid created."),
    initialization: GridInitialization = typer.Option(
        GridInitialization.RANDOM.value, help="Type of initialization."
    ),
    jobs: int = typer.Option(1, help="Number of subprocesses used."),
    fps: int = typer.Option(1, help="Expected number of FPS"),
) -> None:
    """TODO: write docstring"""
    grid: Grid = Grid(grid_size)
    grid_array: np.ndarray = grid.grid_init(initialization)
    living_cells: set[tuple] = find_living_cells(grid_array)

    nb_subset_workers = jobs - 2

    manager = Manager()
    main_event = manager.Event()
    subset_barrier = manager.Barrier(nb_subset_workers)
    subset_event = manager.Event()
    subset_lock = manager.Lock()

    shared_array = Array(ctypes.c_int32, grid_size * grid_size)
    np.frombuffer(shared_array.get_obj(), dtype=np.int32)[:] = grid_array.flat
    shared_living_cells = manager.list(list(living_cells))

    with Pool(jobs, initializer=_init_worker, initargs=(shared_array,)) as pool:
        pool.apply_async(
            _main_worker,
            args=(main_event, subset_event, shared_living_cells, grid_array.shape, fps),
        )
        pool.apply_async(_animation_worker, args=(grid_array.shape,))
        pool.starmap(
            _subset_worker,
            [
                (
                    main_event,
                    subset_event,
                    subset_barrier,
                    subset_lock,
                    shared_living_cells,
                    i,
                    nb_subset_workers,
                    grid_array.shape,
                )
                for i in range(nb_subset_workers)
            ],
        )


def run() -> None:
    """Typer entrypoint."""

    app = typer.Typer(no_args_is_help=True)
    app.command(name="conway")(conway)
    app()
