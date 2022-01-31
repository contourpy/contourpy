from bokeh.io import export_png, export_svg, show
from bokeh.io.export import get_screenshot_as_png
from bokeh.layouts import gridplot
from bokeh.models import Label
from bokeh.palettes import Category10
from bokeh.plotting import figure
import io
import numpy as np

from .bokeh_util import filled_to_bokeh, lines_to_bokeh


class BokehRenderer:
    def __init__(self, nrows=1, ncols=1, figsize=(9, 9), show_frame=True, want_svg=False):
        self._want_svg = want_svg
        self._palette = Category10[10]

        total_size = 100*np.asarray(figsize)  # Assuming 100 dpi.

        nfigures = nrows*ncols
        self._figures = []
        backend = "svg" if self._want_svg else "canvas"
        for _ in range(nfigures):
            fig = figure(output_backend=backend)
            fig.xgrid.visible = False
            fig.ygrid.visible = False
            self._figures.append(fig)
            if not show_frame:
                fig.outline_line_color = None
                fig.axis.visible = False

        self._layout = gridplot(
            self._figures, ncols=ncols, toolbar_location=None,
            width=total_size[0] // ncols, height=total_size[1] // nrows)

    def _convert_color(self, color):
        if isinstance(color, str) and color[0] == "C":
            index = int(color[1:])
            color = self._palette[index]
        return color

    def _get_figure(self, ax):
        if isinstance(ax, int):
            ax = self._figures[ax]
        return ax

    def _grid_as_2d(self, x, y):
        x = np.asarray(x)
        y = np.asarray(y)
        if x.ndim == 1:
            x, y = np.meshgrid(x, y)
        return x, y

    def filled(self, filled, fill_type, ax=0, color="C0", alpha=0.7):
        fig = self._get_figure(ax)
        color = self._convert_color(color)
        xs, ys = filled_to_bokeh(filled, fill_type)
        if len(xs) > 0:
            fig.multi_polygons(xs=[xs], ys=[ys], color=color, fill_alpha=alpha, line_width=0)

    def grid(self, x, y, ax=0, color="black", alpha=0.1, point_color=None, quad_as_tri_alpha=0):
        fig = self._get_figure(ax)
        x, y = self._grid_as_2d(x, y)
        xs = [row for row in x] + [row for row in x.T]
        ys = [row for row in y] + [row for row in y.T]
        kwargs = dict(line_color=color, alpha=alpha)
        fig.multi_line(xs, ys, **kwargs)
        if quad_as_tri_alpha > 0:
            # Assumes no quad mask.
            xmid = (0.25*(x[:-1, :-1] + x[1:, :-1] + x[:-1, 1:] + x[1:, 1:])).ravel()
            ymid = (0.25*(y[:-1, :-1] + y[1:, :-1] + y[:-1, 1:] + y[1:, 1:])).ravel()
            fig.multi_line(
                [row for row in np.stack((x[:-1, :-1].ravel(), xmid, x[1:, 1:].ravel()), axis=1)],
                [row for row in np.stack((y[:-1, :-1].ravel(), ymid, y[1:, 1:].ravel()), axis=1)],
                **kwargs)
            fig.multi_line(
                [row for row in np.stack((x[:-1, 1:].ravel(), xmid, x[1:, :-1].ravel()), axis=1)],
                [row for row in np.stack((y[:-1, 1:].ravel(), ymid, y[1:, :-1].ravel()), axis=1)],
                **kwargs)
        if point_color is not None:
            fig.circle(
                x=x.ravel(), y=y.ravel(), fill_color=color, line_color=None, alpha=alpha, size=8)

    def lines(self, lines, line_type, ax=0, color="C0", alpha=1.0, linewidth=1):
        # Assumes all lines are open line loops.
        fig = self._get_figure(ax)
        color = self._convert_color(color)
        xs, ys = lines_to_bokeh(lines, line_type)
        if len(xs) > 0:
            fig.multi_line(xs, ys, line_color=color, line_alpha=alpha, line_width=linewidth)

    def save(self, filename):
        if self._want_svg:
            export_svg(self._layout, filename=filename)
        else:
            export_png(self._layout, filename=filename)

    def save_to_buffer(self):
        image = get_screenshot_as_png(self._layout)
        buffer = io.BytesIO()
        image.save(buffer, "png")
        return buffer

    def show(self):
        show(self._layout)

    def title(self, title, ax=0, color=None):
        fig = self._get_figure(ax)
        fig.title = title
        fig.title.align = "center"
        if color is not None:
            fig.title.text_color = self._convert_color(color)

    def z_values(self, x, y, z, ax=0, color="green", fmt=".1f", quad_as_tri=False):
        fig = self._get_figure(ax)
        color = self._convert_color(color)
        x, y = self._grid_as_2d(x, y)
        z = np.asarray(z)
        ny, nx = z.shape
        kwargs = dict(text_color=color, text_align="center", text_baseline="middle")
        for j in range(ny):
            for i in range(nx):
                fig.add_layout(Label(x=x[j, i], y=y[j, i], text=f"{z[j, i]:{fmt}}", **kwargs))
        if quad_as_tri:
            for j in range(ny-1):
                for i in range(nx-1):
                    xx = np.mean(x[j:j+2, i:i+2])
                    yy = np.mean(y[j:j+2, i:i+2])
                    zz = np.mean(z[j:j+2, i:i+2])
                    fig.add_layout(Label(x=xx, y=yy, text=f"{zz:{fmt}}", **kwargs))
