from contourpy import max_threads


def test_max_threads():
    n = max_threads()
    # Assume testing on machine with 2 or more cores.
    assert n > 1
