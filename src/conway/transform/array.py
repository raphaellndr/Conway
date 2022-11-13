"""Transformations on arrays."""

import numpy as np


def padding(array: np.ndarray, desired_h: int, desired_w: int):
    """Pads an array to a desired shape. Credit: https://stackoverflow.com/a/59241336.

    :param array: numpy array.
    :param desired_h: desired height.
    :param desired_w: desired width.
    :return: padded array.
    """

    array_h = array.shape[0]
    array_w = array.shape[1]

    a = (desired_h - array_h) // 2  # pylint: disable=invalid-name
    aa = desired_h - a - array_h  # pylint: disable=invalid-name

    b = (desired_w - array_w) // 2  # pylint: disable=invalid-name
    bb = desired_w - b - array_w  # pylint: disable=invalid-name

    return np.pad(array, pad_width=((a, aa), (b, bb)), mode="constant")


def split(array: np.ndarray, n_chunks: int) -> list[np.ndarray]:
    """Splits a matrix into sub-matrices.

    :param array: array to split.
    :param n_chunks: number of chunks to slit the array into.
    :return: list of chunks.
    """

    chunks: list[np.ndarray] = []
    dimension: int = array.shape[0] // (n_chunks // 2)

    for i in range(array.shape[0] // dimension):
        for j in range(array.shape[1] // dimension):
            chunks.append(
                array[
                    max(0, dimension * i - 1) : min(dimension * (i + 1) + 1, array.shape[0]),
                    max(0, dimension * j - 1) : min(dimension * (j + 1) + 1, array.shape[0]),
                ]
            )

    return chunks
