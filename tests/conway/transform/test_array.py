import numpy as np
import pytest

from src.conway.transform.array import padding


@pytest.mark.parametrize(
    "desired_h,desired_w,res_array",
    [
        (
            5,
            5,
            np.asarray(
                [
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0],
                ]
            ),
        ),
        (
            3,
            10,
            np.asarray(
                [
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                ]
            ),
        ),
    ],
)
def test_padding(desired_h: int, desired_w: int, res_array: np.ndarray) -> None:
    array = np.asarray(
        [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ]
    )

    padded_array = padding(array, desired_h=desired_h, desired_w=desired_w)
    assert np.array_equiv(padded_array, res_array)
