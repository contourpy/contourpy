from ._contourpy import FillType, LineType
from ._mpl2005 import Cntr


class Mpl2005ContourGenerator(Cntr):
    default_fill_type = FillType.OuterCodes
    default_line_type = LineType.SeparateCodes

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def chunk_count(self):
        return self._get_chunk_count()

    @property
    def chunk_size(self):
        return self._get_chunk_size()

    @property
    def fill_type(self):
        return Mpl2005ContourGenerator.default_fill_type

    @property
    def line_type(self):
        return Mpl2005ContourGenerator.default_line_type

    @staticmethod
    def supports_corner_mask():
        return False

    @staticmethod
    def supports_fill_type(fill_type):
        return fill_type == Mpl2005ContourGenerator.default_fill_type

    @staticmethod
    def supports_interp():
        return False

    @staticmethod
    def supports_line_type(line_type):
        return line_type == Mpl2005ContourGenerator.default_line_type

    @staticmethod
    def supports_threads():
        return False
