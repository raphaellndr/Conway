"""Transformations on arrays."""

import numpy as np


def padding(array: np.ndarray, *, desired_h: int, desired_w: int) -> np.ndarray:
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

    return np.pad(array, pad_width=((a, aa), (b, bb)))
