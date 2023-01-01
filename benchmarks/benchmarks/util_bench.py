from __future__ import annotations

from contourpy import FillType, LineType, max_threads


def corner_mask_to_bool(corner_mask: str | bool) -> bool:
    if isinstance(corner_mask, bool):
        return corner_mask
    else:
        return False


def corner_masks() -> list[str | bool]:
    return ["no mask", False, True]


def datasets() -> list[str]:
    return ["simple", "random"]


def fill_types() -> list[FillType]:
    return list(FillType.__members__.values())


def line_types() -> list[LineType]:
    return list(LineType.__members__.values())


def problem_sizes() -> list[int]:
    return [10, 30, 100, 300, 1000]


def thread_counts() -> list[int]:
    thread_counts = [1, 2, 4, 6, 8]
    return list(filter(lambda n: n <= max(max_threads(), 1), thread_counts))


def total_chunk_counts() -> list[int]:
    return [4, 12, 40, 120]
