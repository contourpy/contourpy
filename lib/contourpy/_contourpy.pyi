from __future__ import annotations

from typing import ClassVar, NoReturn

import numpy as np
import numpy.typing as npt
from typing_extensions import TypeAlias

import contourpy._contourpy

# Input numpy array types, the same as in common.h
CoordinateArray: TypeAlias = npt.NDArray[np.float64]
MaskArray: TypeAlias = npt.NDArray[np.bool_]

# Output numpy array types, the same as in common.h
PointArray: TypeAlias = npt.NDArray[np.float64]
CodeArray: TypeAlias = npt.NDArray[np.uint8]
OffsetArray: TypeAlias = npt.NDArray[np.uint32]

# Types returned from filled()
FillReturn_OuterCode: TypeAlias = tuple[list[PointArray], list[CodeArray]]
FillReturn_OuterOffset: TypeAlias = tuple[list[PointArray], list[OffsetArray]]
FillReturn_ChunkCombinedCode: TypeAlias = tuple[list[PointArray | None], list[CodeArray | None]]
FillReturn_ChunkCombinedOffset: TypeAlias = tuple[list[PointArray | None], list[OffsetArray | None]]
FillReturn_ChunkCombinedCodeOffset: TypeAlias = tuple[list[PointArray | None], list[CodeArray | None], list[OffsetArray | None]]
FillReturn_ChunkCombinedOffsetOffset: TypeAlias = tuple[list[PointArray | None], list[OffsetArray | None], list[OffsetArray | None]]
FillReturn: TypeAlias = FillReturn_OuterCode | FillReturn_OuterOffset | FillReturn_ChunkCombinedCode | FillReturn_ChunkCombinedOffset | FillReturn_ChunkCombinedCodeOffset | FillReturn_ChunkCombinedOffsetOffset

# Types returned from lines()
LineReturn_Separate: TypeAlias = list[PointArray]
LineReturn_SeparateCode: TypeAlias = tuple[list[PointArray], list[CodeArray]]
LineReturn_ChunkCombinedCode: TypeAlias = tuple[list[PointArray | None], list[CodeArray | None]]
LineReturn_ChunkCombinedOffset: TypeAlias = tuple[list[PointArray | None], list[OffsetArray | None]]
LineReturn: TypeAlias = LineReturn_Separate | LineReturn_SeparateCode | LineReturn_ChunkCombinedCode | LineReturn_ChunkCombinedOffset


CONTOURPY_CXX11: int
CONTOURPY_DEBUG: int
__version__: str

class FillType:
    ChunkCombinedCode: ClassVar[contourpy._contourpy.FillType]
    ChunkCombinedCodeOffset: ClassVar[contourpy._contourpy.FillType]
    ChunkCombinedOffset: ClassVar[contourpy._contourpy.FillType]
    ChunkCombinedOffsetOffset: ClassVar[contourpy._contourpy.FillType]
    OuterCode: ClassVar[contourpy._contourpy.FillType]
    OuterOffset: ClassVar[contourpy._contourpy.FillType]
    __members__: ClassVar[dict[str, contourpy._contourpy.FillType]]
    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> NoReturn: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class LineType:
    ChunkCombinedCode: ClassVar[contourpy._contourpy.LineType]
    ChunkCombinedOffset: ClassVar[contourpy._contourpy.LineType]
    Separate: ClassVar[contourpy._contourpy.LineType]
    SeparateCode: ClassVar[contourpy._contourpy.LineType]
    __members__: ClassVar[dict[str, contourpy._contourpy.LineType]]
    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> NoReturn: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

class ZInterp:
    Linear: ClassVar[contourpy._contourpy.ZInterp]
    Log: ClassVar[contourpy._contourpy.ZInterp]
    __members__: ClassVar[dict[str, contourpy._contourpy.ZInterp]]
    def __eq__(self, other: object) -> bool: ...
    def __getstate__(self) -> int: ...
    def __hash__(self) -> int: ...
    def __index__(self) -> int: ...
    def __init__(self, value: int) -> None: ...
    def __int__(self) -> int: ...
    def __ne__(self, other: object) -> bool: ...
    def __repr__(self) -> str: ...
    def __setstate__(self, state: int) -> NoReturn: ...
    @property
    def name(self) -> str: ...
    @property
    def value(self) -> int: ...

def max_threads() -> int: ...

class ContourGenerator:
    def create_contour(self, level: float) -> LineReturn: ...
    def create_filled_contour(self, lower_level: float, upper_level: float) -> FillReturn: ...
    def filled(self, lower_level: float, upper_level: float) -> FillReturn: ...
    def lines(self, level: float) -> LineReturn: ...
    @staticmethod
    def supports_corner_mask() -> bool: ...
    @staticmethod
    def supports_fill_type(fill_type: FillType) -> bool: ...
    @staticmethod
    def supports_line_type(line_type: LineType) -> bool: ...
    @staticmethod
    def supports_quad_as_tri() -> bool: ...
    @staticmethod
    def supports_threads() -> bool: ...
    @staticmethod
    def supports_z_interp() -> bool: ...
    @property
    def chunk_count(self) -> tuple[int, int]: ...
    @property
    def chunk_size(self) -> tuple[int, int]: ...
    @property
    def corner_mask(self) -> bool: ...
    @property
    def fill_type(self) -> FillType: ...
    @property
    def line_type(self) -> LineType: ...
    @property
    def quad_as_tri(self) -> bool: ...
    @property
    def thread_count(self) -> int: ...
    @property
    def z_interp(self) -> ZInterp: ...
    default_fill_type: contourpy._contourpy.FillType
    default_line_type: contourpy._contourpy.LineType

class Mpl2005ContourGenerator(ContourGenerator):
    def __init__(
        self,
        x: CoordinateArray,
        y: CoordinateArray,
        z: CoordinateArray,
        mask: MaskArray,
        *,
        x_chunk_size: int = 0,
        y_chunk_size: int = 0,
    ) -> None: ...

class Mpl2014ContourGenerator(ContourGenerator):
    def __init__(
        self,
        x: CoordinateArray,
        y: CoordinateArray,
        z: CoordinateArray,
        mask: MaskArray,
        *,
        corner_mask: bool,
        x_chunk_size: int = 0,
        y_chunk_size: int = 0,
    ) -> None: ...

class SerialContourGenerator(ContourGenerator):
    def __init__(
        self,
        x: CoordinateArray,
        y: CoordinateArray,
        z: CoordinateArray,
        mask: MaskArray,
        *,
        corner_mask: bool,
        line_type: LineType,
        fill_type: FillType,
        quad_as_tri: bool,
        z_interp: ZInterp,
        x_chunk_size: int = 0,
        y_chunk_size: int = 0,
    ) -> None: ...
    def _write_cache(self) -> NoReturn: ...

class ThreadedContourGenerator(ContourGenerator):
    def __init__(
        self,
        x: CoordinateArray,
        y: CoordinateArray,
        z: CoordinateArray,
        mask: MaskArray,
        *,
        corner_mask: bool,
        line_type: LineType,
        fill_type: FillType,
        quad_as_tri: bool,
        z_interp: ZInterp,
        x_chunk_size: int = 0,
        y_chunk_size: int = 0,
        thread_count: int = 0,
    ) -> None: ...
    def _write_cache(self) -> None: ...
