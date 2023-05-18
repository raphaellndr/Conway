# Conway
Python implementation of Conway's Game of Life.
=======

The **[Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life)**, created by John Horton Conway in 1970, 
is a zero-player game. Indeed, user only has to choose an initial state to start the game
and observe the result evolve throughout time.

This game, also called **Life**, is really simple. You have a 2D grid of cells, each being either **dead**
or **alive**. Between 2 iterations, the grid will be updated according to these following rules:

- If a cell is alive and has 2 or 3 living neighbours, this cell survives;
- If a cell is dead and has exactly 3 living neighbours, this cell becomes alive;
- Every other cell either dies or stays dead.


## Requirements

In order to be able to use this repository and play around with the code, you'll need a couple of things installed: 
Python and Poetry. And, of course, you will need to clone this repo on your machine, so Git is also required.

### Cloning the repository

Once Git [installed](https://git-scm.com/downloads), simply clone the repository on your machine:

```shell
cd your_directory
git clone https://github.com/raphaellndr/Conway.git
```

### Python

To install Python, simply head to the [download page](https://www.python.org/downloads/). This project is currently using 
python3.10, so this is the one you'll want to install.

### Poetry

To correctly run this repository, it is recommended to use Poetry. Indeed, you'll just have to create an environment with
it and every dependency will automatically be installed. To do so, first head to the [download page](https://python-poetry.org/docs/#installation)
and follow the instructions.

Then, do as follows:

- Spawn a shell within the virtual environment (if none exists yet, it will be created):

```shell
cd conway
poetry shell
```

-  Resolve the dependencies and install them:

```shell
poetry install
```

