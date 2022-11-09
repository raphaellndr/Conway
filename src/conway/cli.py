from enum import Enum

import typer

from .grid.grid import Grid


class Initialization(Enum):
    RANDOM = "random"
    BEACON = "beacon"
    BLINKER = "blinker"
    TOAD = "toad"
    PULSAR = "pulsar"


def conway(
    grid_size: int = typer.Option(10, help="Size of the grid created."),
    initialization: str = typer.Option(
        Initialization.RANDOM.value, help="Type of initialization."
    ),
) -> None:
    grid = Grid(grid_size)

    if initialization == Initialization.RANDOM.value:
        grid.random_init()
    elif initialization == Initialization.BEACON.value:
        grid.init_beacon()
    elif initialization == Initialization.BLINKER.value:
        grid.init_blinker()
    elif initialization == Initialization.TOAD.value:
        grid.init_toad()
    elif initialization == Initialization.PULSAR.value:
        grid.init_pulsar()

    print(grid.array)


def run() -> None:
    """Typer entrypoint."""

    app = typer.Typer(no_args_is_help=True)
    app.command(name="conway")(conway)
    app()
