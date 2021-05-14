from contourpy import max_threads
import pytest


def test_max_threads():
    n = max_threads()
    # Assume testing on machine with 2 or more cores.
    assert n > 1
