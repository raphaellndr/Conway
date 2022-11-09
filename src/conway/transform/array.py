import numpy as np


def padding(array, xx, yy):
    """Pads an array to a desired shape.

    :param array: numpy array.
    :param xx: desired height.
    :param yy: desired width.
    :return: padded array.
    """

    h = array.shape[0]
    w = array.shape[1]

    a = (xx - h) // 2
    aa = xx - a - h

    b = (yy - w) // 2
    bb = yy - b - w

    return np.pad(array, pad_width=((a, aa), (b, bb)), mode="constant")
