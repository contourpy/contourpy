from contourpy import contour_generator, LineType
from contourpy.util.data import random_uniform
import numpy as np
from .util_bench import corner_masks


class BenchLinesChunk:
    params = (corner_masks(), [1000], [1, 10, 100])
    param_names = ["corner_mask", "n", "chunk_count"]

    def setup(self, corner_mask, n, chunk_count):
        self.x, self.y, self.z = random_uniform((n, n), mask_fraction=0.05)
        if corner_mask == "no mask":
            self.z = np.ma.getdata(self.z)
        self.levels = np.arange(0.0, 1.01, 0.1)

    def time_lines_chunk(self, corner_mask, n, chunk_count):
        if corner_mask == "no mask":
            corner_mask = False
        cont_gen = contour_generator(
            self.x, self.y, self.z, name="serial", chunk_count=chunk_count,
            line_type=LineType.ChunkCombinedOffsets, corner_mask=corner_mask)
        for level in self.levels:
            cont_gen.lines(level)
