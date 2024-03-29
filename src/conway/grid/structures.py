"""This module contains definitions of different structures."""

import abc
from enum import Enum

import numpy as np


class StabilizedStructures(Enum):
    """Available stabilized structures."""

    BLOCK = "block"
    BEEHIVE = "beehive"
    LOAF = "loaf"
    BOAT = "boat"
    TUB = "tub"


class OscillatingStructures(Enum):
    """Available oscillating structures."""

    BEACON = "beacon"
    BLINKER = "blinker"
    TOAD = "toad"
    PULSAR = "pulsar"
    PENTA_DECATHLON = "penta_decathlon"


class SpaceshipStructures(Enum):
    """Available spaceships structures."""

    GLIDER = "glider"
    LWSS = "lwss"
    MWSS = "mwss"
    HWSS = "hwss"


class _Structure(abc.ABC):  # pylint: disable=too-few-public-methods
    """Base of every type of structure."""

    def __init__(self, name: str):
        self.array: np.ndarray = self.init_structure(name)

    def init_structure(self, name: str) -> np.ndarray:
        """Initializes a structure according to the given name."""
        return getattr(self, name)()


class Stabilized(_Structure):
    """Contains definition of stabilized structures."""

    @staticmethod
    def block() -> np.ndarray:
        """Instantiates a block structure."""
        return np.asarray([[1, 1], [1, 1]])

    @staticmethod
    def beehive() -> np.ndarray:
        """Instantiates a beehive structure."""
        return np.asarray([[0, 1, 1, 0], [1, 0, 0, 1], [0, 1, 1, 0]])

    @staticmethod
    def loaf() -> np.ndarray:
        """Instantiates a loaf structure."""
        return np.asarray([[0, 1, 1, 0], [1, 0, 0, 1], [0, 1, 0, 1], [0, 0, 1, 0]])

    @staticmethod
    def boat() -> np.ndarray:
        """Instantiates a boat structure."""
        return np.asarray([[1, 1, 0], [1, 0, 1], [0, 1, 0]])

    @staticmethod
    def tub() -> np.ndarray:
        """Instantiates a tub structure."""
        return np.asarray([[0, 1, 0], [1, 0, 1], [0, 1, 0]])


class Oscillator(_Structure):
    """Contains definition of oscillating structures."""

    @staticmethod
    def beacon() -> np.ndarray:
        """Beacon oscillator (period 2)."""
        return np.asarray([[1, 1, 0, 0], [1, 1, 0, 0], [0, 0, 1, 1], [0, 0, 1, 1]])

    @staticmethod
    def blinker() -> np.ndarray:
        """Blinker oscillator (period 2)."""
        return np.asarray([[1, 1, 1]])

    @staticmethod
    def toad() -> np.ndarray:
        """Toad oscillator (period 2)."""
        return np.asarray([[0, 1, 1, 1], [1, 1, 1, 0]])

    @staticmethod
    def pulsar() -> np.ndarray:
        """Pulsar oscillator (period 3)."""
        return np.asarray(
            [
                [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
                [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0],
                [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0],
            ]
        )

    @staticmethod
    def penta_decathlon() -> np.ndarray:
        """Penta-decathlon oscillator (period 15)."""
        return np.asarray(
            [
                [1, 1, 1],
                [1, 0, 1],
                [1, 1, 1],
                [1, 1, 1],
                [1, 1, 1],
                [1, 1, 1],
                [1, 0, 1],
                [1, 1, 1],
            ]
        )


class Spaceship(_Structure):
    """Contains definition of spaceships structures."""

    @staticmethod
    def glider():
        """Instantiates a glider spaceship."""
        return np.asarray([[0, 1, 0], [0, 0, 1], [1, 1, 1]])

    @staticmethod
    def lwss():
        """Instantiates a light-weight spaceship (lwss)."""
        return np.asarray([[1, 0, 0, 1, 0], [0, 0, 0, 0, 1], [1, 0, 0, 0, 1], [0, 1, 1, 1, 1]])

    @staticmethod
    def mwss():
        """Instantiates a middle-weight spaceship (mwss)."""
        return np.asarray(
            [
                [0, 0, 1, 0, 0, 0],
                [1, 0, 0, 0, 1, 0],
                [0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 1],
                [0, 1, 1, 1, 1, 1],
            ]
        )

    @staticmethod
    def hwss():
        """Instantiates a heavy-weight spaceship (hwss)."""
        return np.asarray(
            [
                [0, 0, 1, 1, 0, 0, 0],
                [1, 0, 0, 0, 0, 1, 0],
                [0, 0, 0, 0, 0, 0, 1],
                [1, 0, 0, 0, 0, 0, 1],
                [0, 1, 1, 1, 1, 1, 1],
            ]
        )
