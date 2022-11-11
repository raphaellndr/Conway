"""This module contains definition of different structures."""

from enum import Enum

import numpy as np


class StabilizedStructures(Enum):
    """Possible stabilized structures."""

    BLOCK = "block"
    BEEHIVE = "beehive"
    LOAF = "loaf"
    BOAT = "boat"
    TUB = "tub"


class OscillatingStructures(Enum):
    """Possible oscillating structures."""

    BEACON = "beacon"
    BLINKER = "blinker"
    TOAD = "toad"
    PULSAR = "pulsar"
    PENTA_DECATHLON = "penta_decathlon"


class SpaceshipStructures(Enum):
    """Possible spaceships structures."""

    GLIDER = "glider"
    LWSS = "lwss"
    MWSS = "mwss"
    HWSS = "hwss"


class Stabilized:
    """Contains the definition of stabilized structures."""

    def __init__(self, name: str):
        self.array: np.ndarray = self.init_structure(name)

    def init_structure(self, name: str) -> np.ndarray:
        """Initializes a stabilized structure according to the name given."""

        if name == StabilizedStructures.BLOCK.value:
            return self.block()
        if name == StabilizedStructures.BEEHIVE.value:
            return self.beehive()
        if name == StabilizedStructures.LOAF.value:
            return self.loaf()
        if name == StabilizedStructures.BOAT.value:
            return self.boat()
        return self.tub()

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

        return np.asarray([[1, 1], [1, 1]])

    @staticmethod
    def tub() -> np.ndarray:
        """Instantiates a tub structure."""

        return np.asarray([[1, 1], [1, 1]])


class Oscillator:
    """Contains the definition of oscillating structures."""

    def __init__(self, name: str):
        self.array: np.ndarray = self.init_structure(name)

    def init_structure(self, name: str) -> np.ndarray:
        """Initializes an oscillator according to the name given."""

        if name == OscillatingStructures.BEACON.value:
            return self.beacon()
        if name == OscillatingStructures.BLINKER.value:
            return self.blinker()
        if name == OscillatingStructures.TOAD.value:
            return self.toad()
        if name == OscillatingStructures.PULSAR.value:
            return self.pulsar()
        return self.penta_decathlon()

    @staticmethod
    def beacon() -> np.ndarray:
        """Beacon oscillator (period 2)"""

        return np.asarray([[1, 1, 0, 0], [1, 1, 0, 0], [0, 0, 1, 1], [0, 0, 1, 1]])

    @staticmethod
    def blinker() -> np.ndarray:
        """Blinker oscillator (period 2)"""

        return np.asarray([[1, 1, 1]])

    @staticmethod
    def toad() -> np.ndarray:
        """Toad oscillator (period 2)"""

        return np.asarray([[0, 1, 1, 1], [1, 1, 1, 0]])

    @staticmethod
    def pulsar() -> np.ndarray:
        """Pulsar oscillator (period 3)"""

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
        """Penta-decathlon oscillator (period 15)"""

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


class SpaceShip:
    """Contains the definition of spaceships structures."""

    def __init__(self, name: str):
        self.array: np.ndarray = self.init_structure(name)

    def init_structure(self, name: str) -> np.ndarray:
        """Initializes a spaceship according to the name given."""

        if name == SpaceshipStructures.GLIDER.value:
            return self.glider()
        if name == SpaceshipStructures.LWSS.value:
            return self.lwss()
        if name == SpaceshipStructures.MWSS.value:
            return self.mwss()
        return self.hwss()

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
