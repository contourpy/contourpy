# Force use of Agg backend to render to image file which is required for
# testing on headless servers.  This is used by MplTestRenderer.  All other
# mpl renderer classes switch back to the default interactive backend in their
# constructors.
import matplotlib
_default_backend = matplotlib.get_backend()
matplotlib.use("Agg")

from contourpy import FillType, LineType
from .mpl_util import filled_to_mpl_paths, lines_to_mpl_paths, mpl_codes_to_offsets

import io
import matplotlib.pyplot as plt
import matplotlib.collections as mcollections
import numpy as np


class MplRenderer:
    def __init__(self, nrows=1, ncols=1, figsize=(9, 9)):
        plt.switch_backend(_default_backend)
        self._fig, axes = plt.subplots(
            nrows=nrows, ncols=ncols, figsize=figsize, squeeze=False, sharex=True, sharey=True,
            subplot_kw={"aspect": "equal"})
        self._axes = axes.flatten()

    def __del__(self):
        if hasattr(self, "_fig"):
            plt.close(self._fig)

    def _autoscale(self):
        # Using axes._need_autoscale attribute if need to autoscale before rendering after adding
        # lines/filled.  Only want to autoscale once per axes regardless of how many lines/filled
        # added.
        for ax in self._axes:
            if getattr(ax, "_need_autoscale", False):
                ax.autoscale_view(tight=True)
                ax._need_autoscale = False

    def _get_ax(self, ax):
        if isinstance(ax, int):
            ax = self._axes[ax]
        return ax

    def filled(self, filled, fill_type, ax=0, color="C0", alpha=0.7):
        ax = self._get_ax(ax)
        paths = filled_to_mpl_paths(filled, fill_type)
        collection = mcollections.PathCollection(
            paths, facecolors=color, edgecolors="none", lw=0, alpha=alpha)
        ax.add_collection(collection)
        ax._need_autoscale = True

    def grid(self, x, y, ax=0, color="black", alpha=0.1):
        ax = self._get_ax(ax)
        if x.ndim == 1:
            x, y = np.meshgrid(x, y)
        ax.plot(x, y, x.T, y.T, color=color, alpha=alpha)

    def lines(self, lines, line_type, ax=0, color="C0", alpha=1.0, linewidth=1):
        ax = self._get_ax(ax)
        paths = lines_to_mpl_paths(lines, line_type)
        collection = mcollections.PathCollection(
            paths, facecolors="none", edgecolors=color, lw=linewidth, alpha=alpha)
        ax.add_collection(collection)
        ax._need_autoscale = True

    def save_to_buffer(self):
        self._autoscale()
        buf = io.BytesIO()
        self._fig.savefig(buf, format="png")
        buf.seek(0)
        return buf

    # Save as PNG or SVG.
    def save(self, filename):
        self._autoscale()
        self._fig.savefig(filename)

    def show(self):
        self._autoscale()
        plt.show()

    def title(self, title, ax=0):
        self._get_ax(ax).set_title(title)

    def z_values(self, x, y, z, ax=0, color="green", fmt=".1f"):
        ax = self._get_ax(ax)
        ny, nx = z.shape
        for j in range(ny):
            for i in range(nx):
                ax.text(x[j, i], y[j, i], f"{z[j,i]:{fmt}}", ha="center", va="center",
                        color=color, clip_on=True)


# Test renderer without whitespace around plots and no spines/ticks displayed.
# Uses Agg backend, so can only save to file/buffer, cannot call show().
class MplTestRenderer(MplRenderer):
    def __init__(self, nrows=1, ncols=1, figsize=(9, 9)):
        gridspec = {
            "left": 0.01,
            "right": 0.99,
            "top": 0.99,
            "bottom": 0.01,
            "wspace": 0.01,
            "hspace": 0.01,
        }
        self._fig, axes = plt.subplots(
            nrows=nrows, ncols=ncols, figsize=figsize, squeeze=False, gridspec_kw=gridspec)
        self._axes = axes.flatten()
        for ax in self._axes:
            ax.set_xmargin(0.0)
            ax.set_ymargin(0.0)
            ax.set_xticks([])
            ax.set_yticks([])


class MplDebugRenderer(MplRenderer):
    def __init__(self, nrows=1, ncols=1, figsize=(9, 9)):
        super().__init__(nrows, ncols, figsize)

    def _arrow(self, ax, line_start, line_end, color, alpha, arrow_size):
        mid = 0.5*(line_start + line_end)
        along = line_end - line_start
        along /= np.sqrt(np.dot(along, along))  # Unit vector.
        right = np.asarray((along[1], -along[0]))
        arrow = np.stack((
            mid - (along*0.5 - right)*arrow_size,
            mid + along*0.5*arrow_size,
            mid - (along*0.5 + right)*arrow_size,
        ))
        ax.plot(arrow[:, 0], arrow[:, 1], "-", c=color, alpha=alpha)

    def filled(self, filled, fill_type, ax=0, color="C1", alpha=0.7, line_color="C0",
               point_color="C0", start_point_color="red", arrow_size=0.1):
        super().filled(filled, fill_type, ax, color, alpha)

        if line_color is None and point_color is None:
            return

        ax = self._get_ax(ax)

        if fill_type == FillType.OuterCodes:
            all_points = filled[0]
            all_offsets = [mpl_codes_to_offsets(codes) for codes in filled[1]]
        elif fill_type == FillType.ChunkCombinedCodes:
            all_points = [points for points in filled[0] if points is not None]
            all_offsets = [mpl_codes_to_offsets(codes) for codes in filled[1] if codes is not None]
        elif fill_type == FillType.OuterOffsets:
            all_points = filled[0]
            all_offsets = filled[1]
        elif fill_type == FillType.ChunkCombinedOffsets:
            all_points = [points for points in filled[0] if points is not None]
            all_offsets = [offsets for offsets in filled[1] if offsets is not None]
        elif fill_type == FillType.ChunkCombinedCodesOffsets:
            all_points = []
            all_offsets = []
            for points, codes, outer_offsets in zip(*filled):
                if points is None:
                    continue
                all_points += np.split(points, outer_offsets[1:-1])
                codes = np.split(codes, outer_offsets[1:-1])
                all_offsets += [mpl_codes_to_offsets(codes) for codes in codes]
        elif fill_type == FillType.ChunkCombinedOffsets2:
            all_points = []
            all_offsets = []
            for points, offsets, outer_offsets in zip(*filled):
                if points is None:
                    continue
                for i in range(len(outer_offsets)-1):
                    offs = offsets[outer_offsets[i]:outer_offsets[i+1]+1]
                    all_points.append(points[offs[0]:offs[-1]])
                    all_offsets.append(offs - offs[0])
        else:
            raise RuntimeError(f"Rendering FillType {fill_type} not implemented")

        # Lines.
        if line_color is not None:
            for points, offsets in zip(all_points, all_offsets):
                for start, end in zip(offsets[:-1], offsets[1:]):
                    xys = points[start:end]
                    ax.plot(xys[:, 0], xys[:, 1], c=line_color, alpha=alpha)

                    if arrow_size > 0.0:
                        n = len(xys)
                        for i in range(n-1):
                            self._arrow(ax, xys[i], xys[i+1], line_color, alpha, arrow_size)

        # Points.
        if point_color is not None:
            for points, offsets in zip(all_points, all_offsets):
                mask = np.ones(offsets[-1], dtype=bool)
                mask[offsets[1:]-1] = False  # Exclude end points.
                if start_point_color is not None:
                    start_indices = offsets[:-1]
                    mask[start_indices] = False  # Exclude start points.
                ax.plot(points[:, 0][mask], points[:, 1][mask], "o", c=point_color, alpha=alpha)

                if start_point_color is not None:
                    ax.plot(points[:, 0][start_indices], points[:, 1][start_indices], "o",
                            c=start_point_color, alpha=alpha)

    def lines(self, lines, line_type, ax=0, color="C0", alpha=1.0, linewidth=1, point_color="C0",
              start_point_color="red", arrow_size=0.1):
        super().lines(lines, line_type, ax, color, alpha, linewidth)

        if arrow_size == 0.0 and point_color is None:
            return

        ax = self._get_ax(ax)

        if line_type == LineType.Separate:
            all_lines = lines
        elif line_type == LineType.SeparateCodes:
            all_lines = lines[0]
        elif line_type == LineType.ChunkCombinedCodes:
            all_lines = []
            for points, codes in zip(*lines):
                if points is not None:
                    offsets = mpl_codes_to_offsets(codes)
                    for i in range(len(offsets)-1):
                        all_lines.append(points[offsets[i]:offsets[i+1]])
        elif line_type == LineType.ChunkCombinedOffsets:
            all_lines = []
            for points, offsets in zip(*lines):
                if points is not None:
                    for i in range(len(offsets)-1):
                        all_lines.append(points[offsets[i]:offsets[i+1]])
        else:
            raise RuntimeError(f"Rendering LineType {line_type} not implemented")

        if arrow_size > 0.0:
            for line in all_lines:
                for i in range(len(line)-1):
                    self._arrow(ax, line[i], line[i+1], color, alpha, arrow_size)

        if point_color is not None:
            for line in all_lines:
                start_index = 0
                end_index = len(line)
                if start_point_color is not None:
                    ax.plot(line[0, 0], line[0, 1], "o", c=start_point_color, alpha=alpha)
                    start_index = 1
                    if line[0][0] == line[-1][0] and line[0][1] == line[-1][1]:
                        end_index -= 1
                ax.plot(line[start_index:end_index, 0], line[start_index:end_index, 1], "o",
                        c=color, alpha=alpha)

    def point_numbers(self, x, y, z, ax=0, color="red"):
        ax = self._get_ax(ax)
        ny, nx = z.shape
        for j in range(ny):
            for i in range(nx):
                quad = i + j*nx
                ax.text(x[j, i], y[j, i], str(quad), ha="right", va="top", color=color,
                        clip_on=True)

    def quad_numbers(self, x, y, z, ax=0, color="blue"):
        ax = self._get_ax(ax)
        ny, nx = z.shape
        for j in range(1, ny):
            for i in range(1, nx):
                quad = i + j*nx
                xmid = x[j-1:j+1, i-1:i+1].mean()
                ymid = y[j-1:j+1, i-1:i+1].mean()
                ax.text(xmid, ymid, str(quad), ha="center", va="center", color=color, clip_on=True)

    def z_levels(self, x, y, z, lower_level, upper_level=None, ax=0, color="green"):
        ax = self._get_ax(ax)
        ny, nx = z.shape
        for j in range(ny):
            for i in range(nx):
                zz = z[j, i]
                if upper_level is not None and zz > upper_level:
                    z_level = 2
                elif zz > lower_level:
                    z_level = 1
                else:
                    z_level = 0
                ax.text(x[j, i], y[j, i], z_level, ha="left", va="bottom", color=color,
                        clip_on=True)
