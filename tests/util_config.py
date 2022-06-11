from enum import Enum
import io

import matplotlib.pyplot as plt
import numpy as np

from contourpy import LineType, contour_generator


class PointType(Enum):
    CORNER = 0
    LOWER = 1
    UPPER = 2


class Corner(Enum):
    NW = 1
    NE = 0
    SW = 3
    SE = 2


class Config:
    def __init__(self, name, is_filled, corner_mask, quad_as_tri, show_text):
        self.name = name
        self.is_filled = is_filled
        self.corner_mask = corner_mask
        self.quad_as_tri = quad_as_tri
        self.show_text = show_text

        self.arrowsize = 0.1
        self.fontsize = 8
        self.title_fontsize = 8
        self.marker_size = 3.5
        self.gap = 0.1
        self.text_gap = self.gap/2
        self.grid_kwargs = dict(color="lightgray", linewidth=1)

        self.x, self.y = np.meshgrid([0.0, 1.0], [0.0, 1.0])
        self.mask = False

        # Set in derived classes.
        self.fig = None
        self.axes = None

        import matplotlib
        matplotlib.use("Agg")

    def __del__(self):
        if self.fig:
            plt.close(self.fig)

    def _arrow(self, ax, line_start, line_end, color):
        mid = 0.5*(line_start + line_end)
        along = line_end - line_start
        along /= np.sqrt(np.dot(along, along))  # Unit vector.
        right = np.asarray((along[1], -along[0]))
        arrow = np.stack((
            mid - (along*0.5 - right)*self.arrowsize,
            mid + along*0.5*self.arrowsize,
            mid - (along*0.5 + right)*self.arrowsize))
        ax.plot(arrow[:, 0], arrow[:, 1], "-", c=color)

    def _next_quad(self, config, corner=None, suffix="", set_0=0, set_1=1, set_2=2):
        zlower = 0.5
        zupper = 1.5

        ax = self.axes[self.axes_index]
        nw, ne, sw, se = self._decode_config(config, corner)

        # Quad edge.
        ax.axis("off")
        if corner is None:
            ax.plot([0, 1, 1, 0, 0], [0, 0, 1, 1, 0], **self.grid_kwargs)
            if self.quad_as_tri and not nw == ne == sw == se:
                ax.plot([0, 1], [0, 1], [0, 1], [1, 0], **self.grid_kwargs)
            title = f"{nw}{ne}{sw}{se}={config}{suffix}"
        elif corner == Corner.NW:
            ax.plot([0, 1, 0, 0], [0, 1, 1, 0], **self.grid_kwargs)
            title = f"{nw}{ne}{sw}={config}{suffix}"
        elif corner == Corner.NE:
            ax.plot([1, 1, 0, 1], [0, 1, 1, 0], **self.grid_kwargs)
            title = f"{nw}{ne}{se}={config}{suffix}"
        elif corner == Corner.SW:
            ax.plot([0, 1, 0, 0], [0, 0, 1, 0], **self.grid_kwargs)
            title = f"{nw}{sw}{se}={config}{suffix}"
        elif corner == Corner.SE:
            ax.plot([0, 1, 1, 0], [0, 0, 1, 0], **self.grid_kwargs)
            title = f"{ne}{sw}{se}={config}{suffix}"
        else:
            raise RuntimeError("Invalid corner")

        if self.show_text:
            ax.set_title(title, size=self.title_fontsize)

        # Axes bounds include gap for arrows and corner points.
        ax.set_xlim(-self.gap, 1.0+self.gap)
        ax.set_ylim(-self.gap, 1.0+self.gap)

        if self.show_text:
            # Text for corner and optional middle z-levels.
            fontsize = self.fontsize
            if corner != Corner.NW:
                ax.text(1+self.text_gap, 0, se, va="center", size=fontsize, ha="left")
            if corner != Corner.SW:
                ax.text(1+self.text_gap, 1, ne, va="center", size=fontsize, ha="left")
            if corner != Corner.NE:
                ax.text(-self.text_gap, 0, sw, va="center", size=fontsize, ha="right")
            if corner != Corner.SE:
                ax.text(-self.text_gap, 1, nw, va="center", size=fontsize, ha="right")
            if suffix:  # Suffix (without brackets) is the z-level of quad middle.
                ax.text(0.5, 0.5, suffix[1:-1], va="center", size=fontsize, ha="center")

        lookup = {0: set_0, 1: set_1, 2: set_2, None: None}
        nw = lookup[nw]
        ne = lookup[ne]
        sw = lookup[sw]
        se = lookup[se]

        if suffix:
            zmean = np.mean((nw, ne, sw, se))
            if suffix == "(0)":
                if zmean > zlower:
                    raise RuntimeError(
                        f"Inconsistent zlower {zlower} for config {config}{suffix} with middle_z "
                        f"{zmean}")
            elif suffix in ["(1)", "(>0)", "(<2)"]:
                if zmean < zlower:
                    raise RuntimeError(
                        f"Inconsistent zlower {zlower} for config {config}{suffix} with middle_z "
                        f"{zmean}")
                elif zmean > zupper:
                    raise RuntimeError(
                        f"Inconsistent zupper {zupper} for config {config}{suffix} with middle_z "
                        f"{zmean}")
            elif suffix == "(2)":
                if zmean < zupper:
                    raise RuntimeError(
                        f"Inconsistent zupper {zupper} for config {config}{suffix} with middle_z "
                        f"{zmean}")
            elif suffix != "":
                raise RuntimeError(f"Unexpected suffix {suffix} for config {config}")

        z = np.asarray([[sw, se], [nw, ne]], dtype=np.float64)
        z = np.ma.array(z, mask=self.mask)
        cont_gen = contour_generator(
            self.x, self.y, z, name=self.name, corner_mask=self.corner_mask,
            quad_as_tri=self.quad_as_tri)
        if self.is_filled:
            filled = cont_gen.filled(zlower, zupper)
            lines = filled[0]
        else:
            lines = cont_gen.lines(zlower)
            if cont_gen.line_type == LineType.SeparateCode:
                lines = lines[0]

        # May be 0..2 polygons, and there cannot be any holes.
        for points in lines:
            n = len(points)

            if self.is_filled:
                ax.fill(points[:, 0], points[:, 1], c="C2", alpha=0.2, ec=None)

                # Classify points, either corner, lower level or upper level.
                point_types = []
                for i in range(n-1):
                    xy = points[i]
                    x_on_quad_edge = (xy[0] in (0.0, 1.0))
                    y_on_quad_edge = (xy[1] in (0.0, 1.0))
                    if x_on_quad_edge and y_on_quad_edge:
                        point_types.append(PointType.CORNER)
                    elif not self.is_filled:
                        point_types.append(PointType.LOWER)
                    elif corner is not None or x_on_quad_edge or y_on_quad_edge:
                        if (self._interp(z, xy[0], xy[1], corner) < 0.5*(zlower + zupper)):
                            point_types.append(PointType.LOWER)
                        else:
                            point_types.append(PointType.UPPER)
                    else:
                        # Point on quad diagonal from middle point, so same type as previous point.
                        point_types.append(point_types[-1])
                # End point is the same as the start point.
                point_types.append(point_types[0])

                # Draw lines.
                for i in range(n-1):
                    s = points[i]
                    e = points[i+1]
                    c = "C2"
                    if point_types[i] == point_types[i+1] and point_types[i] != PointType.CORNER:
                        c = "C3" if point_types[i] == PointType.LOWER else "C0"
                    ax.plot([s[0], e[0]], [s[1], e[1]], "-", c=c)

                    # Arrows on boundary and contour levels (the latter only if not quad_as_tri).
                    if point_types[i] == point_types[i+1] and (
                            point_types[i] == PointType.CORNER or not self.quad_as_tri):
                        self._arrow(ax, s, e, c)

                # Arrows on contour levels (lower and upper) for quad_as_tri.  Only want a single
                # arrow on each line strip, so find and use the longest line segment.  Care needed
                # identifying the longest due to rounding error, so find all segments within a small
                # length of the longest and take the max index of these.
                if self.quad_as_tri:
                    for point_type in [PointType.LOWER, PointType.UPPER]:
                        mask = np.equal(point_types, point_type)
                        start_indices = np.nonzero(np.logical_and(mask[1:], ~mask[:-1]))[0]
                        for start_index in start_indices:
                            start_index = (start_index + 1) % (n-1)

                            # Roll point_types array so start segment of line strip is at front.
                            rolled = np.roll(point_types[:-1], -start_index)
                            end_offset = np.nonzero(rolled != point_type)[0][0]

                            pts = points[start_index:start_index+end_offset]  # Line strip points.
                            diff = np.diff(pts, axis=0)
                            lengths = np.sum(np.square(diff), axis=1)  # Segment lengths.
                            offset = np.nonzero(lengths > lengths.max() - 1e-6)[0].max()

                            i = (start_index + offset) % (n-1)
                            c = "C3" if point_type == PointType.LOWER else "C0"
                            self._arrow(ax, points[i], points[i+1], c)

                # Draw markers.
                for i in range(n-1):
                    if point_types[i] != PointType.CORNER:
                        c = "C3" if point_types[i] == PointType.LOWER else "C0"
                        ax.plot(points[i][0], points[i][1], "o", c=c, ms=self.marker_size)
            else:
                ax.plot(points[:, 0], points[:, 1], "o-", c="C3", ms=self.marker_size)

                # Single arrow in middle segment (if even number of points) or the following
                # segment (if odd number of points).
                i = (n-1) // 2
                self._arrow(ax, points[i], points[i+1], "C3")

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
        self.fig.savefig(buf, format="png")
        buf.seek(0)
        return buf

    def save_to_file(self, filename):
        self.fig.savefig(filename)


class ConfigFilledCommon(Config):
    def __init__(self, name, corner_mask, quad_as_tri, show_text):
        super().__init__(name, True, corner_mask, quad_as_tri, show_text)

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
                [nw, ne, sw, se] = [a, b, c, None]
            elif corner == Corner.NE:
                [nw, ne, sw, se] = [a, b, None, c]
            elif corner == Corner.SW:
                [nw, ne, sw, se] = [a, None, b, c]
            else:  # Corner.SE
                [nw, ne, sw, se] = [None, a, b, c]
        if nw == 3 or ne == 3 or sw == 3 or se == 3:
            raise ValueError("Invalid config")
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
    def __init__(self, name, quad_as_tri=False, show_text=True):
        super().__init__(name, False, quad_as_tri, show_text)

        subplot_kw = dict(aspect="equal")
        if self.quad_as_tri:
            self.fig, axes = plt.subplots(18, 12, figsize=(10.4, 17.1), subplot_kw=subplot_kw)
        else:
            self.fig, axes = plt.subplots(9, 11, figsize=(9.4, 8.4), subplot_kw=subplot_kw)
        self.axes = axes.flatten()

        self.axes_index = 0
        for config in range(171):
            try:
                (nw, ne, sw, se) = all = self._decode_config(config)
            except ValueError:
                continue

            # A quad is degenerate if all 4 quad edges include either the lower
            # or upper contour levels.
            degenerate_lower = (se == nw == 0 and sw > 0 and ne > 0) or \
                               (sw == ne == 0 and se > 0 and nw > 0)
            degenerate_upper = (se == nw == 2 and sw < 2 and ne < 2) or \
                               (sw == ne == 2 and se < 2 and nw < 2)

            if self.quad_as_tri:
                if not nw == ne == sw == se:
                    zmax = max(all)
                    zmin = min(all)
                    zsum = np.sum(all)
                    all = np.asarray(all)
                    if zmin == 0 and zmax == 1:
                        lookup_0 = {1: 0, 2: -1, 3: -1.8}
                        self._next_quad(config, suffix="(0)", set_0=lookup_0[zsum])

                        lookup_1 = {1: 0.4, 2: 0.35, 3: 0}
                        self._next_quad(config, suffix="(1)", set_0=lookup_1[zsum])
                    elif zmin == 0 and zmax == 2:
                        count_1 = np.count_nonzero(all == 1)
                        lookup_0 = {2: -0.3, 3: -1, 4: -2-count_1/2, 5: -5, 6: -6}
                        self._next_quad(config, suffix="(0)", set_0=lookup_0[zsum])

                        if zsum <= 3:
                            self._next_quad(config, suffix="(1)", set_2=3.01)
                        elif zsum <= 5:
                            self._next_quad(config, suffix="(1)")
                        elif zsum == 6:
                            self._next_quad(config, suffix="(1)", set_0=-1)

                        lookup_2 = {2: 8.01, 3: 7.01, 4: 4+count_1/2, 5: 3.5, 6: 2.5}
                        self._next_quad(config, suffix="(2)", set_2=lookup_2[zsum])
                    elif zmin == 1 and zmax == 2:
                        lookup_1 = {5: 2, 6: 1.65, 7: 1.6}
                        self._next_quad(config, suffix="(1)", set_2=lookup_1[zsum])

                        lookup_2 = {5: 4, 6: 3, 7: 2}
                        self._next_quad(config, suffix="(2)", set_2=lookup_2[zsum])
                    else:
                        raise RuntimeError(f"Invalid combination of zmin {zmin} and zmax {zmax}")
                else:
                    self._next_quad(config)
            else:  # !quad_as_tri
                if degenerate_lower and degenerate_upper:
                    # middle needs to be 0, 1 and 2.
                    self._next_quad(config, suffix="(0)", set_0=-1.01)
                    self._next_quad(config, suffix="(1)")
                    self._next_quad(config, suffix="(2)", set_2=3.01)
                elif degenerate_lower:
                    # middle needs to be 0 and >0.
                    self._next_quad(config, suffix="(0)", set_0=-0.01 if max(all) == 1 else -0.51)
                    self._next_quad(config, suffix="(>0)", set_1=1.01)
                elif degenerate_upper:
                    # middle needs to be <2 and 2.
                    self._next_quad(config, suffix="(<2)")
                    self._next_quad(config, suffix="(2)", set_2=2.01 if min(all) == 1 else 2.51)
                else:
                    # Not degenerate.
                    self._next_quad(config)

        # Hide unwanted axes.
        for i in range(self.axes_index, len(self.axes)):
            self.axes[i].axis("off")

        self.fig.tight_layout()


class ConfigFilledCorner(ConfigFilledCommon):
    def __init__(self, name, show_text=True):
        super().__init__(name, corner_mask=True, quad_as_tri=False, show_text=show_text)

        self.fig, axes = plt.subplots(8, 14, figsize=(12.1, 7.6), subplot_kw={"aspect": "equal"})
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

            self.axes[self.axes_index].axis("off")
            self.axes_index += 1

        self.fig.tight_layout()


class ConfigLinesCommon(Config):
    def __init__(self, name, corner_mask, quad_as_tri, show_text):
        super().__init__(name, False, corner_mask, quad_as_tri, show_text)

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
                [nw, ne, sw, se] = [a, b, c, None]
            elif corner == Corner.NE:
                [nw, ne, sw, se] = [a, b, None, c]
            elif corner == Corner.SW:
                [nw, ne, sw, se] = [a, None, b, c]
            else:  # Corner.SE
                [nw, ne, sw, se] = [None, a, b, c]
        return nw, ne, sw, se


class ConfigLines(ConfigLinesCommon):
    def __init__(self, name, quad_as_tri=False, show_text=True):
        super().__init__(name, False, quad_as_tri, show_text)

        subplot_kw = dict(aspect="equal")
        if self.quad_as_tri:
            self.fig, axes = plt.subplots(5, 6, figsize=(5.2, 4.75), subplot_kw=subplot_kw)
        else:
            self.fig, axes = plt.subplots(3, 6, figsize=(5.2, 2.85), subplot_kw=subplot_kw)
        self.axes = axes.flatten()

        self.axes_index = 0
        for config in range(16):
            (nw, ne, sw, se) = all = self._decode_config(config)

            # A quad is degenerate if all 4 quad edges include the z level.
            degenerate = (se == nw == 0 and sw > 0 and ne > 0) or \
                         (sw == ne == 0 and se > 0 and nw > 0)

            if degenerate or (self.quad_as_tri and not nw == ne == sw == se):
                if self.quad_as_tri:
                    count_1 = np.count_nonzero(all)
                    count_0 = 4 - count_1
                    self._next_quad(config, suffix="(0)", set_0=1.01 - count_1)
                    self._next_quad(config, suffix="(1)", set_1=0.01 + count_0)
                else:
                    self._next_quad(config, suffix="(0)", set_1=0.99)
                    self._next_quad(config, suffix="(1)", set_1=1.01)
            else:
                self._next_quad(config)

        self.fig.tight_layout()


class ConfigLinesCorner(ConfigLinesCommon):
    # All 4 corners plotted together.
    def __init__(self, name, show_text=True):
        super().__init__(name, corner_mask=True, quad_as_tri=False, show_text=show_text)

        self.fig, axes = plt.subplots(4, 8, figsize=(6.93, 3.8), subplot_kw={"aspect": "equal"})
        self.axes = axes.flatten()

        self.axes_index = 0
        corners = [Corner.NW, Corner.NE, Corner.SW, Corner.SE]
        for icorner in range(4):
            corner = corners[icorner]
            self._set_mask(corner)

            for config in range(8):
                self._next_quad(config, corner)

        self.fig.tight_layout()
