from abc import ABC, abstractmethod

import numpy as np


class Renderer(ABC):
    """Abstract base class for renderers, defining the interface that they must implement."""

    def _grid_as_2d(self, x, y):
        x = np.asarray(x)
        y = np.asarray(y)
        if x.ndim == 1:
            x, y = np.meshgrid(x, y)
        return x, y

    @abstractmethod
    def filled(self, filled, fill_type, ax=0, color="C0", alpha=0.7):
        pass

    @abstractmethod
    def grid(self, x, y, ax=0, color="black", alpha=0.1, point_color=None, quad_as_tri_alpha=0):
        pass

    @abstractmethod
    def lines(self, lines, line_type, ax=0, color="C0", alpha=1.0, linewidth=1):
        pass

    @abstractmethod
    def mask(self, x, y, z, ax=0, color="black"):
        pass

    @abstractmethod
    def save(self, filename, transparent=False):
        pass

    @abstractmethod
    def save_to_buffer(self):
        pass

    @abstractmethod
    def show(self):
        pass

    @abstractmethod
    def title(self, title, ax=0, color=None):
        pass

    @abstractmethod
    def z_values(self, x, y, z, ax=0, color="green", fmt=".1f", quad_as_tri=False):
        pass
