from contourpy import LineType, contour_generator

from .bench_base import BenchBase
from .util_bench import chunk_counts, corner_masks, datasets


class BenchLinesSerialChunk(BenchBase):
    params = (
        ["serial"], datasets(), [LineType.ChunkCombinedOffset], corner_masks(), [1000],
        chunk_counts())
    param_names = ("name", "dataset", "line_type", "corner_mask", "n", "chunk_count")

    def setup(self, name, dataset, line_type, corner_mask, n, chunk_count):
        self.set_xyz_and_levels(dataset, n, corner_mask != "no mask")

    def time_lines_serial_chunk(self, name, dataset, line_type, corner_mask, n, chunk_count):
        if corner_mask == "no mask":
            corner_mask = False
        cont_gen = contour_generator(
            self.x, self.y, self.z, name=name, line_type=line_type, corner_mask=corner_mask,
            chunk_count=chunk_count)
        for level in self.levels:
            cont_gen.lines(level)
