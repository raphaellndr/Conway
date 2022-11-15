"""This module contains the definition of a Grid."""

from enum import Enum

import numpy as np

from ..transform.array import padding
from .cell import CellStatus, get_neighbors, get_neighbors_by_status
from .structures import (
    OscillatingStructures,
    Oscillator,
    SpaceShip,
    SpaceshipStructures,
    Stabilized,
    StabilizedStructures,
)


class GridInitialization(Enum):
    """All possible initializations."""

    value: str

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


def update_grid(
    array: np.ndarray, living_cells: set[tuple], tmp_living_cells: set[tuple]
) -> tuple[np.ndarray, set[tuple]]:
    """Updates the grid according to the different rules.

    :param array: grid array.
    :param living_cells: positions of the living cells.
    :param tmp_living_cells: copy of living_cells.
    :return: updated grid and the positions of the living cells.
    """
    for living_cell in tmp_living_cells:
        living_cell_neighbors: set[tuple] = get_neighbors(array.shape, *living_cell)

        living_cell_living_neighbors: set[tuple] = get_neighbors_by_status(
            array, living_cell_neighbors, status=CellStatus.ALIVE
        )
        living_cell_dead_neighbors: set[tuple] = get_neighbors_by_status(
            array, living_cell_neighbors, status=CellStatus.DEAD
        )

        if len(living_cell_living_neighbors) < 2 or len(living_cell_living_neighbors) > 3:
            living_cells.remove(tuple(living_cell))

        for dead_neighbor in living_cell_dead_neighbors:
            dead_cell_neighbors: set[tuple] = get_neighbors(array.shape, *dead_neighbor)

            dead_cell_living_neighbors: set[tuple] = get_neighbors_by_status(
                array, dead_cell_neighbors, status=CellStatus.ALIVE
            )

            if len(dead_cell_living_neighbors) == 3:
                living_cells.add(tuple(dead_neighbor))

    for cell in living_cells:
        array[cell] = 1

    for cell in tmp_living_cells - living_cells:
        array[cell] = 0

    tmp_living_cells = living_cells.copy()

    return array, tmp_living_cells


class Grid:
    """Grid class."""

    def __init__(self, grid_size: int):
        """Grid constructor: initialize a blank grid.

        :param grid_size: size of the grid.
        """
        self.grid_size: int = grid_size

    def grid_init(self, structure_name: str) -> np.ndarray:
        """Initializes the grid with a stabilized structure."""

        if structure_name in set(stabilized.value for stabilized in StabilizedStructures):
            structure = Stabilized(structure_name).array
        elif structure_name in set(oscillator.value for oscillator in OscillatingStructures):
            structure = Oscillator(structure_name).array
        elif structure_name in set(spaceship.value for spaceship in SpaceshipStructures):
            structure = SpaceShip(structure_name).array
        else:
            structure = self.random_init()

        if self.grid_size < max(structure.shape):
            raise ValueError(
                f"The grid size isn't big enough to fit the chosen structure (shape = "
                f"{structure.shape})"
            )
        if self.grid_size > max(structure.shape):
            structure = padding(structure, self.grid_size, self.grid_size)

        return structure

    def random_init(self) -> np.ndarray:
        """Initializes a random grid."""

        random_grid: np.ndarray = np.random.choice(
            [0, 1], size=(self.grid_size, self.grid_size), p=[3.0 / 5, 2.0 / 5]
        )
        return random_grid
