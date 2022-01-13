from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
from .color import Color


class ColorMap(object):
    """Class providing a map for colors of a specific color palette.

    Parameters
    ----------
    colors : sequence[tuple[float, float, float]]
        A sequence of colors forming the map.

    Attributes
    ----------
    colors : list[:class:`compas.colors.Color`]
        The colors of the map.

    See Also
    --------
    The available named palettes for this color map are due to https://www.fabiocrameri.ch/colourmaps/
    and the corresponding python package https://pypi.org/project/cmcrameri/

    Examples
    --------
    >>> cmap = ColorMap.from_palette('oslo')
    >>> cmap.plot()

    """

    def __init__(self, colors):
        self._colors = None
        self.colors = colors

    @property
    def colors(self):
        return self._colors

    @colors.setter
    def colors(self, colors):
        self._colors = [Color(r, g, b) for r, g, b in colors]

    @classmethod
    def from_palette(cls, name):
        """Construct a color map from a palette name.

        Parameters
        ----------
        name : str
            The name of the palette.

        Returns
        -------
        :class:`compas.colors.ColorMap`

        Raises
        ------
        FileNotFoundError
            If the file containing the colors of the palette doesn't exist.

        """
        here = os.path.dirname(__file__)
        path = os.path.join(here, 'cmaps', '{}.txt'.format(name))
        colors = []
        with open(path, 'r') as f:
            for line in f:
                if line:
                    parts = line.split()
                    if len(parts) == 3:
                        r = float(parts[0])
                        g = float(parts[1])
                        b = float(parts[2])
                        colors.append((r, g, b))
        return cls(colors)

    def plot(self):
        """Visualize the current map with the plotter.

        Returns
        -------
        None

        """
        from compas_plotters.plotter import Plotter
        from compas.geometry import Pointcloud
        from compas.geometry import Plane, Circle
        plotter = Plotter()
        cloud = Pointcloud.from_bounds(10, 10, 0, len(self.colors))
        for i, color in enumerate(self.colors):
            c = Circle(Plane(cloud[i], [0, 0, 1]), 0.1)
            plotter.add(c, facecolor=color, edgecolor=color)
        plotter.zoom_extents()
        plotter.show()
