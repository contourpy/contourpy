from contourpy import FillType, LineType
from .mpl_util import mpl_codes_to_offsets

from bokeh.io import export_png, export_svg
from bokeh.layouts import gridplot
from bokeh.palettes import Category10
from bokeh.plotting import figure
import numpy as np


class BokehRenderer:
    def __init__(self, nrows=1, ncols=1, figsize=(9, 9), want_svg=False):
        self._want_svg = want_svg
        self._palette = Category10[10]

        total_size = 100*np.asarray(figsize)

        nfigures = nrows*ncols
        self._figures = []
        backend = 'svg' if self._want_svg else 'canvas'
        for i in range(nfigures):
            fig = figure(output_backend=backend)
            fig.xgrid.visible = False
            fig.ygrid.visible = False
            self._figures.append(fig)

        self._layout = gridplot(
            self._figures, ncols=ncols, toolbar_location=None,
            plot_width=total_size[0] // ncols,
            plot_height=total_size[1] // nrows)

    def _convert_color(self, color):
        if isinstance(color, str) and color[0] == 'C':
            index = int(color[1:])
            color = self._palette[index]
        return color

    def _get_figure(self, ax):
        if isinstance(ax, int):
            ax = self._figures[ax]
        return ax

    def filled(self, filled, fill_type, ax=0, color='C0', alpha=0.7):
        fig = self._get_figure(ax)
        color = self._convert_color(color)
        xs = []
        ys = []

        if fill_type in (FillType.OuterOffsets, FillType.ChunkCombinedOffsets,
                         FillType.OuterCodes, FillType.ChunkCombinedCodes):
            have_codes = \
                fill_type in (FillType.OuterCodes,
                              FillType.ChunkCombinedCodes)

            for points, offsets in zip(*filled):
                if points is None:
                    continue
                if have_codes:
                    offsets = mpl_codes_to_offsets(offsets)
                xs.append([])  # New outer with zero or more holes.
                ys.append([])
                for i in range(len(offsets)-1):
                    xys = points[offsets[i]:offsets[i+1]]
                    xs[-1].append(xys[:, 0])
                    ys[-1].append(xys[:, 1])
        elif fill_type in (FillType.ChunkCombinedCodesOffsets,
                           FillType.ChunkCombinedOffsets2):
            for points, codes_or_offsets, outer_offsets in zip(*filled):
                if points is None:
                    continue
                for j in range(len(outer_offsets)-1):
                    if fill_type == FillType.ChunkCombinedCodesOffsets:
                        codes = codes_or_offsets[outer_offsets[j]:
                                                 outer_offsets[j+1]]
                        offsets = mpl_codes_to_offsets(codes) + outer_offsets[j]
                    else:
                        offsets = codes_or_offsets[outer_offsets[j]:
                                                   outer_offsets[j+1]+1]
                    xs.append([])  # New outer with zero or more holes.
                    ys.append([])
                    for k in range(len(offsets)-1):
                        xys = points[offsets[k]:offsets[k+1]]
                        xs[-1].append(xys[:, 0])
                        ys[-1].append(xys[:, 1])
        else:
            raise RuntimeError(f'Rendering FillType {fill_type} not implemented')

        if len(xs) > 0:
            fig.multi_polygons(
                xs=[xs], ys=[ys], color=color, fill_alpha=alpha, line_width=0)

    def grid(self, x, y, ax=0, color='black', alpha=0.1):
        fig = self._get_figure(ax)

        if x.ndim == 1:
            x, y = np.meshgrid(x, y)

        xs = [row for row in x] + [row for row in x.T]
        ys = [row for row in y] + [row for row in y.T]
        fig.multi_line(xs, ys, line_color=color, alpha=alpha)

    def lines(self, lines, line_type, ax=0, color='C0', alpha=1.0,
              linewidth=1):
        # Assumes all lines are open line loops.
        fig = self._get_figure(ax)
        color = self._convert_color(color)
        xs = []
        ys = []

        if line_type == LineType.Separate:
            for line in lines:
                xs.append(line[:, 0])
                ys.append(line[:, 1])
        elif line_type == LineType.SeparateCodes:
            for line in lines[0]:
                xs.append(line[:, 0])
                ys.append(line[:, 1])
        elif line_type in (LineType.ChunkCombinedCodes,
                           LineType.ChunkCombinedOffsets):
            for points, offsets in zip(*lines):
                if points is None:
                    continue
                if line_type == LineType.ChunkCombinedCodes:
                    offsets = mpl_codes_to_offsets(offsets)

                for i in range(len(offsets)-1):
                    line = points[offsets[i]:offsets[i+1]]
                    xs.append(line[:, 0])
                    ys.append(line[:, 1])
        else:
            raise RuntimeError(f'Rendering LineType {line_type} not implemented')

        if len(xs) > 0:
            fig.multi_line(xs, ys, line_color=color, line_alpha=alpha,
                           line_width=linewidth)

    def save(self, filename):
        if self._want_svg:
            export_svg(self._layout, filename=filename)
        else:
            export_png(self._layout, filename=filename)

    def title(self, title, ax=0):
        self._get_figure(ax).title = title
