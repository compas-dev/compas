from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import warnings

import re

try:
    basestring
except NameError:
    basestring = str

warnings.warn(
    "The colors module in utilities is deprecated. Use compas.colors instead",
    DeprecationWarning,
    stacklevel=2,
)

red = 255, 0, 0
orange = 255, 125, 0
yellow = 255, 255, 0
yellowish = 125, 255, 0
green = 0, 255, 0
greenish = 0, 255, 125
cyan = 0, 255, 255
cyanish = 0, 125, 255
blue = 0, 0, 255

white = 255, 255, 255
black = 0, 0, 0


BASE16 = "0123456789abcdef"

try:
    HEX_DEC = {v: int(v, base=16) for v in [x + y for x in BASE16 for y in BASE16]}
except Exception:
    HEX_DEC = {v: int(v, 16) for v in [x + y for x in BASE16 for y in BASE16]}


def i_to_rgb(i, normalize=False):
    """Convert a number between 0.0 and 1.0 to an equivalent RGB tuple.

    .. deprecated:: 1.14
        Use :class:`~compas.colors.Color` instead.

    Parameters
    ----------
    i : float
        A number between 0.0 and 1.0.
    normalize : bool, optional
        If True, normalize the resulting RGB values.
        Default is to return integer values ranging from 0 to 255.

    Returns
    -------
    tuple
        The RGB values of the color corresponding to the provided number.
        If `normalize` is true, the RGB values are normalized to values between 0.0 and 1.0.
        If `normalize` is false, the RGB values are integers between 0 and 255.

    Examples
    --------
    >>> i_to_rgb(1.0)
    (255, 0, 0)
    >>> i_to_rgb(0.75)
    (255, 255, 0)
    >>> i_to_rgb(0.5)
    (0, 255, 0)
    >>> i_to_rgb(0.25)
    (0, 255, 255)
    >>> i_to_rgb(0.0)
    (0, 0, 255)

    >>> i_to_rgb(1.0, True)
    (1.0, 0.0, 0.0)
    >>> i_to_rgb(0.75, True)
    (1.0, 1.0, 0.0)
    >>> i_to_rgb(0.5, True)
    (0.0, 1.0, 0.0)
    >>> i_to_rgb(0.25, True)
    (0.0, 1.0, 1.0)
    >>> i_to_rgb(0.0, True)
    (0.0, 0.0, 1.0)

    """
    i = max(i, 0.0)
    i = min(i, 1.0)
    if i == 0.0:
        r, g, b = 0, 0, 255
    elif 0.0 < i < 0.25:
        r, g, b = 0, int(255 * (4 * i)), 255
    elif i == 0.25:
        r, g, b = 0, 255, 255
    elif 0.25 < i < 0.5:
        r, g, b = 0, 255, int(255 - 255 * 4 * (i - 0.25))
    elif i == 0.5:
        r, g, b = 0, 255, 0
    elif 0.5 < i < 0.75:
        r, g, b = int(0 + 255 * 4 * (i - 0.5)), 255, 0
    elif i == 0.75:
        r, g, b = 255, 255, 0
    elif 0.75 < i < 1.0:
        r, g, b, = (
            255,
            int(255 - 255 * 4 * (i - 0.75)),
            0,
        )
    elif i == 1.0:
        r, g, b = 255, 0, 0
    else:
        r, g, b = 0, 0, 0
    if not normalize:
        return r, g, b
    return r / 255.0, g / 255.0, b / 255.0


def i_to_red(i, normalize=False):
    """Convert a number between 0.0 and 1.0 to a shade of red.

    .. deprecated:: 1.14
        Use :class:`~compas.colors.Color` instead.

    Parameters
    ----------
    i : float
        A number between 0.0 and 1.0.
    normalize : bool, optional
        If True, normalize the resulting RGB values.
        Default is to return integer values ranging from 0 to 255.

    Returns
    -------
    tuple
        The RGB values of the color corresponding to the provided number.
        If `normalize` is true, the RGB values are normalized to values between 0.0 and 1.0.
        If `normalize` is false, the RGB values are integers between 0 and 255.

    Examples
    --------
    >>> i_to_red(1.0)
    (255, 0, 0)
    >>> i_to_red(0.0)
    (255, 255, 255)

    """
    i = max(i, 0.0)
    i = min(i, 1.0)
    g = b = min((1 - i) * 255, 255)
    if not normalize:
        return 255, int(g), int(b)
    return 1.0, g / 255, b / 255


def i_to_green(i, normalize=False):
    """Convert a number between 0.0 and 1.0 to a shade of green.

    .. deprecated:: 1.14
        Use :class:`~compas.colors.Color` instead.

    Parameters
    ----------
    i : float
        A number between 0.0 and 1.0.
    normalize : bool, optional
        If True, normalize the resulting RGB values.
        Default is to return integer values ranging from 0 to 255.

    Returns
    -------
    tuple
        The RGB values of the color corresponding to the provided number.
        If `normalize` is true, the RGB values are normalized to values between 0.0 and 1.0.
        If `normalize` is false, the RGB values are integers between 0 and 255.

    Examples
    --------
    >>> i_to_green(1.0)
    (0, 255, 0)
    >>> i_to_green(0.0)
    (255, 255, 255)

    """
    i = max(i, 0.0)
    i = min(i, 1.0)
    r = b = min((1 - i) * 255, 255)
    if not normalize:
        return int(r), 255, int(b)
    return r / 255, 1.0, b / 255


def i_to_blue(i, normalize=False):
    """Convert a number between 0.0 and 1.0 to a shade of blue.

    .. deprecated:: 1.14
        Use :class:`~compas.colors.Color` instead.

    Parameters
    ----------
    i : float
        A number between 0.0 and 1.0.
    normalize : bool, optional
        If True, normalize the resulting RGB values.
        Default is to return integer values ranging from 0 to 255.

    Returns
    -------
    tuple
        The RGB values of the color corresponding to the provided number.
        If `normalize` is true, the RGB values are normalized to values between 0.0 and 1.0.
        If `normalize` is false, the RGB values are integers between 0 and 255.

    Examples
    --------
    >>> i_to_blue(1.0)
    (0, 0, 255)
    >>> i_to_blue(0.0)
    (255, 255, 255)

    """
    i = max(i, 0.0)
    i = min(i, 1.0)
    r = g = min((1 - i) * 255, 255)
    if not normalize:
        return int(r), int(g), 255
    return r / 255, g / 255, 1.0


def i_to_white(i, normalize=False):
    """Convert a number between 0.0 and 1.0 to a shade of white.

    .. deprecated:: 1.14
        Use :class:`~compas.colors.Color` instead.

    Parameters
    ----------
    i : float
        A number between 0.0 and 1.0.
    normalize : bool, optional
        If True, normalize the resulting RGB values.
        Default is to return integer values ranging from 0 to 255.

    Returns
    -------
    tuple
        The RGB values of the color corresponding to the provided number.
        If `normalize` is true, the RGB values are normalized to values between 0.0 and 1.0.
        If `normalize` is false, the RGB values are integers between 0 and 255.

    Examples
    --------
    >>> i_to_white(1.0)
    (255, 255, 255)
    >>> i_to_white(0.0)
    (0, 0, 0)

    """
    i = max(i, 0.0)
    i = min(i, 1.0)
    rgb = min(i * 255, 255)
    if not normalize:
        return int(rgb), int(rgb), int(rgb)
    rgb = rgb / 255
    return rgb, rgb, rgb


def i_to_black(i, normalize=False):
    """Convert a number between 0.0 and 1.0 to a shade of black.

    .. deprecated:: 1.14
        Use :class:`~compas.colors.Color` instead.

    Parameters
    ----------
    i : float
        A number between 0.0 and 1.0.
    normalize : bool, optional
        If True, normalize the resulting RGB values.
        Default is to return integer values ranging from 0 to 255.

    Returns
    -------
    tuple
        The RGB values of the color corresponding to the provided number.
        If `normalize` is true, the RGB values are normalized to values between 0.0 and 1.0.
        If `normalize` is false, the RGB values are integers between 0 and 255.

    Examples
    --------
    >>> i_to_black(1.0)
    (0, 0, 0)
    >>> i_to_black(0.0)
    (255, 255, 255)

    """
    i = max(i, 0.0)
    i = min(i, 1.0)
    rgb = min((1 - i) * 255, 255)
    if not normalize:
        return int(rgb), int(rgb), int(rgb)
    rgb = rgb / 255
    return rgb, rgb, rgb


class Colormap(object):
    """Convenience class for converting a data range into a corresponding RGB color range.

    .. deprecated:: 1.14
        Use :class:`~compas.colors.ColorMap` instead.

    Parameters
    ----------
    data : list
        A list of data points.
    spec : {'rgb', 'red', 'green', 'blue', 'white', 'black'}
        A color specification.

    Class Attributes
    ----------------
    colorfuncs : dict[str, callable]
        A dictionary mapping color specification names to corresponding converters.

    Examples
    --------
    >>> data = list(range(10))
    >>> cmap = Colormap(data, 'rgb')
    >>> for d in data:
    ...     cmap(d)
    ...
    (0, 0, 255)
    (0, 113, 255)
    (0, 226, 255)
    (0, 255, 170)
    (0, 255, 56)
    (56, 255, 0)
    (169, 255, 0)
    (255, 226, 0)
    (255, 113, 0)
    (255, 0, 0)

    """

    colorfuncs = {
        "rgb": i_to_rgb,
        "red": i_to_red,
        "green": i_to_green,
        "blue": i_to_blue,
        "white": i_to_white,
        "black": i_to_black,
    }

    def __init__(self, data, spec):
        self.data = data
        self.dmin = min(data)
        self.dmax = max(data)
        self.dspan = self.dmax - self.dmin
        self.colorfunc = Colormap.colorfuncs[spec]

    def __call__(self, value):
        i = (value - self.dmin) / (self.dspan)
        return self.colorfunc(i)


def is_color_rgb(color):
    """Is a color in a valid RGB format.

    .. deprecated:: 1.14
        Use :class:`~compas.colors.Color` instead.

    Parameters
    ----------
    color : [int, int, int] | [float, float, float]
        The color object.

    Returns
    -------
    bool
        True, if the color object is in RGB format.
        False, otherwise.

    Examples
    --------
    >>> color = (255, 0, 0)
    >>> is_color_rgb(color)
    True
    >>> color = (1.0, 0.0, 0.0)
    >>> is_color_rgb(color)
    True
    >>> color = (1.0, 0, 0)
    >>> is_color_rgb(color)
    False
    >>> color = (255, 0.0, 0.0)
    >>> is_color_rgb(color)
    False
    >>> color = (256, 0, 0)
    >>> is_color_rgb(color)
    False

    """
    if isinstance(color, (tuple, list)):
        if len(color) == 3:
            if all(isinstance(c, float) for c in color):
                if all(c >= 0.0 and c <= 1.0 for c in color):
                    return True
            elif all(isinstance(c, int) for c in color):
                if all(c >= 0 and c <= 255 for c in color):
                    return True
    return False


def is_color_hex(color):
    """Is a color in a valid HEX format.

    .. deprecated:: 1.14
        Use :class:`~compas.colors.Color` instead.

    Parameters
    ----------
    color : str
        The color object.

    Returns
    -------
    bool
        True, if the color object is in HEX format.
        False, otherwise.

    Examples
    --------
    >>> is_color_hex("#ff0000")
    True
    >>> is_color_hex("#f00")
    True
    >>> is_color_hex("#f000")
    False
    >>> is_color_hex("#ff000")
    False

    """
    if isinstance(color, basestring):
        match = re.search(r"^#(?:[0-9a-fA-F]{3}){1,2}$", color)
        if match:
            return True
        return False
    return False


def rgb_to_rgb(rgb, g=None, b=None):
    """Convert an RGB color specification to an integer-based RGB color specification.

    .. deprecated:: 1.14
        Use :class:`~compas.colors.Color` instead.

    Parameters
    ----------
    rgb : int or float | [int, int, int] | [float, float, float]
        A full RGB color specification, or an integer or a float representing the value of the red component.
    g : int | float, optional
        The green component.
        This parameter is ignored if `rgb` is a full color specification.
    b : int | float, optional
        The blue component.
        This parameter is ignored if `rgb` is a full color specification.

    Returns
    -------
    tuple[int, int, int]
        Three RGB color components in integer format, each in the range of 0-255.

    Examples
    --------
    >>> rgb_to_rgb((255, 0.0, 0.0))
    (255, 0, 0)
    >>> rgb_to_rgb((255, 0, 0))
    (255, 0, 0)
    >>> rgb_to_rgb((1.0, 0, 0))
    (255, 0, 0)
    >>> rgb_to_rgb((1, 0, 0))
    (1, 0, 0)

    """
    if g is None and b is None:
        r, g, b = rgb
    else:
        r = rgb
    r = max(0, min(r, 255))
    g = max(0, min(g, 255))
    b = max(0, min(b, 255))
    if any(isinstance(c, float) for c in (r, g, b)) and all(c <= 1.0 for c in (r, g, b)):
        r = r * 255.0
        g = g * 255.0
        b = b * 255.0
    if all(c > 0.0 and c < 1.0 for c in (r, g, b)):
        r = r * 255.0
        g = g * 255.0
        b = b * 255.0
    return int(r), int(g), int(b)


def rgb_to_hex(rgb, g=None, b=None):
    """Convert an RGB color specification to HEX.

    .. deprecated:: 1.14
        Use :class:`~compas.colors.Color` instead.

    Parameters
    ----------
    rgb : int or float | [int, int, int] | [float, float, float]
        A full RGB color specification, or an integer or a float representing the value of the red component.
    g : int | float, optional
        The green component.
        This parameter is ignored if `rgb` is a full color specification.
    b : int | float, optional
        The blue component.
        This parameter is ignored if `rgb` is a full color specification.

    Returns
    -------
    str
        The corresponding HEX color.

    Examples
    --------
    >>> rgb_to_hex((255, 0.0, 0.0))
    '#ff0000'
    >>> rgb_to_hex((255, 0, 0))
    '#ff0000'
    >>> rgb_to_hex((1.0, 0, 0))
    '#ff0000'
    >>> rgb_to_hex((1, 0, 0))
    '#010000'

    """
    r, g, b = rgb_to_rgb(rgb, g=g, b=b)
    return "#{0:02x}{1:02x}{2:02x}".format(r, g, b)


def hex_to_rgb(value, normalize=False):
    """Convert a HEX color to the corresponding RGB format.

    .. deprecated:: 1.14
        Use :class:`~compas.colors.Color` instead.

    Parameters
    ----------
    value : str
        A HEX color.
    normalize : bool, optional
        Normalize the RGB components if true.

    Returns
    -------
    tuple[int, int, int] | tuple[float, float, float]
        If `normalize` is True, the RGB color with 0-1 float components.
        If `normalize` is False, the RGB color with 0-255 integer components.

    Examples
    --------
    >>> hex_to_rgb('#ff0000')
    (255, 0, 0)
    >>> hex_to_rgb('#ff0000', normalize=True)
    (1.0, 0.0, 0.0)

    """
    value = value.lstrip("#").lower()
    r = HEX_DEC[value[0:2]]
    g = HEX_DEC[value[2:4]]
    b = HEX_DEC[value[4:6]]
    if normalize:
        return r / 255.0, g / 255.0, b / 255.0
    return r, g, b


def color_to_rgb(color, normalize=False):
    """Convert a HEX or RGB color to RGB.

    .. deprecated:: 1.14
        Use :class:`~compas.colors.Color` instead.

    Parameters
    ----------
    color : str | [int, int, int] | [float, float, float]
        The color.
    normalize : bool, optional
        If True, normalize the resulting RGB color components.

    Returns
    -------
    tuple[int, int, int] | tuple[float, float, float]
        If `normalize` is True, the RGB color with 0-1 float components.
        If `normalize` is False, the RGB color with 0-255 integer components.

    Examples
    --------
    >>> color_to_rgb('#ff0000')
    (255, 0, 0)
    >>> color_to_rgb('#ff0000', normalize=True)
    (1.0, 0.0, 0.0)
    >>> color_to_rgb(1.0, normalize=True)
    (1.0, 0.0, 0.0)
    >>> color_to_rgb(1.0)
    (255, 0, 0)
    >>> color_to_rgb((255, 0, 0))
    (255, 0, 0)
    >>> color_to_rgb((255, 0, 0), normalize=True)
    (1.0, 0.0, 0.0)

    """
    if isinstance(color, basestring):
        r, g, b = hex_to_rgb(color)
    elif isinstance(color, float):
        r, g, b = i_to_rgb(color)
    else:
        r, g, b = color
    if not normalize:
        return r, g, b
    if isinstance(r, float):
        return r, g, b
    return r / 255.0, g / 255.0, b / 255.0


def color_to_colordict(color, keys, default=None, colorformat="rgb", normalize=False):
    """Convert a color specification to a dict of colors.

    .. deprecated:: 1.14
        Use :class:`~compas.colors.Color` instead.

    Parameters
    ----------
    color : str | [int, int, int] | [float, float, float] | dict[hashable, [int, int, int]] | dict[hashable, [float, float, float]]
        The base color specification.
        This can be a single color (as HEX or RGB), a list of colors, or a dict of colors.
    keys : sequence[hashable]
        The keys of the color dict.
    default : str | tuple[int, int, int] | tuple[float, float, float], optional
        A valid color specification (HEX or RGB).
    colorformat : Literal['hex', 'rgb'], optional
        The format of the colors in the color dict.
    normalize : bool, optional
        If True and `colorformat` is ``'rgb'``, normalize the color components.

    Returns
    -------
    dict[hashable, tuple[int, int, int]] | dict[hashable, tuple[float, float, float]]
        A dictionary mapping the provided keys to the provided color(s).

    Raises
    ------
    Exception
        If the value of `color`, or the value of `colorformat` is not valid.

    Examples
    --------
    >>> color_to_colordict('#ff0000', [0, 1, 2])
    {0: (255, 0, 0), 1: (255, 0, 0), 2: (255, 0, 0)}
    >>> color_to_colordict('#ff0000', [0, 1, 2], colorformat='hex')
    {0: '#ff0000', 1: '#ff0000', 2: '#ff0000'}
    >>> color_to_colordict('#ff0000', [0, 1, 2], colorformat='rgb', normalize=True)
    {0: (1.0, 0.0, 0.0), 1: (1.0, 0.0, 0.0), 2: (1.0, 0.0, 0.0)}

    """
    color = color or default
    if color is None:
        return {key: None for key in keys}
    # if input is hex
    if isinstance(color, basestring):
        # and output should be rgb
        if colorformat == "rgb":
            color = hex_to_rgb(color, normalize=normalize)
        return {key: color for key in keys}
    # if input is rgb
    if isinstance(color, (tuple, list)) and len(color) == 3:
        # and output should be hex
        if colorformat == "hex":
            color = rgb_to_hex(color, normalize=normalize)
        # and output should be rgb
        # else:
        #     color = rgb_to_rgb(color, normalize=normalize)
        return {key: color for key in keys}
    if isinstance(color, dict):
        for k, c in color.items():
            # if input is hex
            if isinstance(c, basestring):
                # and output should be rgb
                if colorformat == "rgb":
                    color[k] = hex_to_rgb(c, normalize=normalize)
            # if input is rgb
            elif isinstance(c, (tuple, list)) and len(c) == 3:
                # and output should be hex
                if colorformat == "hex":
                    color[k] = rgb_to_hex(c, normalize=normalize)
                # and output should be rgb
                # else:
                #     color[k] = rgb_to_rgb(c, normalize=normalize)
        return {key: (default if key not in color else color[key]) for key in keys}
    raise Exception("This is not a valid color format: {0}".format(type(color)))


def is_color_light(color):
    r"""Is a color "light".

    .. deprecated:: 1.14
        Use :class:`~compas.colors.Color` instead.

    Parameters
    ----------
    color: str | tuple[float, float, float] | tuple[int, int, int]
        The color specification in HEX or RGB format.

    Returns
    -------
    bool
        True, if the color is light.
        False, otherwise.

    Notes
    -----
    A color is considered "light" if the following is True for normalized RGB components:

    .. math::

        0.2126   \frac{r + 0.055}{1.055}^2.4
        + 0.7152 \frac{g + 0.055}{1.055}^2.4
        + 0.0722 \frac{b + 0.055}{1.055}^2.4 > 0.179

    """
    if is_color_hex(color):
        rgb = hex_to_rgb(color)
    else:
        rgb = color
    r, g, b = rgb_to_rgb(rgb)
    r = r / 255.0
    g = g / 255.0
    b = b / 255.0
    r = ((r + 0.055) / 1.055) ** 2.4
    g = ((g + 0.055) / 1.055) ** 2.4
    b = ((b + 0.055) / 1.055) ** 2.4
    L = 0.2126 * r + 0.7152 * g + 0.0722 * b
    return L > 0.179
