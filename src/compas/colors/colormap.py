from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

from compas.utilities import linspace

from .color import Color
from .mpl_colormap import _magma_data
from .mpl_colormap import _inferno_data
from .mpl_colormap import _plasma_data
from .mpl_colormap import _viridis_data

mpl = {
    "magma": _magma_data,
    "inferno": _inferno_data,
    "plasma": _plasma_data,
    "viridis": _viridis_data,
}


class ColorMap(object):
    """Class providing a map for colors of a specific color palette.

    Parameters
    ----------
    colors : sequence[tuple[float, float, float]]
        A sequence of colors forming the map.

    Attributes
    ----------
    colors : list[:class:`~compas.colors.Color`]
        The colors of the map.

    Examples
    --------
    >>> import random
    >>> cmap = ColorMap.from_palette('bamako')
    >>> for i in range(100):
    ...     color = cmap(random.random())
    ...

    >>> cmap = ColorMap.from_mpl('viridis')
    >>> n = 100
    >>> for i in range(n):
    ...     color = cmap(i, 0, n - 1)
    ...

    >>> cmap = ColorMap.from_color(Color.red(), rangetype='light')
    >>> cmap.plot()    # doctest: +SKIP

    """

    def __init__(self, colors):
        self._colors = None
        self.colors = colors

    # --------------------------------------------------------------------------
    # properties
    # --------------------------------------------------------------------------

    @property
    def colors(self):
        return self._colors

    @colors.setter
    def colors(self, colors):
        self._colors = [Color(r, g, b) for r, g, b in colors]

    # --------------------------------------------------------------------------
    # customization
    # --------------------------------------------------------------------------

    def __getitem__(self, index):
        return self.colors[index]

    def __call__(self, value, minval=0.0, maxval=1.0):
        """Returns the color in the map corresponding to the given value.

        Parameters
        ----------
        value : float
            The data value for which a color should be computed.
        minval : float, optional
            The minimum value of the data range.
        maxval : float, optional
            The maximum value of the data range.

        Returns
        -------
        :class:`~compas.colors.Color`

        """
        key = (value - minval) / (maxval - minval)
        if key > 1.0 or key < 0.0:
            raise KeyError("The normalized value must be in the range 0 - 1.")
        index = int(key * (len(self.colors) - 1))
        return self.colors[index]

    # --------------------------------------------------------------------------
    # constructors
    # --------------------------------------------------------------------------

    @classmethod
    def from_palette(cls, name):
        """Construct a color map from a named palette.

        Parameters
        ----------
        name : str
            The name of the palette.

        Returns
        -------
        :class:`~compas.colors.ColorMap`

        Raises
        ------
        FileNotFoundError
            If the file containing the colors of the palette doesn't exist.

        Notes
        -----
        The colormaps use the colors of the palettes available here https://www.fabiocrameri.ch/colourmaps/
        and the python package https://pypi.org/project/cmcrameri/.
        See `compas/colors/cmcrameri/LICENSE` for more info.

        """
        here = os.path.dirname(__file__)
        path = os.path.join(here, "cmcrameri", "{}.txt".format(name))
        colors = []
        with open(path, "r") as f:
            for line in f:
                if line:
                    parts = line.split()
                    if len(parts) == 3:
                        r = float(parts[0])
                        g = float(parts[1])
                        b = float(parts[2])
                        colors.append((r, g, b))
        cmap = cls(colors)
        return cmap

    @classmethod
    def from_mpl(cls, name):
        """Construct a color map from matplotlib.

        Parameters
        ----------
        name : Literal['magma', 'inferno', 'plasma', 'viridis']
            The name of the mpl colormap.

        Returns
        -------
        :class:`~compas.colors.ColorMap`

        Raises
        ------
        KeyError
            If the color is not available.

        Notes
        -----
        The palettes available through this function are from https://github.com/BIDS/colormap,
        but with the dependency on `matplotlib` removed to ensure compatibility with RhinoGH.
        See `compas/colors/mpl_colormap.py` for more info and license information.

        """
        colors = [Color(r, g, b) for r, g, b in mpl[name]]
        return cls(colors)

    @classmethod
    def from_color(cls, color, rangetype="full"):
        """Construct a color map from a single color by varying luminance.

        Parameters
        ----------
        color : :class:`~compas.colors.Color`
            The base color.
        rangetype : Literal['full', 'light', 'dark'], optional
            If ``'full'``, use the full luminance range (0.0 - 1.0).
            If ``'light'``, use only the "light" part of the luminance range (0.5 - 1.0).
            If ``'dark'``, use only the "dark" part of the luminance range (0.0 - 0.5).

        Returns
        -------
        :class:`~compas.colors.Color`

        """
        n = 256
        h, _, s = color.hls

        if rangetype == "full":
            step = 1.0 / (n - 1)
            colors = [Color.from_hls(h, 0.0 + i * step, s) for i in range(n)]
            return cls(colors)

        if rangetype == "light":
            step = 0.5 / (n - 1)
            colors = [Color.from_hls(h, 0.5 + i * step, s) for i in range(n)]
            return cls(colors)

        if rangetype == "dark":
            step = 0.5 / (n - 1)
            colors = [Color.from_hls(h, 0.0 + i * step, s) for i in range(n)]
            return cls(colors)

        raise ValueError("`rangetype` should be one of 'full', 'light', 'dark'.")

    @classmethod
    def from_two_colors(cls, c1, c2, diverging=False):
        """Create a color map from two colors.

        Parameters
        ----------
        c1 : :class:`~compas.colors.Color`
            The first color.
        c2 : :class:`~compas.colors.Color`
            The second color.
        diverging : bool, optional
            If True, use white as transition color in the middle.

        Returns
        -------
        :class:`~compas.colors.ColorMap`

        """
        colors = []
        if diverging:
            for i in linspace(0, 1.0, 128):
                r = c1[0] * (1 - i) + 1.0 * i
                g = c1[1] * (1 - i) + 1.0 * i
                b = c1[2] * (1 - i) + 1.0 * i
                colors.append(Color(r, g, b))
            for i in linspace(0, 1.0, 128):
                r = 1.0 * (1 - i) + c2[0] * i
                g = 1.0 * (1 - i) + c2[1] * i
                b = 1.0 * (1 - i) + c2[2] * i
                colors.append(Color(r, g, b))
        else:
            for i in linspace(0, 1, 256):
                r = c1[0] * (1 - i) + c2[0] * i
                g = c1[1] * (1 - i) + c2[1] * i
                b = c1[2] * (1 - i) + c2[2] * i
                colors.append(Color(r, g, b))
        return cls(colors)

    @classmethod
    def from_three_colors(cls, c1, c2, c3):
        """Construct a color map from three colors.

        Parameters
        ----------
        c1 : :class:`~compas.colors.Color`
            The first color.
        c2 : :class:`~compas.colors.Color`
            The second color.
        c3 : :class:`~compas.colors.Color`
            The third color.

        Returns
        -------
        :class:`~compas.colors.ColorMap`

        """
        colors = []
        for i in linspace(0, 1.0, 128):
            r = c1[0] * (1 - i) + c2[0] * i
            g = c1[1] * (1 - i) + c2[1] * i
            b = c1[2] * (1 - i) + c2[2] * i
            colors.append(Color(r, g, b))
        for i in linspace(0, 1.0, 128):
            r = c2[0] * (1 - i) + c3[0] * i
            g = c2[1] * (1 - i) + c3[1] * i
            b = c2[2] * (1 - i) + c3[2] * i
            colors.append(Color(r, g, b))
        return cls(colors)

    @classmethod
    def from_rgb(cls):
        """Construct a color map from the complete rgb color space.

        Returns
        -------
        :class:`~compas.colors.Color`

        """
        colors = []
        for i in linspace(0, 1.0, 256):
            colors.append(Color.from_i(i))
        return cls(colors)

    # --------------------------------------------------------------------------
    # methods
    # --------------------------------------------------------------------------

    def plot(self):
        """Visualize the current map with the plotter.

        Returns
        -------
        None

        """
        from compas_plotters.plotter import Plotter
        from compas.geometry import Pointcloud
        from compas.geometry import Plane, Circle, Polygon

        plotter = Plotter(figsize=(16, 12))
        w = 16
        h = 10
        n = len(self.colors)
        d = w / n
        cloud = Pointcloud.from_bounds(w, h, 0, n)
        white = Color.white()
        for i, color in enumerate(self.colors):
            c = Circle(Plane(cloud[i], [0, 0, 1]), 0.1)
            p = Polygon(
                [
                    [i * d, -2, 0],
                    [(i + 1) * d, -2, 0],
                    [(i + 1) * d, -1, 0],
                    [i * d, -1, 0],
                ]
            )
            plotter.add(c, facecolor=color, edgecolor=white, linewidth=0.5)
            plotter.add(p, facecolor=color, edgecolor=color)
        plotter.zoom_extents()
        plotter.show()
