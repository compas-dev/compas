import colorsys
import math
import re
from collections.abc import Iterator
from collections.abc import Sequence
from typing import Self
from typing import TypeGuard

from compas.colors.html_colors import HTML_TO_RGB255
from compas.data import Data
from compas.tolerance import TOL


class ColorError(Exception):
    """Raise if color input is not a color."""


ColorLikeSequence = Sequence[int] | Sequence[float]
ColorLike = str | ColorLikeSequence
type ColorInput = Color | ColorLike | None


class Color(Data):
    """Class for working with colors.

    Parameters
    ----------
    red
        The red component in the range `[0.0, 1.0]`.
    green
        The green component in the range `[0.0, 1.0]`.
    blue
        The blue component in the range `[0.0, 1.0]`.
    alpha
        Transparency setting.
        If `alpha = 0.0`, the color is fully transparent.
        If `alpha = 1.0`, the color is fully opaque.
    name
        The name of the color.

    Examples
    --------
    By default, this class creates a color with RGB components in the range `[0.0, 1.0]`.

    >>> Color(1, 0, 0)
    Color(red=1, green=0, blue=0, alpha=1.0)

    Components outside `[0.0, 1.0]` raise `ValueError`.

    >>> Color(255, 0, 0)
    Traceback (most recent call last):
    ...
    ValueError: Components of an RGBA color should be in the range 0-1.

    To create a color with components in `[0, 255]`, use `from_rgb255`.

    >>> Color.from_rgb255(255, 0, 0)
    Color(red=1.0, green=0.0, blue=0.0, alpha=1.0)

    Similarly, other constructors are available to create colors from other color spaces.

    >>> color = Color.from_hls(0.0, 0.5, 1.0)
    >>> color = Color.from_hsv(0.0, 1.0, 1.0)
    >>> color = Color.from_yiq(0.0, 0.0, 0.0)
    >>> color = Color.from_yuv(0.0, 0.0, 0.0)

    Or, to construct specific colors, for example, ...

    >>> color = Color.red()
    >>> color = Color.magenta()
    >>> color = Color.lime()
    >>> color = Color.navy()
    >>> color = Color.olive()

    Colors can be modified through inversion, saturation/desaturation, and lightening/darkening.

    >>> color = Color.red()
    >>> color.desaturated(25)
    Color(red=0.875, green=0.125, blue=0.125, alpha=1.0)
    >>> color.desaturated(50)
    Color(red=0.75, green=0.25, blue=0.25, alpha=1.0)
    >>> color.desaturated(75)
    Color(red=0.625, green=0.375, blue=0.375, alpha=1.0)
    >>> color.desaturated(100)
    Color(red=0.5, green=0.5, blue=0.5, alpha=1.0)

    See Also
    --------
    [`ColorMap`][compas.colors.ColorMap]

    """

    # --------------------------------------------------------------------------
    # Data
    # --------------------------------------------------------------------------

    @property
    def __data__(self) -> dict[str, float]:
        return {"red": self.r, "green": self.g, "blue": self.b, "alpha": self.a}

    # --------------------------------------------------------------------------
    # Dunder methods
    # --------------------------------------------------------------------------

    def __init__(self, red: float, green: float, blue: float, alpha: float = 1.0, name: str | None = None) -> None:
        super().__init__(name=name)
        self._r: float = 1.0
        self._g: float = 1.0
        self._b: float = 1.0
        self._a: float = 1.0
        self.r = red
        self.g = green
        self.b = blue
        self.a = alpha

    def __repr__(self) -> str:
        return "{0}(red={1}, green={2}, blue={3}, alpha={4})".format(type(self).__name__, self.r, self.g, self.b, self.a)

    def __str__(self) -> str:
        return "{0}(red={1}, green={2}, blue={3}, alpha={4})".format(
            type(self).__name__,
            TOL.format_number(self.r),
            TOL.format_number(self.g),
            TOL.format_number(self.b),
            TOL.format_number(self.a),
        )

    def __getitem__(self, key: int) -> float:
        if key == 0:
            return self.r
        if key == 1:
            return self.g
        if key == 2:
            return self.b
        raise KeyError

    def __len__(self) -> int:
        return 3

    def __iter__(self) -> Iterator[float]:
        return iter(self.rgb)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Color):
            return self.rgba == other.rgba
        if not isinstance(other, Sequence) or isinstance(other, str):
            return False
        if len(other) == 3:
            return self.a == 1.0 and self.rgb == tuple(other)
        if len(other) == 4:
            return self.rgba == tuple(other)
        return False

    # --------------------------------------------------------------------------
    # Properties
    # --------------------------------------------------------------------------

    @property
    def r(self) -> float:
        """The red component in RGB1 space."""
        return self._r

    @r.setter
    def r(self, red: float) -> None:
        if isinstance(red, bool) or not math.isfinite(red) or red > 1.0 or red < 0.0:
            raise ValueError("Components of an RGBA color should be in the range 0-1.")
        self._r = red

    @property
    def g(self) -> float:
        """The green component in RGB1 space."""
        return self._g

    @g.setter
    def g(self, green: float) -> None:
        if isinstance(green, bool) or not math.isfinite(green) or green > 1.0 or green < 0.0:
            raise ValueError("Components of an RGBA color should be in the range 0-1.")
        self._g = green

    @property
    def b(self) -> float:
        """The blue component in RGB1 space."""
        return self._b

    @b.setter
    def b(self, blue: float) -> None:
        if isinstance(blue, bool) or not math.isfinite(blue) or blue > 1.0 or blue < 0.0:
            raise ValueError("Components of an RGBA color should be in the range 0-1.")
        self._b = blue

    @property
    def a(self) -> float:
        """The alpha component in RGBA1 space."""
        return self._a

    @a.setter
    def a(self, alpha: float) -> None:
        if isinstance(alpha, bool) or not math.isfinite(alpha) or alpha > 1.0 or alpha < 0.0:
            raise ValueError("Components of an RGBA color should be in the range 0-1.")
        self._a = alpha

    @property
    def rgb(self) -> tuple[float, float, float]:
        """The RGB1 components."""
        r = self.r
        g = self.g
        b = self.b
        return r, g, b

    @property
    def rgb255(self) -> tuple[int, int, int]:
        """The RGB components scaled to integer values from 0 to 255."""
        r = round(self.r * 255)
        g = round(self.g * 255)
        b = round(self.b * 255)
        return r, g, b

    @property
    def rgba(self) -> tuple[float, float, float, float]:
        """The RGBA1 components."""
        r, g, b = self.rgb
        a = self.a
        return r, g, b, a

    @property
    def rgba255(self) -> tuple[int, int, int, int]:
        """The RGBA components scaled to integer values from 0 to 255."""
        r, g, b = self.rgb255
        a = round(self.a * 255)
        return r, g, b, a

    @property
    def hex(self) -> str:
        """The RGB components as a six-digit hexadecimal string."""
        return "#{0:02x}{1:02x}{2:02x}".format(*self.rgb255)

    @property
    def hls(self) -> tuple[float, float, float]:
        """The hue, lightness, and saturation components."""
        return colorsys.rgb_to_hls(*self.rgb)

    @property
    def hsv(self) -> tuple[float, float, float]:
        """The hue, saturation, and value components."""
        return colorsys.rgb_to_hsv(*self.rgb)

    @property
    def lightness(self) -> float:
        """The HLS lightness component."""
        return self.hls[1]

    @property
    def brightness(self) -> float:
        """The HSV value or brightness component."""
        return self.hsv[2]

    @property
    def is_light(self) -> bool:
        """Whether the relative luminance exceeds the contrast threshold."""
        return self.luminance > 0.179

    @property
    def yuv(self) -> tuple[float, float, float]:
        """The luma and two chroma components."""
        y = self.luma
        u, v = self.chroma
        return y, u, v

    @property
    def luma(self) -> float:
        """The weighted brightness of the YUV signal."""
        return 0.299 * self.r + 0.587 * self.g + 0.114 * self.b

    @property
    def chroma(self) -> tuple[float, float]:
        """The blue and red projections of the YUV signal."""
        y = self.luma
        u = 0.492 * (self.b - y)
        v = 0.877 * (self.r - y)
        return u, v

    @property
    def luminance(self) -> float:
        """The relative luminance of the color in linear sRGB space.

        Notes
        -----
        The sRGB components are linearized before applying the relative
        luminance coefficients defined by WCAG.

        References
        ----------
        - [WCAG relative luminance](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html)

        """
        r = self.r / 12.92 if self.r <= 0.04045 else ((self.r + 0.055) / 1.055) ** 2.4
        g = self.g / 12.92 if self.g <= 0.04045 else ((self.g + 0.055) / 1.055) ** 2.4
        b = self.b / 12.92 if self.b <= 0.04045 else ((self.b + 0.055) / 1.055) ** 2.4
        return 0.2126 * r + 0.7152 * g + 0.0722 * b

    @property
    def saturation(self) -> float:
        """The HSV saturation.

        Achromatic black has zero saturation.

        """
        maxval = max(self.r, self.g, self.b)
        minval = min(self.r, self.g, self.b)
        if maxval == 0.0:
            return 0.0
        return (maxval - minval) / maxval

    @property
    def contrast(self) -> Self:
        """A darker or lighter color that contrasts with this color."""
        return self.darkened(25) if self.is_light else self.lightened(50)

    # --------------------------------------------------------------------------
    # Constructors
    # --------------------------------------------------------------------------

    @classmethod
    def from_rgb255(cls, r: int, g: int, b: int) -> Self:
        """Construct a color from RGB255 components.

        Parameters
        ----------
        r
            Red component in the range `[0, 255]`.
        g
            Green component in the range `[0, 255]`.
        b
            Blue component in the range `[0, 255]`.

        Returns
        -------
        Self

        """
        return cls(r / 255, g / 255, b / 255)

    @classmethod
    def from_hls(cls, hue: float, luminance: float, saturation: float) -> Self:
        """Construct a color from Hue, Lightness, and Saturation.

        Parameters
        ----------
        hue
            Hue.
        luminance
            Lightness.
        saturation
            Saturation.

        Returns
        -------
        Self

        References
        ----------
        - [HSL and HSV](https://en.wikipedia.org/wiki/HSL_and_HSV)

        """
        r, g, b = colorsys.hls_to_rgb(hue, luminance, saturation)
        return cls(r, g, b)

    @classmethod
    def from_hsv(cls, h: float, s: float, v: float) -> Self:
        """Construct a color from Hue, Saturation, and Value.

        Parameters
        ----------
        h
            Hue.
        s
            Saturation.
        v
            Value.

        Returns
        -------
        Self

        References
        ----------
        - [HSL and HSV](https://en.wikipedia.org/wiki/HSL_and_HSV)

        """
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return cls(r, g, b)

    @classmethod
    def from_yiq(cls, y: float, i: float, q: float) -> Self:
        """Construct a color from components in the YIQ color space.

        Parameters
        ----------
        y
            Luma.
        i
            Orange-blue chroma.
        q
            Purple-green chroma.

        Returns
        -------
        Self

        References
        ----------
        - [YIQ](https://en.wikipedia.org/wiki/YIQ)

        """
        r, g, b = colorsys.yiq_to_rgb(y, i, q)
        return cls(r, g, b)

    @classmethod
    def from_yuv(cls, y: float, u: float, v: float) -> Self:
        """Construct a color from components in the YUV color space.

        Parameters
        ----------
        y
            Luma.
        u
            Blue projection chroma.
        v
            Red projection chroma.

        Returns
        -------
        Self

        References
        ----------
        - [YUV](https://en.wikipedia.org/wiki/YUV)

        """
        r = y + 1.140 * v
        g = y - 0.395 * u - 0.581 * v
        b = y + 2.032 * u
        return cls(r, g, b)

    @classmethod
    def from_number(cls, number: float) -> Self:
        """Construct a color from a single number in the range 0-1.

        Parameters
        ----------
        number
            Number in the range 0-1, representing the color.

        Returns
        -------
        Self

        """
        if number == 0.0:
            r, g, b = 0, 0, 255
        elif 0.0 < number < 0.25:
            r, g, b = 0, int(255 * (4 * number)), 255
        elif number == 0.25:
            r, g, b = 0, 255, 255
        elif 0.25 < number < 0.5:
            r, g, b = 0, 255, int(255 - 255 * 4 * (number - 0.25))
        elif number == 0.5:
            r, g, b = 0, 255, 0
        elif 0.5 < number < 0.75:
            r, g, b = int(0 + 255 * 4 * (number - 0.5)), 255, 0
        elif number == 0.75:
            r, g, b = 255, 255, 0
        elif 0.75 < number < 1.0:
            (r, g, b) = (255, int(255 - 255 * 4 * (number - 0.75)), 0)
        elif number == 1.0:
            r, g, b = 255, 0, 0
        else:
            r, g, b = 0, 0, 0
        return cls(r / 255.0, g / 255.0, b / 255.0)

    from_i = from_number

    @classmethod
    def from_hex(cls, value: str) -> Self:
        """Construct a color from a hexadecimal color value.

        Parameters
        ----------
        value
            The hexadecimal color.

        Returns
        -------
        Self

        """
        if not cls._is_hex(value):
            raise ValueError("A hexadecimal color should contain three or six hexadecimal digits.")
        value = value.removeprefix("#").lower()
        if len(value) == 3:
            value = "".join(character * 2 for character in value)
        r = int(value[0:2], 16)
        g = int(value[2:4], 16)
        b = int(value[4:6], 16)
        return cls(r / 255.0, g / 255.0, b / 255.0)

    @classmethod
    def from_name(cls, name: str) -> Self:
        """Construct a color from a name in the extended color table of HTML/CSS/SVG.

        Parameters
        ----------
        name
            The color name. The name is case-insensitive.

        Returns
        -------
        Self

        References
        ----------
        - [CSS Color Module Level 3](https://www.w3.org/TR/css-color-3/#svg-color)

        """
        rgb255 = HTML_TO_RGB255.get(name.lower())
        if rgb255 is None:
            raise ValueError("Color name not found.")
        return cls.from_rgb255(*rgb255)

    @classmethod
    def from_unknown(cls, unknown: ColorInput) -> Self | None:
        """Construct a color from an unknown input.

        Parameters
        ----------
        unknown
            The color input.

        Returns
        -------
        Self | None

        Raises
        ------
        ColorError

        """
        if unknown is None:
            return None

        if isinstance(unknown, cls):
            return unknown

        if isinstance(unknown, Color):
            return cls(unknown.r, unknown.g, unknown.b, unknown.a)

        if cls._is_rgb255(unknown):
            return cls.from_rgb255(unknown[0], unknown[1], unknown[2])

        if cls._is_hex(unknown):
            return cls.from_hex(unknown)

        if cls._is_rgb1(unknown):
            return cls(unknown[0], unknown[1], unknown[2])

        if isinstance(unknown, str):
            return cls.from_name(unknown)

        raise ColorError(f"Cannot convert {unknown!r} to a color.")

    @classmethod
    def coerce(cls, color: ColorInput) -> Self | None:
        """Coerce a color input into a color.

        Parameters
        ----------
        color
            The color input.

        Returns
        -------
        Self | None

        Raises
        ------
        ColorError

        """
        return cls.from_unknown(color)

    @classmethod
    def white(cls) -> Self:
        """Construct the color white.

        Returns
        -------
        Self

        """
        return cls(1.0, 1.0, 1.0)

    @classmethod
    def black(cls) -> Self:
        """Construct the color black.

        Returns
        -------
        Self

        """
        return cls(0.0, 0.0, 0.0)

    @classmethod
    def grey(cls) -> Self:
        """Construct the color grey.

        Returns
        -------
        Self

        """
        return cls(0.5, 0.5, 0.5)

    @classmethod
    def red(cls) -> Self:
        """Construct the color red.

        Returns
        -------
        Self

        """
        return cls(1.0, 0.0, 0.0)

    @classmethod
    def orange(cls) -> Self:
        """Construct the color orange.

        Returns
        -------
        Self

        """
        return cls(1.0, 0.5, 0.0)

    @classmethod
    def yellow(cls) -> Self:
        """Construct the color yellow.

        Returns
        -------
        Self

        """
        return cls(1.0, 1.0, 0.0)

    @classmethod
    def lime(cls) -> Self:
        """Construct the color lime (or chartreuse green).

        Returns
        -------
        Self

        """
        return cls(0.5, 1.0, 0.0)

    @classmethod
    def green(cls) -> Self:
        """Construct the color green.

        Returns
        -------
        Self

        """
        return cls(0.0, 1.0, 0.0)

    @classmethod
    def mint(cls) -> Self:
        """Construct the color mint (or spring green).

        Returns
        -------
        Self

        """
        return cls(0.0, 1.0, 0.5)

    @classmethod
    def cyan(cls) -> Self:
        """Construct the color cyan.

        Returns
        -------
        Self

        """
        return cls(0.0, 1.0, 1.0)

    @classmethod
    def azure(cls) -> Self:
        """Construct the color azure.

        Returns
        -------
        Self

        """
        return cls(0.0, 0.5, 1.0)

    @classmethod
    def blue(cls) -> Self:
        """Construct the color blue.

        Returns
        -------
        Self

        """
        return cls(0.0, 0.0, 1.0)

    @classmethod
    def violet(cls) -> Self:
        """Construct the color violet.

        Returns
        -------
        Self

        """
        return cls(0.5, 0.0, 1.0)

    @classmethod
    def magenta(cls) -> Self:
        """Construct the color magenta.

        Returns
        -------
        Self

        """
        return cls(1.0, 0.0, 1.0)

    @classmethod
    def pink(cls) -> Self:
        """Construct the color pink.

        Returns
        -------
        Self

        """
        return cls(1.0, 0.0, 0.5)

    @classmethod
    def maroon(cls) -> Self:
        """Construct the color maroon.

        Returns
        -------
        Self

        """
        return cls(0.5, 0.0, 0.0)

    @classmethod
    def brown(cls) -> Self:
        """Construct the color brown.

        Returns
        -------
        Self

        """
        return cls(0.5, 0.25, 0.0)

    @classmethod
    def olive(cls) -> Self:
        """Construct the color olive.

        Returns
        -------
        Self

        """
        return cls(0.5, 0.5, 0.0)

    @classmethod
    def teal(cls) -> Self:
        """Construct the color teal.

        Returns
        -------
        Self

        """
        return cls(0.0, 0.5, 0.5)

    @classmethod
    def navy(cls) -> Self:
        """Construct the color navy.

        Returns
        -------
        Self

        """
        return cls(0.0, 0.0, 0.5)

    @classmethod
    def purple(cls) -> Self:
        """Construct the color purple.

        Returns
        -------
        Self

        """
        return cls(0.5, 0.0, 0.5)

    @classmethod
    def silver(cls) -> Self:
        """Construct the color silver.

        Returns
        -------
        Self

        """
        return cls(0.75, 0.75, 0.75)

    # ochre
    # beige
    # bordeaux
    # hotpink
    # steel
    # midnight
    # salmon

    # --------------------------------------------------------------------------
    # Methods
    # --------------------------------------------------------------------------

    def lighten(self, factor: float = 10.0) -> None:
        """Lighten the color.

        Parameters
        ----------
        factor
            Percentage of lightness increase.

        Raises
        ------
        ValueError
            If the percentage of lightness increase is not in the range 0-100.

        """
        if factor > 100 or factor < 0:
            raise ValueError("Percentage of increased lightness should be in the range 0-100.")

        factor = 1.0 + factor / 100

        hue, luminance, saturation = self.hls
        r, g, b = colorsys.hls_to_rgb(hue, min(1.0, luminance * factor), saturation)
        self.r = r
        self.g = g
        self.b = b

    def lightened(self, factor: float = 10.0) -> Self:
        """Return a lightened copy of the color.

        Parameters
        ----------
        factor
            Percentage of lightness increase.

        Returns
        -------
        Self

        Raises
        ------
        ValueError
            If the percentage of lightness increase is not in the range 0-100.

        """
        color = self.copy()
        color.lighten(factor=factor)
        return color

    def darken(self, factor: float = 10.0) -> None:
        """Darken the color.

        Parameters
        ----------
        factor
            Percentage of lightness reduction.

        Raises
        ------
        ValueError
            If the percentage of lightness reduction is not in the range 0-100.

        """
        if factor > 100 or factor < 0:
            raise ValueError("Percentage of reduced lightness should be in the range 0-100.")

        factor = 1.0 - factor / 100

        hue, luminance, saturation = self.hls
        r, g, b = colorsys.hls_to_rgb(hue, max(0.0, luminance * factor), saturation)
        self.r = r
        self.g = g
        self.b = b

    def darkened(self, factor: float = 10.0) -> Self:
        """Return a darkened copy of the color.

        Parameters
        ----------
        factor
            Percentage of lightness reduction.

        Returns
        -------
        Self

        Raises
        ------
        ValueError
            If the percentage of lightness reduction is not in the range 0-100.

        """
        color = self.copy()
        color.darken(factor=factor)
        return color

    def invert(self) -> None:
        """Invert the current color wrt to the RGB color circle."""
        self.r = 1.0 - self.r
        self.g = 1.0 - self.g
        self.b = 1.0 - self.b

    def inverted(self) -> Self:
        """Return an inverted copy of the color.

        Returns
        -------
        Self

        """
        color = self.copy()
        color.invert()
        return color

    def saturate(self, factor: float = 10.0) -> None:
        """Saturate the color by a given percentage.

        Parameters
        ----------
        factor
            Percentage of saturation increase.

        Raises
        ------
        ValueError
            If the percentage of saturation is not in the range 0-100.

        """
        if factor > 100 or factor < 0:
            raise ValueError("Percentage of saturation should be in the range 0-100.")

        factor = 1.0 + factor / 100

        hue, luminance, saturation = self.hls
        r, g, b = colorsys.hls_to_rgb(hue, luminance, min(1.0, saturation * factor))
        self.r = r
        self.g = g
        self.b = b

    def saturated(self, factor: float = 10.0) -> Self:
        """Return a saturated copy of the color.

        Parameters
        ----------
        factor
            Percentage of saturation increase.

        Returns
        -------
        Self

        Raises
        ------
        ValueError
            If the percentage of desaturation is not in the range 0-100.

        """
        color = self.copy()
        color.saturate(factor=factor)
        return color

    def desaturate(self, factor: float = 10.0) -> None:
        """Desaturate the color by a given percentage.

        Parameters
        ----------
        factor
            Percentage of saturation reduction.

        Raises
        ------
        ValueError
            If the percentage of desaturation is not in the range 0-100.

        """
        if factor > 100 or factor < 0:
            raise ValueError("Percentage of desaturation should be in the range 0-100.")

        factor = 1.0 - factor / 100

        hue, luminance, saturation = self.hls
        r, g, b = colorsys.hls_to_rgb(hue, luminance, max(0.0, saturation * factor))
        self.r = r
        self.g = g
        self.b = b

    def desaturated(self, factor: float = 10.0) -> Self:
        """Return a desaturated copy of the color.

        Parameters
        ----------
        factor
            Percentage of saturation reduction.

        Returns
        -------
        Self

        Raises
        ------
        ValueError
            If the percentage of desaturation is not in the range 0-100.

        """
        color = self.copy()
        color.desaturate(factor=factor)
        return color

    # --------------------------------------------------------------------------
    # Private helpers
    # --------------------------------------------------------------------------

    @staticmethod
    def _is_rgb1(color: object) -> TypeGuard[Sequence[float]]:
        """Verify that the color is in the RGB 1 color space.

        Returns
        -------
        bool

        """
        if not isinstance(color, Sequence) or isinstance(color, str) or len(color) != 3:
            return False
        return all(isinstance(c, (int, float)) and not isinstance(c, bool) and c >= 0 and c <= 1 for c in color)

    @staticmethod
    def _is_rgb255(color: object) -> TypeGuard[Sequence[int]]:
        """Verify that the color is in the RGB 255 color space.

        Returns
        -------
        bool

        """
        if not isinstance(color, Sequence) or isinstance(color, str) or len(color) != 3:
            return False
        return all(isinstance(c, int) and not isinstance(c, bool) and 0 <= c <= 255 for c in color)

    @staticmethod
    def _is_hex(color: object) -> TypeGuard[str]:
        """Verify that the color is in hexadecimal format.

        Returns
        -------
        bool

        """
        return isinstance(color, str) and re.fullmatch(r"#?(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})", color) is not None
