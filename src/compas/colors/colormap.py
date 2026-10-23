from collections.abc import Sequence
from pathlib import Path
from typing import Literal
from typing import Self

from compas.data import Data
from compas.itertools import linspace

from .color import Color
from .mpl_colormap import _inferno_data
from .mpl_colormap import _magma_data
from .mpl_colormap import _plasma_data
from .mpl_colormap import _viridis_data

mpl = {
    "magma": _magma_data,
    "inferno": _inferno_data,
    "plasma": _plasma_data,
    "viridis": _viridis_data,
}

ColorMapColor = Sequence[float] | Color
ColorMapName = Literal["magma", "inferno", "plasma", "viridis"]
ColorRangeType = Literal["full", "light", "dark"]


class ColorMap(Data):
    """Class providing a map for 256 distinct colors of a specific color palette.

    Parameters
    ----------
    colors
        A sequence of colors forming the map.
        The number of colors in the sequence should be 256.

    Raises
    ------
    ValueError
        If the number of colors in the sequence is not 256.

    Examples
    --------
    >>> import random
    >>> cmap = ColorMap.from_palette("bamako")
    >>> for i in range(100):
    ...     color = cmap(random.random())

    >>> cmap = ColorMap.from_mpl("viridis")
    >>> n = 100
    >>> for i in range(n):
    ...     color = cmap(i, minval=0, maxval=n - 1)

    See Also
    --------
    [`Color`][compas.colors.Color]

    """

    # --------------------------------------------------------------------------
    # Data
    # --------------------------------------------------------------------------

    @property
    def __data__(self) -> dict[str, tuple[Color, ...]]:
        return {"colors": self.colors}

    @classmethod
    def __from_data__(cls, data: dict[str, Sequence[ColorMapColor]]) -> Self:
        return cls(data["colors"])

    # --------------------------------------------------------------------------
    # Dunder methods
    # --------------------------------------------------------------------------

    def __init__(self, colors: Sequence[ColorMapColor], name: str | None = None) -> None:
        super().__init__(name=name)
        self._colors: tuple[Color, ...] = ()
        self.colors = colors

    def __call__(self, value: float, minval: float = 0.0, maxval: float = 1.0) -> Color:
        """Return the color corresponding to a value in a numeric range.

        Parameters
        ----------
        value
            The data value for which a color should be computed.
        minval
            The minimum value of the data range.
        maxval
            The maximum value of the data range.

        Returns
        -------
        Color

        Raises
        ------
        KeyError
            If the value is not in the range `[minval, maxval]`.

        """
        if minval == maxval:
            raise ValueError("The color-map range should have a nonzero length.")
        key = (value - minval) / (maxval - minval)
        if key > 1.0 or key < 0.0:
            raise KeyError("The normalized value must be in the range 0 - 1.")
        index = int(key * (len(self.colors) - 1))
        return self.colors[index]

    # --------------------------------------------------------------------------
    # Properties
    # --------------------------------------------------------------------------

    @property
    def colors(self) -> tuple[Color, ...]:
        """The 256 colors in the map.

        The colors are exposed as an immutable tuple. Assigning colors copies
        every input color and requires exactly 256 three-component colors.

        """
        return self._colors

    @colors.setter
    def colors(self, colors: Sequence[ColorMapColor]) -> None:
        if len(colors) != 256:
            raise ValueError("The color map should have 256 colors.")
        copied = []
        for color in colors:
            if isinstance(color, Color):
                copied.append(Color(color.r, color.g, color.b, color.a))
                continue
            r, g, b = color
            copied.append(Color(r, g, b))
        self._colors = tuple(copied)

    # --------------------------------------------------------------------------
    # Constructors
    # --------------------------------------------------------------------------

    @classmethod
    def from_palette(cls, name: str) -> Self:
        """Construct a color map from a named palette.

        Parameters
        ----------
        name
            The name of the palette.

        Returns
        -------
        Self
            A color map with 256 colors.

        Raises
        ------
        FileNotFoundError
            If the file containing the colors of the palette doesn't exist.

        Notes
        -----
        The colormaps use the [Scientific colour maps](https://www.fabiocrameri.ch/colourmaps/)
        and the [cmcrameri](https://pypi.org/project/cmcrameri/) package.
        See `compas/colors/cmcrameri/LICENSE` for more info.

        """
        path = Path(__file__).parent / "cmcrameri" / f"{name}.txt"
        colors: list[tuple[float, float, float]] = []
        with path.open(encoding="utf-8") as f:
            for line in f:
                if line:
                    parts = line.split()
                    if len(parts) == 3:
                        r = float(parts[0])
                        g = float(parts[1])
                        b = float(parts[2])
                        colors.append((r, g, b))
        return cls(colors)

    @classmethod
    def from_mpl(cls, name: ColorMapName) -> Self:
        """Construct a color map from matplotlib.

        Parameters
        ----------
        name
            The name of the mpl colormap.

        Returns
        -------
        Self
            A color map with 256 colors.

        Raises
        ------
        KeyError
            If the color is not available.

        Notes
        -----
        The palettes available through this function are from
        [BIDS/colormap](https://github.com/BIDS/colormap), with the dependency
        on `matplotlib` removed.
        See `compas/colors/mpl_colormap.py` for more info and license information.

        """
        colors = [Color(r, g, b) for r, g, b in mpl[name]]
        return cls(colors)

    @classmethod
    def from_color(cls, color: Color, rangetype: ColorRangeType = "full") -> Self:
        """Construct a color map from a single color by varying luminance.

        Parameters
        ----------
        color
            The base color.
        rangetype
            If `"full"`, use the full luminance range from 0.0 to 1.0.
            If `"light"`, use the light half from 0.5 to 1.0.
            If `"dark"`, use the dark half from 0.0 to 0.5.

        Returns
        -------
        Self
            A color map with 256 colors.

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
    def from_two_colors(cls, c1: Color, c2: Color, diverging: bool = False) -> Self:
        """Create a color map from two colors.

        Parameters
        ----------
        c1
            The first color.
        c2
            The second color.
        diverging
            If True, use white as transition color in the middle.

        Returns
        -------
        Self
            A color map with 256 colors.

        """
        colors: list[Color] = []
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
    def from_three_colors(cls, c1: Color, c2: Color, c3: Color) -> Self:
        """Construct a color map from three colors.

        Parameters
        ----------
        c1
            The first color.
        c2
            The second color.
        c3
            The third color.

        Returns
        -------
        Self
            A color map with 256 colors.

        """
        colors: list[Color] = []
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
    def from_rgb(cls) -> Self:
        """Construct a color map from the complete rgb color space.

        Returns
        -------
        Self

        """
        colors: list[Color] = []
        for i in linspace(0, 1.0, 256):
            colors.append(Color.from_i(i))
        return cls(colors)
