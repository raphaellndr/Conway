"""This module contains the definition of a Grid."""

import numpy as np

from ..transform.array import padding
from .structures import (
    OscillatingStructures,
    Oscillator,
    SpaceShip,
    SpaceshipStructures,
    Stabilized,
    StabilizedStructures,
)


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
            [0, 1], size=(self.grid_size, self.grid_size), p=[4.0 / 5, 1.0 / 5]
        )
        return random_grid
