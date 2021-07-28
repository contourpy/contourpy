from contourpy.util.data import random, simple
import numpy as np


class BenchBase:
    def set_xyz_and_levels(self, dataset, n, want_mask):
        if dataset == "random":
            mask_fraction = 0.05 if want_mask else 0.0
            self.x, self.y, self.z = random((n, n), mask_fraction=mask_fraction)
            self.levels = np.arange(0.0, 1.01, 0.1)
        elif dataset == "simple":
            self.x, self.y, self.z = simple((n, n), want_mask=want_mask)
            self.levels = np.arange(-1.0, 1.01, 0.1)
        else:
            raise NotImplementedError()
