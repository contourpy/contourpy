import io
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import matplotlib.patches as mpatches
import numpy as np


class Renderer:
    def __init__(self, x, y, show_grid=False):
        self.fig = plt.figure(figsize=(9, 9))
        self.ax = self.fig.add_axes([0.01, 0.01, 0.98, 0.98])

        self.ax.set_xlim(x.min(), x.max())
        self.ax.set_ylim(y.min(), y.max())
        self.ax.set_xticks([])
        self.ax.set_yticks([])

        if show_grid:
            self.ax.plot(x, y, 'k-', x.T, y.T, 'k-', alpha=0.1)

    def add_filled(self, filled, color='C0', alpha=0.7):
        for points, codes in zip(filled[0], filled[1]):
            path = mpath.Path(points, codes)
            patch = mpatches.PathPatch(path, facecolor=color, lw=0, alpha=alpha)
            self.ax.add_patch(patch)

    def add_lines(self, lines, color='C0', alpha=1.0):
        for line in lines:
            # Drawing as Paths so that they can be closed correctly.
            closed = np.array_equal(line[0], line[-1])
            path = mpath.Path(line, closed=closed)
            patch = mpatches.PathPatch(path, facecolor='none', lw=1, ec=color,
                                       alpha=alpha, capstyle='round')
            self.ax.add_patch(patch)

    def save(self, filename):
        self.fig.savefig(filename)

    def save_to_buffer(self):
        buf = io.BytesIO()
        self.fig.savefig(buf, format='png')
        buf.seek(0)
        return buf
