"""Transformations on arrays."""

import numpy as np


def padding(array: np.ndarray, *, desired_height: int, desired_width: int) -> np.ndarray:
    """Pads an array to a desired shape. Credit: https://stackoverflow.com/a/59241336.

    :param array: numpy array.
    :param desired_height: desired height.
    :param desired_width: desired width.
    :return: padded array.
    """
    array_height = array.shape[0]
    array_width = array.shape[1]

    a = (desired_height - array_height) // 2  # pylint: disable=invalid-name
    aa = desired_height - a - array_height  # pylint: disable=invalid-name

    b = (desired_width - array_width) // 2  # pylint: disable=invalid-name
    bb = desired_width - b - array_width  # pylint: disable=invalid-name

    return np.pad(array, pad_width=((a, aa), (b, bb)))
