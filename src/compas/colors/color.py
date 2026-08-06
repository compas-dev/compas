import colorsys
import re
from typing import Annotated
from typing import Iterator
from typing import Optional
from typing import Sequence
from typing import Union
from typing import cast

from typing_extensions import Self

from compas.colors.html_colors import HTML_TO_RGB255
from compas.data import Data
from compas.tolerance import TOL

BASE16: str = "0123456789abcdef"

HEX_DEC: dict[str, int] = {v: int(v, base=16) for v in [x + y for x in BASE16 for y in BASE16]}


class ColorError(Exception):
    """Raise if color input is not a color."""


ColorLikeSequence = Union[Annotated[Sequence[int], 3], Annotated[Sequence[float], 3]]
ColorLike = Union[str, ColorLikeSequence]
ColorInput = Union["Color", ColorLike]


class Color(Data):
    """Class for working with colors.

    Parameters
    ----------
    red
        The red component in the range ``[0.0, 1.0]``.
    green
        The green component in the range of ``[0.0, 1.0]``.
    blue
        The blue component in the range of ``[0.0, 1.0]``.
    alpha
        Transparency setting.
        If ``alpha = 0.0``, the color is fully transparent.
        If ``alpha = 1.0``, the color is fully opaque.
    name
        The name of the color.

    Attributes
    ----------
    r
        Red component of the color in RGB1 color space.
    g
        Green component of the color in RGB1 color space.
    b
        Blue component of the color in RGB1 color space.
    a
        Transparency in RGB1 color space.
    rgb
        RGB1 color tuple, with components in the range ``[0.0, 1.0]``.
    rgba
        RGBA1 color tuple (including alpha), with components in the range ``[0.0, 1.0]``.
    rgb255
        RGB255 color tuple, with components in the range ``[0, 255]``.
    rgba255
        RGBA255 color tuple (including alpha), with components in the range ``[0, 255]``.
    hex
        Hexadecimal color string.
    hls
        Hue, Lightness, Saturation.
    hsv
        Hue, Saturation, Value / Brightness.
    lightness
        How much white the color appears to contain.
        This is the "Lightness" in HLS.
        Making a color "lighter" is like adding more white.
    brightness
        How well-lit the color appears to be.
        This is the "Value" in HSV.
        Making a color "brighter" is like shining a stronger light on it, or illuminating it better.
    yuv
        Luma and chroma components, with chroma defined by the blue and red projections.
    luma
        The brightness of a yuv signal.
    chroma
        The color of a yuv signal.
        "How different from a grey of the same lightness the color appears to be."
    luminance
        The amount of light that passes through, is emitted from, or is reflected from a particular area.
        Here, it expresses the preceived brightness of the color.
        Note that this is not the same as the "Lightness" of HLS or the "Value/Brightness" of HSV.
    saturation
        The perceived freedom of whiteness.
    is_light
        If True, the color is considered light.
    contrast
        The contrasting color to the current color.

    Examples
    --------
    By default, this class will create a color with the RGB components in the range ``[0.0, 1.0]``.

    >>> Color(1, 0, 0)
    Color(red=1, green=0, blue=0, alpha=1.0)

    Attempting to create a color with components outside of the range ``[0.0, 1.0]`` will raise a ``ValueError``.

    >>> Color(255, 0, 0)
    Traceback (most recent call last):
    ...
    ValueError: Components of an RGBA color should be in the range 0-1.

    To create a color with components in the range ``[0, 255]``, use the `from_rgb255` constructor.

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
    compas.colors.ColorMap

    """

    @property
    def __data__(self) -> dict[str, float]:
        return {"red": self.r, "green": self.g, "blue": self.b, "alpha": self.a}

    def __init__(self, red: float, green: float, blue: float, alpha: float = 1.0, name: Optional[str] = None) -> None:
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
        other = cast(Union["Color", ColorLikeSequence], other)
        return all(a == b for a, b in zip(self, other))

    # --------------------------------------------------------------------------
    # Properties
    # --------------------------------------------------------------------------

    @property
    def r(self) -> float:
        return self._r

    @r.setter
    def r(self, red: float) -> None:
        if red > 1.0 or red < 0.0:
            raise ValueError("Components of an RGBA color should be in the range 0-1.")
        self._r = red

    @property
    def g(self) -> float:
        return self._g

    @g.setter
    def g(self, green: float) -> None:
        if green > 1.0 or green < 0.0:
            raise ValueError("Components of an RGBA color should be in the range 0-1.")
        self._g = green

    @property
    def b(self) -> float:
        return self._b

    @b.setter
    def b(self, blue: float) -> None:
        if blue > 1.0 or blue < 0.0:
            raise ValueError("Components of an RGBA color should be in the range 0-1.")
        self._b = blue

    @property
    def a(self) -> float:
        return self._a

    @a.setter
    def a(self, alpha: float) -> None:
        if alpha > 1.0 or alpha < 0.0:
            raise ValueError("Components of an RGBA color should be in the range 0-1.")
        self._a = alpha

    @property
    def rgb(self) -> tuple[float, float, float]:
        r = self.r
        g = self.g
        b = self.b
        return r, g, b

    @property
    def rgb255(self) -> tuple[int, int, int]:
        r = int(self.r * 255)
        g = int(self.g * 255)
        b = int(self.b * 255)
        return r, g, b

    @property
    def rgba(self) -> tuple[float, float, float, float]:
        r, g, b = self.rgb
        a = self.a
        return r, g, b, a

    @property
    def rgba255(self) -> tuple[int, int, int, int]:
        r, g, b = self.rgb255
        a = int(self.a * 255)
        return r, g, b, a

    @property
    def hex(self) -> str:
        return "#{0:02x}{1:02x}{2:02x}".format(*self.rgb255)

    @property
    def hls(self) -> tuple[float, float, float]:
        return colorsys.rgb_to_hls(*self.rgb)

    @property
    def hsv(self) -> tuple[float, float, float]:
        return colorsys.rgb_to_hsv(*self.rgb)

    @property
    def lightness(self) -> float:
        return self.hls[1]

    @property
    def brightness(self) -> float:
        return self.hsv[2]

    @property
    def is_light(self) -> bool:
        return self.luminance > 0.179

    @property
    def yuv(self) -> tuple[float, float, float]:
        y = self.luma
        u, v = self.chroma
        return y, u, v

    @property
    def luma(self) -> float:
        return 0.299 * self.r + 0.587 * self.g + 0.114 * self.b

    @property
    def chroma(self) -> tuple[float, float]:
        y = self.luma
        u = 0.492 * (self.b - y)
        v = 0.877 * (self.r - y)
        return u, v

    @property
    def luminance(self) -> float:
        return 0.2126 * self.r + 0.7152 * self.g + 0.0722 * self.b

    @property
    def saturation(self) -> float:
        maxval = max(self.r, self.g, self.b)
        minval = min(self.r, self.g, self.b)
        return (maxval - minval) / maxval

    @property
    def contrast(self) -> Self:
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
            Red component in the range ``[0, 255]``.
        g
            Green component in the range ``[0, 255]``.
        b
            Blue component in the range ``[0, 255]``.

        Returns
        -------
        Color

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
        Color

        References
        ----------
        https://en.wikipedia.org/wiki/HSL_and_HSV

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
        Color

        References
        ----------
        https://en.wikipedia.org/wiki/HSL_and_HSV

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
        Color

        References
        ----------
        https://en.wikipedia.org/wiki/YIQ

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
        Color

        References
        ----------
        https://en.wikipedia.org/wiki/YUV

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
        Color

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
        Color

        """
        value = value.lstrip("#").lower()
        r = HEX_DEC[value[0:2]]
        g = HEX_DEC[value[2:4]]
        b = HEX_DEC[value[4:6]]
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
        Color

        References
        ----------
        https://www.w3.org/TR/css-color-3/#svg-color

        """
        rgb255 = HTML_TO_RGB255.get(name.lower())
        if rgb255 is None:
            raise ValueError("Color name not found.")
        return cls.from_rgb255(*rgb255)

    @classmethod
    def from_unknown(cls, unknown: ColorInput) -> Optional["Color"]:
        """Construct a color from an unknown input.

        Parameters
        ----------
        unknown
            The color input.

        Returns
        -------
        Color | None

        Raises
        ------
        ColorError

        """
        if not unknown:
            return

        if isinstance(unknown, cls):
            return unknown

        if Color._is_rgb255(unknown):
            rgb255 = cast(tuple[int, int, int], list(cast(Sequence[int], unknown)))
            return cls.from_rgb255(*rgb255)

        if Color._is_hex(unknown):
            return cls.from_hex(cast(str, unknown))

        if Color._is_rgb1(unknown):
            rgb1 = cast(tuple[float, float, float], list(cast(Sequence[float], unknown)))
            return cls(*rgb1)

        if isinstance(unknown, str):
            return cls.from_name(unknown)

        raise ColorError

    @staticmethod
    def coerce(color: ColorInput) -> Optional["Color"]:
        """Coerce a color input into a color.

        Parameters
        ----------
        color
            The color input.

        Returns
        -------
        Color | None

        Raises
        ------
        ColorError

        """
        if not color:
            return
        if isinstance(color, Color):
            return color
        if Color._is_hex(color):
            return Color.from_hex(cast(str, color))
        if Color._is_rgb1(color):
            rgb1 = cast(tuple[float, float, float], color)
            return Color(*rgb1)
        if Color._is_rgb255(color):
            rgb255 = cast(tuple[int, int, int], color)
            return Color.from_rgb255(*rgb255)
        raise ColorError

    @staticmethod
    def _is_rgb1(color: object) -> bool:
        """Verify that the color is in the RGB 1 color space.

        Returns
        -------
        bool

        """
        if not color:
            return False
        color = cast(ColorLikeSequence, color)
        return all(isinstance(c, float) and (c >= 0 and c <= 1) for c in color)

    @staticmethod
    def _is_rgb255(color: object) -> bool:
        """Verify that the color is in the RGB 255 color space.

        Returns
        -------
        bool

        """
        if not color:
            return False
        color = cast(ColorLikeSequence, color)
        return all(isinstance(c, int) and (c >= 0 and c <= 255) for c in color)

    @staticmethod
    def _is_hex(color: object) -> bool:
        """Verify that the color is in hexadecimal format.

        Returns
        -------
        bool

        """
        if isinstance(color, str):
            match = re.search(r"^#(?:[0-9a-fA-F]{3}){1,2}$", color)
            if match:
                return True
            return False
        return False

    # --------------------------------------------------------------------------
    # Presets
    # --------------------------------------------------------------------------

    @classmethod
    def white(cls) -> Self:
        """Construct the color white.

        Returns
        -------
        Color

        """
        return cls(1.0, 1.0, 1.0)

    @classmethod
    def black(cls) -> Self:
        """Construct the color black.

        Returns
        -------
        Color

        """
        return cls(0.0, 0.0, 0.0)

    @classmethod
    def grey(cls) -> Self:
        """Construct the color grey.

        Returns
        -------
        Color

        """
        return cls(0.5, 0.5, 0.5)

    @classmethod
    def red(cls) -> Self:
        """Construct the color red.

        Returns
        -------
        Color

        """
        return cls(1.0, 0.0, 0.0)

    @classmethod
    def orange(cls) -> Self:
        """Construct the color orange.

        Returns
        -------
        Color

        """
        return cls(1.0, 0.5, 0.0)

    @classmethod
    def yellow(cls) -> Self:
        """Construct the color yellow.

        Returns
        -------
        Color

        """
        return cls(1.0, 1.0, 0.0)

    @classmethod
    def lime(cls) -> Self:
        """Construct the color lime (or chartreuse green).

        Returns
        -------
        Color

        """
        return cls(0.5, 1.0, 0.0)

    @classmethod
    def green(cls) -> Self:
        """Construct the color green.

        Returns
        -------
        Color

        """
        return cls(0.0, 1.0, 0.0)

    @classmethod
    def mint(cls) -> Self:
        """Construct the color mint (or spring green).

        Returns
        -------
        Color

        """
        return cls(0.0, 1.0, 0.5)

    @classmethod
    def cyan(cls) -> Self:
        """Construct the color cyan.

        Returns
        -------
        Color

        """
        return cls(0.0, 1.0, 1.0)

    @classmethod
    def azure(cls) -> Self:
        """Construct the color azure.

        Returns
        -------
        Color

        """
        return cls(0.0, 0.5, 1.0)

    @classmethod
    def blue(cls) -> Self:
        """Construct the color blue.

        Returns
        -------
        Color

        """
        return cls(0.0, 0.0, 1.0)

    @classmethod
    def violet(cls) -> Self:
        """Construct the color violet.

        Returns
        -------
        Color

        """
        return cls(0.5, 0.0, 1.0)

    @classmethod
    def magenta(cls) -> Self:
        """Construct the color magenta.

        Returns
        -------
        Color

        """
        return cls(1.0, 0.0, 1.0)

    @classmethod
    def pink(cls) -> Self:
        """Construct the color pink.

        Returns
        -------
        Color

        """
        return cls(1.0, 0.0, 0.5)

    # --------------------------------------------------------------------------
    # Other presets
    # --------------------------------------------------------------------------

    @classmethod
    def maroon(cls) -> Self:
        """Construct the color maroon.

        Returns
        -------
        Color

        """
        return cls(0.5, 0.0, 0.0)

    @classmethod
    def brown(cls) -> Self:
        """Construct the color brown.

        Returns
        -------
        Color

        """
        return cls(0.5, 0.25, 0.0)

    @classmethod
    def olive(cls) -> Self:
        """Construct the color olive.

        Returns
        -------
        Color

        """
        return cls(0.5, 0.5, 0.0)

    @classmethod
    def teal(cls) -> Self:
        """Construct the color teal.

        Returns
        -------
        Color

        """
        return cls(0.0, 0.5, 0.5)

    @classmethod
    def navy(cls) -> Self:
        """Construct the color navy.

        Returns
        -------
        Color

        """
        return cls(0.0, 0.0, 0.5)

    @classmethod
    def purple(cls) -> Self:
        """Construct the color purple.

        Returns
        -------
        Color

        """
        return cls(0.5, 0.0, 0.5)

    @classmethod
    def silver(cls) -> Self:
        """Construct the color silver.

        Returns
        -------
        Color

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

        Returns
        -------
        None

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
        Color

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

        Returns
        -------
        None

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
        Color

        Raises
        ------
        ValueError
            If the percentage of lightness reduction is not in the range 0-100.

        """
        color = self.copy()
        color.darken(factor=factor)
        return color

    def invert(self) -> None:
        """Invert the current color wrt to the RGB color circle.

        Returns
        -------
        None

        """
        self.r = 1.0 - self.r
        self.g = 1.0 - self.g
        self.b = 1.0 - self.b

    def inverted(self) -> Self:
        """Return an inverted copy of the color.

        Returns
        -------
        Color

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

        Returns
        -------
        None

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
        Color

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

        Returns
        -------
        None

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
        Color

        Raises
        ------
        ValueError
            If the percentage of desaturation is not in the range 0-100.

        """
        color = self.copy()
        color.desaturate(factor=factor)
        return color
