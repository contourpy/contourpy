from contourpy import contour_generator, FillType
from .bench_base import BenchBase
from .util_bench import chunk_counts, corner_masks, datasets


class BenchFilledSerialChunk(BenchBase):
    params = (
        ["serial"], datasets(), [FillType.ChunkCombinedOffsets2], corner_masks(), [1000],
        chunk_counts())
    param_names = ("name", "dataset", "fill_type", "corner_mask", "n", "chunk_count")

    def setup(self, name, dataset, fill_type, corner_mask, n, chunk_count):
        self.set_xyz_and_levels(dataset, n, corner_mask != "no mask")

    def time_filled_serial_chunk(self, name, dataset, fill_type, corner_mask, n, chunk_count):
        if corner_mask == "no mask":
            corner_mask = False
        cont_gen = contour_generator(
            self.x, self.y, self.z, name=name, fill_type=fill_type, corner_mask=corner_mask,
            chunk_count=chunk_count)
        for i in range(len(self.levels)-1):
            cont_gen.filled(self.levels[i], self.levels[i+1])
