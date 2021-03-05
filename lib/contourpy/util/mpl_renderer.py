# Force use of Agg backend to render to image file which is required for
# testing on headless servers.  This is used by MplTestRenderer.  All other
# mpl renderer classes switch back to the default interactive backend in their
# constructors.
import matplotlib
_default_backend = matplotlib.get_backend()
matplotlib.use('Agg')

import io
import matplotlib.pyplot as plt
import matplotlib.collections as mcollections
import matplotlib.path as mpath
import numpy as np


class MplRenderer:
    def __init__(self, nrows=1, ncols=1, figsize=(9, 9)):
        plt.switch_backend(_default_backend)
        self.fig, axes = plt.subplots(
            nrows=nrows, ncols=ncols, figsize=figsize, squeeze=False,
            sharex=True, sharey=True, subplot_kw={'aspect': 'equal'})
        self.axes = axes.flatten()

    def _get_ax(self, ax):
        if isinstance(ax, int):
            ax = self.axes[ax]
        return ax

    def filled(self, filled, ax=0, color='C0', alpha=0.7):
        ax = self._get_ax(ax)
        paths = [mpath.Path(points, codes) for points, codes
                 in zip(filled[0], filled[1])]
        collection = mcollections.PathCollection(
            paths, facecolors=color, edgecolors='none', lw=0, alpha=alpha)
        ax.add_collection(collection)

    def grid(self, x, y, ax=0, color='k', alpha=0.1):
        ax = self._get_ax(ax)
        ax.plot(x, y, x.T, y.T, color=color, alpha=alpha)

    def lines(self, lines, ax=0, color='C0', alpha=1.0):
        ax = self._get_ax(ax)
        paths = []
        for line in lines:
            # Drawing as Paths so that they can be closed correctly.
            closed = line[0, 0] == line[-1, 0] and line[0, 1] == line[-1, 1]
            paths.append(mpath.Path(line, closed=closed))
        collection = mcollections.PathCollection(
            paths, facecolors='none', edgecolors=color, lw=1, alpha=alpha)
        ax.add_collection(collection)

    def save_to_buffer(self):
        buf = io.BytesIO()
        self.fig.savefig(buf, format='png')
        buf.seek(0)
        return buf

    def show(self):
        plt.show()

    def title(self, ax, title):
        self._get_ax(ax).set_title(title)


# Test renderer without whitespace around plots or spines/ticks displayed.
class MplTestRenderer(MplRenderer):
    def __init__(self, x, y, nrows=1, ncols=1, figsize=(9, 9)):
        gridspec = {'left': 0.01, 'right': 0.99, 'top': 0.99, 'bottom': 0.01,
                    'wspace': 0.01, 'hspace': 0.01}
        self.fig, axes = plt.subplots(
            nrows=nrows, ncols=ncols, figsize=figsize, squeeze=False,
            gridspec_kw=gridspec)
        self.axes = axes.flatten()

        xlim = (x.min(), x.max())
        ylim = (y.min(), y.max())

        for ax in self.axes:
            ax.set_xlim(xlim)
            ax.set_ylim(ylim)
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
            mid - (along*0.5 + right)*arrow_size))
        ax.plot(arrow[:,0], arrow[:, 1], '-', c=color, alpha=alpha)

    def filled(self, filled, ax=0, color='C1', alpha=0.7, line_color='C0',
               point_color='C0', start_point_color='red', arrow_size=0.1):
        super().filled(filled, ax, color, alpha)

        ax = self._get_ax(ax)

        # Lines.
        if line_color is not None:
            for points, codes in zip(filled[0], filled[1]):
                starts = np.append(np.nonzero(codes == 1)[0], len(codes))
                for start, end in zip(starts[:-1], starts[1:]):
                    xys = points[start:end]
                    ax.plot(xys[:, 0], xys[:, 1], c=line_color, alpha=alpha)

                    if arrow_size > 0.0:
                        n = len(xys)
                        for i in range(n-1):
                            self._arrow(ax, xys[i], xys[i+1], line_color, alpha,
                                        arrow_size)

        # Points.
        if point_color is not None:
            for points, codes in zip(filled[0], filled[1]):
                if start_point_color is not None:
                    mask = (codes == 2)
                else:
                    mask = (codes != 79)
                ax.plot(points[:, 0][mask], points[:, 1][mask], 'o',
                        c=point_color, alpha=alpha)

                if start_point_color is not None:
                    mask = (codes == 1)
                    ax.plot(points[:, 0][mask], points[:, 1][mask], 'o',
                            c=start_point_color, alpha=alpha)

    def point_numbers(self, x, y, z, ax=0, color='red'):
        ax = self._get_ax(ax)
        ny, nx = z.shape
        for j in range(ny):
            for i in range(nx):
                quad = i + j*nx
                ax.text(x[j, i], y[j, i], str(quad), ha='right', va='top',
                        color=color, clip_on=True)

    def quad_numbers(self, x, y, z, ax=0, color='blue'):
        ax = self._get_ax(ax)
        ny, nx = z.shape
        for j in range(1, ny):
            for i in range(1, nx):
                quad = i + j*nx
                xmid = x[j-1:j+1, i-1:i+1].mean()
                ymid = y[j-1:j+1, i-1:i+1].mean()
                ax.text(xmid, ymid, str(quad), ha='center', va='center',
                        color=color, clip_on=True)

    def z_levels(self, x, y, z, lower_level, upper_level, ax=0, color='green'):
        ax = self._get_ax(ax)
        ny, nx = z.shape
        for j in range(1, ny):
            for i in range(1, nx):
                zz = z[j,i]
                if zz > upper_level:
                    z_level = 2
                elif zz > lower_level:
                    z_level = 1
                else:
                    z_level = 0
                ax.text(x[j, i], y[j, i], z_level, ha='left', va='bottom',
                        color=color, clip_on=True)

