Dechunking
----------

Contour lines and filled contours that are split into multiple chunks can have their chunks combined
using the functions :func:`~.dechunk_lines`, :func:`~.dechunk_filled`,
:func:`~.dechunk_multi_lines` and :func:`~.dechunk_multi_filled`. Line and
fill types that are not split into chunks (``LineType.Separate``, ``LineType.SeparateCode``,
``FillType.OuterCode`` and ``FillType.OuterOffset``) and those that are but only have a single chunk
are returned unmodified by the dechunk functions.

Individual lines and polygons are grouped together into a single chunk, but they remain as separate
lines or polygons; they are not geometrically combined.

As an example, first generate some contour lines that are chunked:

   >>> from contourpy import contour_generator, dechunk_lines
   >>> cont_gen = contour_generator(z=[[0, 1, 0], [0, 1, 0], [0, 0, 0]],
   ...                              line_type="ChunkCombinedOffset", chunk_size=1)
   >>> lines = cont_gen.lines(0.5)
   >>> lines
   ([array([[0.5, 1. ], [0.5, 0. ]]),
     array([[1.5, 0. ], [1.5, 1. ]]),
     array([[1. , 1.5], [0.5, 1. ]]),
     array([[1.5, 1. ], [1. , 1.5]])],
    [array([0, 2], dtype=uint32),
     array([0, 2], dtype=uint32),
     array([0, 2], dtype=uint32),
     array([0, 2], dtype=uint32)])

There are 4 chunks and each contains a single 2-point line. Now call :func:`~.dechunk_lines`:

   >>> lines = dechunk_lines(lines, "ChunkCombinedOffset")
   >>> lines
   ([array([[0.5, 1. ], [0.5, 0. ], [1.5, 0. ], [1.5, 1. ], [1. , 1.5], [0.5, 1. ],
            [1.5, 1. ], [1. , 1.5]])],
    [array([0, 2, 4, 6, 8], dtype=uint32)])

This returns a single chunk containing all 4 lines.

These functions are useful if you want to support the option to generate contours using multiple
chunks, such as to support the ``"threaded"`` algorithm, but your code to process the contours
only supports a single chunk.
