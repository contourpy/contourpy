import contourpy
from enum import Enum
import io
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import matplotlib.path as mpat
import matplotlib.patches as mpatches
import numpy as np



class PointType(Enum):
    CORNER = 0,
    LOWER = 1,
    UPPER = 2


class Corner(Enum):
    NW = 1,
    NE = 0,
    SW = 3,
    SE = 2


class Config:
    def __init__(self, is_filled):
        self.is_filled = is_filled

        self.arrowsize = 0.1
        self.fontsize = 8
        self.title_fontsize = 9
        self.marker_size = 4
        self.gap = 0.12
        self.text_gap = self.gap/2

        self.default_zlower = 0.5
        self.default_zupper = 1.5

        self.x, self.y = np.meshgrid([0.0, 1.0], [0.0, 1.0])
        self.mask = False

    def _arrow(self, ax, line_start, line_end, color):
        mid = 0.5*(line_start + line_end)
        along = line_end - line_start
        along /= np.sqrt(np.dot(along, along))  # Unit vector.
        right = np.asarray((along[1], -along[0]))
        arrow = np.stack((
            mid - along*0.5*self.arrowsize + right*self.arrowsize,
            mid + along*0.5*self.arrowsize,
            mid - along*0.5*self.arrowsize - right*self.arrowsize))
        ax.plot(arrow[:,0], arrow[:, 1], '-', c=color)

    def _next_quad(self, config, corner=None, suffix='', zlower=None,
                   zupper=None):
        if zlower is None:
            zlower = self.default_zlower
        if zupper is None:
            zupper = self.default_zupper

        ax = self.axes[self.axes_index]
        nw, ne, sw, se = self._decode_config(config, corner)

        # Quad edge.
        ax.axis('off')
        if corner is None:
            ax.plot([0, 1, 1, 0, 0], [0, 0, 1, 1, 0], 'k-', lw=0.25)
            title = f'{nw}{ne}{sw}{se} = {config}{suffix}'
        elif corner == Corner.NW:
            ax.plot([0, 1, 0, 0], [0, 1, 1, 0], 'k-', lw=0.25)
            title = f'{nw}{ne}{sw} = {config}{suffix}'
        elif corner == Corner.NE:
            ax.plot([1, 1, 0, 1], [0, 1, 1, 0], 'k-', lw=0.25)
            title = f'{nw}{ne}{se} = {config}{suffix}'
        elif corner == Corner.SW:
            ax.plot([0, 1, 0, 0], [0, 0, 1, 0], 'k-', lw=0.25)
            title = f'{nw}{sw}{se} = {config}{suffix}'
        elif corner == Corner.SE:
            ax.plot([0, 1, 1, 0], [0, 0, 1, 0], 'k-', lw=0.25)
            title = f'{ne}{sw}{se} = {config}{suffix}'
        else:
            raise RuntimeError('xxx')
        ax.set_title(title, size=self.title_fontsize)

        # Axes bounds include gap for arrows and corner points.
        ax.set_xlim(-self.gap, 1.0+self.gap)
        ax.set_ylim(-self.gap, 1.0+self.gap)

        # Text for corner and optional middle z-levels.
        fontsize = self.fontsize
        if corner != Corner.NW:
            ax.text(1+self.text_gap, 0, se, va='center', size=fontsize, ha='left')
        if corner != Corner.SW:
            ax.text(1+self.text_gap, 1, ne, va='center', size=fontsize, ha='left')
        if corner != Corner.NE:
            ax.text(-self.text_gap, 0, sw, va='center', size=fontsize, ha='right')
        if corner != Corner.SE:
            ax.text(-self.text_gap, 1, nw, va='center', size=fontsize, ha='right')
        if suffix:  # Suffix (without brackets) is the z-level of quad middle.
            ax.text(0.5, 0.5, suffix[1:-1], va='center', size=fontsize,
                    ha='center')

        z = np.asarray([[sw, se], [nw, ne]], dtype=np.float64)
        z = np.ma.array(z, mask=self.mask)
        cont_gen = contourpy.contour_generator(self.x, self.y, z)
        if self.is_filled:
            filled = cont_gen.contour_filled(zlower, zupper)
            lines = filled[0]
        else:
            lines = cont_gen.contour_lines(zlower)

        # May be 0..2 polygons, and there cannot be any holes.
        for points in lines:
            n = len(points)

            if self.is_filled:
                ax.fill(points[:, 0], points[:, 1], c='C2', alpha=0.2, ec=None)

                # Classify points, either corner, lower level or upper level.
                point_types = []
                for i in range(n-1):
                    xy = points[i]
                    if xy[0] in (0.0, 1.0) and xy[1] in (0.0, 1.0):
                        point_types.append(PointType.CORNER)
                    elif not self.is_filled:
                        point_types.append(PointType.LOWER)
                    elif (self._interp(z, xy[0], xy[1], corner) <
                          0.5*(zlower + zupper)):
                        point_types.append(PointType.LOWER)
                    else:
                        point_types.append(PointType.UPPER)
                point_types.append(point_types[0])

                # Draw lines.
                for i in range(n-1):
                    s = points[i]
                    e = points[i+1]
                    c = 'C2'
                    if (point_types[i] == point_types[i+1] and
                        point_types[i] != PointType.CORNER):
                        c = 'C3' if point_types[i] == PointType.LOWER else 'C0'
                    ax.plot([s[0], e[0]], [s[1], e[1]], '-', c=c)

                    if point_types[i] == point_types[i+1]:
                        self._arrow(ax, s, e, c)

                # Draw markers.
                for i in range(n-1):
                    if point_types[i] != PointType.CORNER:
                        c = 'C3' if point_types[i] == PointType.LOWER else 'C0'
                        ax.plot(points[i][0], points[i][1], 'o', c=c,
                                ms=self.marker_size)
            else:
                ax.plot(points[:, 0], points[:, 1], 'o-', c='C3',
                        ms=self.marker_size)

                for i in range(n-1):
                    self._arrow(ax, points[i], points[i+1], 'C3')

        self.axes_index += 1

    def _set_mask(self, corner):
        if corner is None:
            self.mask = False
        else:
            self.mask = np.zeros(4, dtype=bool)
            self.mask[corner.value] = True
            self.mask.shape = (2, 2)

    def save_to_buffer(self):
        buf = io.BytesIO()
        self.fig.savefig(buf, format='png')
        buf.seek(0)
        return buf

    def save_to_file(self, filename):
        self.fig.savefig(filename)


class ConfigFilledCommon(Config):
    def __init__(self):
        super().__init__(True)

    def _decode_config(self, config, corner=None):
        if corner is None:
            nw = (config >> 6) & 0x3
            ne = (config >> 4) & 0x3
            sw = (config >> 2) & 0x3
            se = config & 0x3
        else:
            a = (config >> 4) & 0x3
            b = (config >> 2) & 0x3
            c = config & 0x3
            if corner == Corner.NW:
                [nw, ne, sw, se] = [a, b, c, -1]
            elif corner == Corner.NE:
                [nw, ne, sw, se] = [a, b, -1, c]
            elif corner == Corner.SW:
                [nw, ne, sw, se] = [a, -1, b, c]
            else:  # Corner.SE
                [nw, ne, sw, se] = [-1, a, b, c]
        if nw == 3 or ne == 3 or sw == 3 or se == 3:
            raise ValueError('Invalid config')
        return nw, ne, sw, se

    def _interp(self, zquad, x, y, corner=None):
        # Interpolate zquad to determine value of z at (x, y).  Could use
        # scipy.interp2d for this, but do not want scipy as a dependency just
        # for this.
        # (x, y) must lie on one of the edges of the quad.
        # zquad[0,0] = sw, zquad[0,1] = se, zquad[1,0] = nw, zquad[1,1] = ne
        if x == 0.0:
            return zquad[0, 0]*(1.0-y) + zquad[1, 0]*y
        elif x == 1.0:
            return zquad[0, 1]*(1.0-y) + zquad[1, 1]*y
        elif y == 0.0:
            return zquad[0, 0]*(1.0-x) + zquad[0, 1]*x
        elif y == 1.0:
            return zquad[1, 0]*(1.0-x) + zquad[1, 1]*x
        else:
            # corner is not None
            if corner in (Corner.NW, Corner.SE):
                return zquad[0, 0]*(1.0-y) + zquad[1, 1]*y
            else:
                return zquad[0, 1]*(1.0-y) + zquad[1, 0]*y


class ConfigFilled(ConfigFilledCommon):
    def __init__(self):
        super().__init__()

        self.fig, axes = plt.subplots(8, 12, figsize=(13, 9.8),
                                      subplot_kw={'aspect': 'equal'})
        self.axes = axes.flatten()

        self.axes_index = 0
        for config in range(170):
            try:
                nw, ne, sw, se = self._decode_config(config)
            except ValueError:
                continue

            # A quad is degenerate if all 4 quad edges include either the lower
            # or upper contour levels.
            degenerate_lower = (se == nw == 0 and sw > 0 and ne > 0) or \
                               (sw == ne == 0 and se > 0 and nw > 0)
            degenerate_upper = (se == nw == 2 and sw < 2 and ne < 2) or \
                               (sw == ne == 2 and se < 2 and nw < 2)

            if degenerate_lower and degenerate_upper:
                # middle needs to be 0, 1 and 2.
                self._next_quad(config, suffix='(0)', zlower=1.01)
                self._next_quad(config, suffix='(1)')
                self._next_quad(config, suffix='(2)', zupper=0.99)
            elif degenerate_lower:
                # middle needs to be 0 and >0.
                zmean = np.mean((nw, ne, sw, se))
                zlower = max(self.default_zlower, zmean)
                self._next_quad(config, suffix='(0)', zlower=zlower+0.01)
                self._next_quad(config, suffix='(>0)', zlower=zlower-0.01)
            elif degenerate_upper:
                # middle needs to be <2 and 2.
                zmean = np.mean((nw, ne, sw, se))
                zupper = min(self.default_zupper, zmean)
                self._next_quad(config, suffix='(<2)', zupper=zupper+0.01)
                self._next_quad(config, suffix='(2)', zupper=zupper-0.01)
            else:
                # Not degenerate.
                self._next_quad(config)

        self.fig.tight_layout()


class ConfigFilledCorner(ConfigFilledCommon):
    def __init__(self):
        super().__init__()

        self.fig, axes = plt.subplots(8, 14, figsize=(15, 9.8),
                                      subplot_kw={'aspect': 'equal'})
        self.axes = axes.flatten()

        corners = [Corner.NW, Corner.NE, Corner.SW, Corner.SE]
        self.axes_index = 0
        for icorner in range(4):
            corner = corners[icorner]
            self._set_mask(corner)
            for config in range(43):
                try:
                    _ = self._decode_config(config, corner)
                except ValueError:
                    continue

                self._next_quad(config, corner=corner)

            self.axes[self.axes_index].axis('off')
            self.axes_index += 1

        self.fig.tight_layout()


class ConfigLinesCommon(Config):
    def __init__(self):
        super().__init__(False)

    def _decode_config(self, config, corner=None):
        if corner is None:
            nw = (config >> 3) & 0x1
            ne = (config >> 2) & 0x1
            sw = (config >> 1) & 0x1
            se = config & 0x1
        else:
            a = (config >> 2) & 0x1
            b = (config >> 1) & 0x1
            c = config & 0x1
            if corner == Corner.NW:
                [nw, ne, sw, se] = [a, b, c, -1]
            elif corner == Corner.NE:
                [nw, ne, sw, se] = [a, b, -1, c]
            elif corner == Corner.SW:
                [nw, ne, sw, se] = [a, -1, b, c]
            else:  # Corner.SE
                [nw, ne, sw, se] = [-1, a, b, c]
        return nw, ne, sw, se


class ConfigLines(ConfigLinesCommon):
    def __init__(self):
        super().__init__()

        self.fig, axes = plt.subplots(3, 6, figsize=(6.6, 3.6),
                                      subplot_kw={'aspect': 'equal'})
        self.axes = axes.flatten()

        self.axes_index = 0
        for config in range(16):
            nw, ne, sw, se = self._decode_config(config)

            # A quad is degenerate if all 4 quad edges include the z level.
            degenerate = (se == nw == 0 and sw > 0 and ne > 0) or \
                         (sw == ne == 0 and se > 0 and nw > 0)

            if degenerate:
                zmean = np.mean((nw, ne, sw, se))
                zlower = max(self.default_zlower, zmean)
                self._next_quad(config, suffix='(0)', zlower=zlower+0.01)
                self._next_quad(config, suffix='(1)', zlower=zlower-0.01)
            else:
                self._next_quad(config)

        self.fig.tight_layout()


class ConfigLinesCorner(ConfigLinesCommon):
    # All 4 corners plotted together.
    def __init__(self):
        super().__init__()

        self.fig, axes = plt.subplots(4, 8, figsize=(8.8, 4.9),
                                      subplot_kw={'aspect': 'equal'})
        self.axes = axes.flatten()

        self.axes_index = 0
        corners = [Corner.NW, Corner.NE, Corner.SW, Corner.SE]
        for icorner in range(4):
            corner = corners[icorner]
            self._set_mask(corner)

            for config in range(8):
                self._next_quad(config, corner)

        self.fig.tight_layout()
