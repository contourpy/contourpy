from ._contourpy import FillType, LineType
from ._mpl2005 import Cntr


class Mpl2005ContourGenerator(Cntr):
    default_line_type = LineType.SeparateCodes
    default_fill_type = FillType.OuterCodes

    def __init__(self, *args, **kwargs):
        line_type = kwargs.pop('line_type', None)
        if line_type is not None and line_type != self.default_line_type:
            raise ValueError(f'mpl2005 contour generator does not support line_type {line_type}')

        fill_type = kwargs.pop('fill_type', None)
        if fill_type is not None and fill_type != self.default_fill_type:
            raise ValueError(f'mpl2005 contour generator does not support fill_type {fill_type}')

        super().__init__(*args, **kwargs)

    @property
    def chunk_count(self):
        return self._get_chunk_count()

    @property
    def chunk_size(self):
        return self._get_chunk_size()

    @property
    def fill_type(self):
        return self.default_fill_type

    @property
    def line_type(self):
        return self.default_line_type

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
