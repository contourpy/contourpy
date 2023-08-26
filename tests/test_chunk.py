# Test functions in chunk.py

from __future__ import annotations

import pytest

from contourpy.chunk import calc_chunk_sizes, two_factors


@pytest.mark.parametrize(
    "n, factors",
    [[1, (1, 1)], [2, (2, 1)], [3, (3, 1)], [4, (2, 2)], [5, (5, 1)], [6, (3, 2)], [7, (7, 1)],
     [8, (4, 2)], [9, (3, 3)], [10, (5, 2)], [11, (11, 1)], [12, (4, 3)], [20, (5, 4)],
     [24, (6, 4)], [30, (6, 5)], [99, (11, 9)], [100, (10, 10)], [101, (101, 1)]]
)
def test_two_factors(n: int, factors: tuple[int, int]) -> None:
    assert two_factors(n) == factors


@pytest.mark.parametrize("n", [-1, -9])
def test_two_factors_invalid(n: int) -> None:
    with pytest.raises(ValueError, match=f"two_factors expects positive integer not {n}"):
        two_factors(n)


@pytest.mark.parametrize("chunk_size", [0, 1, 2, 3, 6, 9])
def test_chunk_size_1d(chunk_size: int) -> None:
    assert calc_chunk_sizes(
        chunk_size=chunk_size, chunk_count=None, total_chunk_count=None, ny=5, nx=7,
    ) == (chunk_size, chunk_size)


@pytest.mark.parametrize("x_chunk_size, y_chunk_size", [(0, 1), (1, 3), (4, 2)])
def test_chunk_size_2d(x_chunk_size: int, y_chunk_size: int) -> None:
    assert calc_chunk_sizes(
        chunk_size=(x_chunk_size, y_chunk_size), chunk_count=None, total_chunk_count=None,
        ny=5, nx=7,
    ) == (x_chunk_size, y_chunk_size)


@pytest.mark.parametrize(
    "chunk_count, res",
    [[0, (4, 6)], [1, (4, 6)], [2, (2, 3)], [3, (2, 2)], [4, (1, 2)], [5, (1, 2)], [6, (1, 1)]],
)
def test_chunk_count_1d(chunk_count: int, res: tuple[int, int]) -> None:
    assert calc_chunk_sizes(
        chunk_size=None, chunk_count=chunk_count, total_chunk_count=None, ny=5, nx=7,
    ) == res

    # Swap x and y
    assert calc_chunk_sizes(
        chunk_size=None, chunk_count=chunk_count, total_chunk_count=None, ny=7, nx=5,
    ) == res[::-1]


@pytest.mark.parametrize(
    "chunk_count, res",
    [[(0, 0), (4, 6)], [(1, 1), (4, 6)], [(2, 2), (2, 3)], [(2, 3), (2, 2)], [(9, 9), (1, 1)]  ]
)
def test_chunk_count_2d(chunk_count: tuple[int, int], res: tuple[int, int]) -> None:
    assert calc_chunk_sizes(
        chunk_size=None, chunk_count=chunk_count, total_chunk_count=None, ny=5, nx=7,
    ) == res


@pytest.mark.parametrize(
    "total_chunk_count, res",
    [[-1, (0, 0)], [0, (0, 0)], [1, (0, 0)], [2, (4, 3)], [3, (4, 2)], [4, (2, 3)]],
)
def test_total_chunk_count(total_chunk_count: int, res: tuple[int, int]) -> None:
    assert calc_chunk_sizes(
        chunk_size=None, chunk_count=None, total_chunk_count=total_chunk_count, ny=5, nx=7,
    ) == res

    # Swap x and y..
    assert calc_chunk_sizes(
        chunk_size=None, chunk_count=None, total_chunk_count=total_chunk_count, ny=7, nx=5,
    ) == res[::-1]


def test_calc_chunk_sizes_invalid() -> None:
    msg = "Only one of chunk_size, chunk_count and total_chunk_count should be set"
    with pytest.raises(ValueError, match=msg):
        calc_chunk_sizes(chunk_size=1, chunk_count=1, total_chunk_count=None, ny=2, nx=2)
    with pytest.raises(ValueError, match=msg):
        calc_chunk_sizes(chunk_size=1, chunk_count=None, total_chunk_count=1, ny=2, nx=2)
    with pytest.raises(ValueError, match=msg):
        calc_chunk_sizes(chunk_size=None, chunk_count=1, total_chunk_count=1, ny=2, nx=2)
    with pytest.raises(ValueError, match=msg):
        calc_chunk_sizes(chunk_size=1, chunk_count=1, total_chunk_count=1, ny=2, nx=2)

    msg = r"\(ny, nx\) must be at least \(2, 2\)"
    with pytest.raises(ValueError, match=msg):
        calc_chunk_sizes(chunk_size=1, chunk_count=None, total_chunk_count=None, ny=1, nx=2)
    with pytest.raises(ValueError, match=msg):
        calc_chunk_sizes(chunk_size=1, chunk_count=None, total_chunk_count=None, ny=2, nx=1)
    with pytest.raises(ValueError, match=msg):
        calc_chunk_sizes(chunk_size=1, chunk_count=None, total_chunk_count=None, ny=1, nx=1)
