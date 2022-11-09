import numpy as np

from .structures import Beacon, Blinker, Pulsar, Toad
from ..transform.array import padding


class Grid:
    def __init__(self, grid_size: int):
        """Grid constructor: initialize a blank grid.

        :param grid_size: size of the grid.
        """
        self.grid_size: int = grid_size
        self.array: np.ndarray = np.zeros((grid_size, grid_size))

    def random_init(self):
        """Initializes a random grid.

        :return:
        """
        random_grid: np.ndarray = np.random.choice(
            [0, 1], size=(self.grid_size, self.grid_size), p=[4.0 / 5, 1.0 / 5]
        )
        self.array = random_grid

    def init_beacon(self):
        """Initializes a grid with a beacon."""

        beacon: np.ndarray = Beacon().array

        if self.grid_size < max(beacon.shape):
            raise ValueError(
                f"The grid size isn't big enough to fit a beacon (shape = {beacon.shape})"
            )

        beacon = padding(beacon, self.grid_size, self.grid_size)
        self.array = beacon

    def init_blinker(self):
        """Initializes a grid with a blinker."""

        blinker: np.ndarray = Blinker().array

        if self.grid_size < max(blinker.shape):
            raise ValueError(
                f"The grid size isn't big enough to fit a blinker (shape = {blinker.shape})"
            )

        blinker = padding(blinker, self.grid_size, self.grid_size)
        self.array = blinker

    def init_toad(self):
        """Initializes a grid with a blinker."""

        toad: np.ndarray = Toad().array

        if self.grid_size < max(toad.shape):
            raise ValueError(
                f"The grid size isn't big enough to fit a toad (shape = {toad.shape})"
            )

        toad = padding(toad, self.grid_size, self.grid_size)
        self.array = toad

    def init_pulsar(self):
        """Initializes a grid with a pulsar."""

        pulsar: np.ndarray = Pulsar().array

        if self.grid_size < max(pulsar.shape):
            raise ValueError(
                f"The grid size isn't big enough to fit a pulsar (shape: {pulsar.shape})"
            )

        pulsar = padding(pulsar, self.grid_size, self.grid_size)
        self.array = pulsar
