"""This module contains the definition of a Grid."""

import numpy as np
import typer
from loguru import logger

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
        self.array: np.ndarray = np.zeros((grid_size, grid_size))

    def grid_init(self, structure_name: str) -> None:
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

        self.array = structure

    def random_init(self) -> np.ndarray:
        """Initializes a random grid."""

        random_grid: np.ndarray = np.random.choice(
            [0, 1], size=(self.grid_size, self.grid_size), p=[4.0 / 5, 1.0 / 5]
        )
        return random_grid

    def find_living_cells(self) -> set[tuple]:
        """Gets living cells positions."""

        positions: set[tuple] = set()
        living_cells_pos: np.ndarray = np.argwhere(self.array == 1)

        if living_cells_pos.any():
            logger.info("No living cells found: exiting program")
            typer.Exit(0)

        for pos in living_cells_pos:
            positions.add(tuple(pos))

        return positions

    def get_cell_neighbors(self, x: int, y: int) -> set[tuple]:
        """Get cell's neighbors positions.

        :param x: cell's x index.
        :param y: cell's y index.
        :return: cell's neighbors positions.
        """
        neighbors: set[tuple] = set()

        for i in range(max(0, x - 1), min(x + 1, self.grid_size - 1) + 1):
            for j in range(max(0, y - 1), min(y + 1, self.grid_size - 1) + 1):
                if (i, j) == (x, y):
                    pass
                else:
                    neighbors.add((i, j))

        return neighbors
