from __future__ import annotations

from typing import TYPE_CHECKING, Any

import numpy as np

from contourpy.util.data import random, simple

if TYPE_CHECKING:
    import numpy.typing as npt


class BenchBase:
    levels: npt.NDArray[np.float64]
    timeout: int = 120  # Some rendering benchmarks can take more than the default minute.
    x: npt.NDArray[np.float64]
    y: npt.NDArray[np.float64]
    z: npt.NDArray[np.float64] | np.ma.MaskedArray[Any, Any]

    def set_xyz_and_levels(self, dataset: str, n: int, want_mask: bool) -> None:
        if dataset == "random":
            mask_fraction = 0.05 if want_mask else 0.0
            self.x, self.y, self.z = random((n, n), mask_fraction=mask_fraction)
            self.levels = np.arange(0.0, 1.01, 0.1)
        elif dataset == "simple":
            self.x, self.y, self.z = simple((n, n), want_mask=want_mask)
            self.levels = np.arange(-1.0, 1.01, 0.1)
        else:
            raise NotImplementedError()
