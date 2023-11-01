from __future__ import annotations

import numpy as np
import pytest

from contourpy.typecheck import check_code_array, check_offset_array, check_point_array
from contourpy.types import code_dtype, offset_dtype, point_dtype


def test_check_code_array() -> None:
    # Valid code array, does not raise.
    check_code_array(np.array([1, 2, 79], dtype=code_dtype))

    with pytest.raises(TypeError, match=r"Expected numpy array not <class 'list'>"):
        check_code_array([1, 2, 79])

    with pytest.raises(ValueError, match=r"Expected numpy array of dtype <class 'numpy.uint8'>"):
        check_code_array(np.array([1, 2, 79], dtype=np.int64))

    with pytest.raises(ValueError, match=r"Expected numpy array of shape"):
        check_code_array(np.array([[1, 2, 79]], dtype=code_dtype))

    with pytest.raises(ValueError, match=r"First element of code array must be 1"):
        check_code_array(np.array([2, 2, 79], dtype=code_dtype))


def test_check_offset_array() -> None:
    # Valid offset array, does not raise.
    check_offset_array(np.array([0, 5], dtype=offset_dtype))

    with pytest.raises(TypeError, match=r"Expected numpy array not <class 'list'>"):
        check_offset_array([0, 5])

    with pytest.raises(ValueError, match=r"Expected numpy array of dtype <class 'numpy.uint32'>"):
        check_offset_array(np.array([0, 5], dtype=np.int64))

    with pytest.raises(ValueError, match=r"Expected numpy array of shape"):
        check_offset_array(np.array([[0], [5]], dtype=offset_dtype))

    with pytest.raises(ValueError, match=r"First element of offset array must be 0"):
        check_offset_array(np.array([1, 5], dtype=offset_dtype))


def test_check_point_array() -> None:
    # Valid point array, does not raise.
    check_point_array(np.array([[1.1, 2.2], [3.3, 4.4]], dtype=point_dtype))

    with pytest.raises(TypeError, match=r"Expected numpy array not <class 'list'>"):
        check_point_array([[1.1, 2.2], [3.3, 4.4]])

    with pytest.raises(ValueError, match=r"Expected numpy array of dtype <class 'numpy.float64'>"):
        check_point_array(np.array([[1.1, 2.2], [3.3, 4.4]], dtype=np.float32))

    with pytest.raises(ValueError, match=r"Expected numpy array of shape"):
        check_point_array(np.array([[1.1, 2.2, 3.3, 4.4]], dtype=point_dtype))
