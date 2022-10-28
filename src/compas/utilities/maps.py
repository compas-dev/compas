from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas


__all__ = [
    "geometric_key",
    "reverse_geometric_key",
    "geometric_key_xy",
]


def geometric_key(xyz, precision=None, sanitize=True):
    """Convert XYZ coordinates to a string that can be used as a dict key.

    Parameters
    ----------
    xyz : list[float]
        The XYZ coordinates.
    precision : str, optional
        A formatting option that specifies the precision of the
        individual numbers in the string.
        Supported values are any float precision (e.g. ``'3f'``), or decimal integer (``'d'``).
        Default is ``None``, in which case the global precision setting will be used (:attr:`compas.PRECISION`).
    sanitize : bool, optional
        If True, minus signs ("-") will be removed from values that are equal to zero up to the given precision.

    Returns
    -------
    str
        The string representation of the given coordinates.

    See also
    --------
    geometric_key_xy

    Examples
    --------
    >>> from math import pi
    >>> geometric_key([pi, pi, pi])
    '3.142,3.142,3.142'

    """
    x, y, z = xyz
    if not precision:
        precision = compas.PRECISION
    if precision == "d":
        return "{0},{1},{2}".format(int(x), int(y), int(z))
    if sanitize:
        minzero = "-{0:.{1}}".format(0.0, precision)
        if "{0:.{1}}".format(x, precision) == minzero:
            x = 0.0
        if "{0:.{1}}".format(y, precision) == minzero:
            y = 0.0
        if "{0:.{1}}".format(z, precision) == minzero:
            z = 0.0
    return "{0:.{3}},{1:.{3}},{2:.{3}}".format(x, y, z, precision)


def reverse_geometric_key(gkey):
    """Reverse a geometric key string into xyz coordinates.

    Parameters
    ----------
    gkey : str
        A geometric key.

    Returns
    -------
    list[float]
        A list of XYZ coordinates.

    See Also
    --------
    geometric_key

    Examples
    --------
    >>> from math import pi
    >>> xyz = [pi, pi, pi]
    >>> gkey = geometric_key(xyz)
    >>> reverse_geometric_key(gkey)
    [3.142, 3.142, 3.142]

    """
    xyz = gkey.split(",")
    return [float(i) for i in xyz]


def geometric_key_xy(xy, precision=None, sanitize=True):
    """Convert XY coordinates to a string that can be used as a dict key.

    Parameters
    ----------
    xy : list[float]
        The XY(Z) coordinates.
    precision : str, optional
        A formatting option that specifies the precision of the
        individual numbers in the string.
        Supported values are any float precision (e.g. ``'3f'``), or decimal integer (``'d'``).
        Default is ``None``, inwhich case the global precision setting will be used (``compas.PRECISION``).
    sanitize : bool, optional
        If True, minus signs ("-") will be removed from values that are equal to zero up to the given precision.

    Returns
    -------
    str
        The string representation of the given coordinates.

    See also
    --------
    geometric_key

    Examples
    --------
    >>> from math import pi
    >>> geometric_key_xy([pi, pi, pi])
    '3.142,3.142'

    """
    x, y = xy[:2]
    if not precision:
        precision = compas.PRECISION
    if precision == "d":
        return "{0},{1}".format(int(x), int(y))
    if sanitize:
        minzero = "-{0:.{1}}".format(0.0, precision)
        if "{0:.{1}}".format(x, precision) == minzero:
            x = 0.0
        if "{0:.{1}}".format(y, precision) == minzero:
            y = 0.0
    return "{0:.{2}},{1:.{2}}".format(x, y, precision)
