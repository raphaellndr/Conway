"""This module contains the definition of a Grid."""

from enum import Enum

import numpy as np

from ..transform.array import padding
from .cell import get_neighbors
from .structures import (
    Oscillator,
    SpaceShip,
    SpaceshipStructures,
    Stabilized,
    StabilizedStructures,
    OscillatingStructures,
)


class GridInitialization(Enum):
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


def update_positions(
    array: np.ndarray, living_cells: set[tuple], subset_living_cells: set[tuple]
) -> tuple[set[tuple], set[tuple]]:
    """Updates the grid according to the different rules.

    :param array: grid array.
    :param living_cells: living cells positions.
    :param subset_living_cells: subset of living cells positions.
    :return: positions of the living cells.
    """
    prev_living_cells: set[tuple] = subset_living_cells.copy()
    for living_cell in prev_living_cells:
        living_cell_neighbors: set[tuple] = get_neighbors(array.shape, *living_cell)

        living_cell_living_neighbors: set[tuple] = living_cell_neighbors.intersection(living_cells)
        living_cell_dead_neighbors: set[tuple] = (
            living_cell_neighbors - living_cell_living_neighbors
        )

        if len(living_cell_living_neighbors) < 2 or len(living_cell_living_neighbors) > 3:
            subset_living_cells.remove(tuple(living_cell))

        for dead_neighbor in living_cell_dead_neighbors:
            dead_cell_neighbors: set[tuple] = get_neighbors(array.shape, *dead_neighbor)

            dead_cell_living_neighbors: set[tuple] = dead_cell_neighbors.intersection(living_cells)

            if len(dead_cell_living_neighbors) == 3:
                subset_living_cells.add(tuple(dead_neighbor))

    return subset_living_cells, prev_living_cells


def update_grid(
    array: np.ndarray, living_cells: set[tuple], prev_living_cells: set[tuple]
) -> np.ndarray:
    """Updates the grid array.

    :param array: grid to update.
    :param living_cells: current living cells.
    :param prev_living_cells: previous living cells.
    """
    for cell in living_cells:
        array[cell] = 1

    for cell in prev_living_cells - living_cells:
        array[cell] = 0

    return array


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
        elif structure_name == GridInitialization.RANDOM.value:
            structure = self.random_init()
        else:
            raise AttributeError(f"Unknown structure: '{structure_name}'")

        if self.grid_size < max(structure.shape):
            raise ValueError(
                f"The grid size isn't big enough to fit the chosen structure (shape = "
                f"{structure.shape})"
            )
        if self.grid_size > min(structure.shape):
            structure = padding(structure, desired_h=self.grid_size, desired_w=self.grid_size)

        return structure

    def random_init(self) -> np.ndarray:
        """Initializes a random grid."""
        random_grid: np.ndarray = np.random.choice(
            [0, 1], size=(self.grid_size, self.grid_size), p=[4.0 / 5, 1.0 / 5]
        )
        return random_grid
