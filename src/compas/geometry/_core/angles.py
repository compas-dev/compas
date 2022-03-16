from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from math import pi
from math import degrees
from math import acos

from compas.geometry._core import subtract_vectors
from compas.geometry._core import subtract_vectors_xy
from compas.geometry._core import dot_vectors
from compas.geometry._core import dot_vectors_xy
from compas.geometry._core import length_vector
from compas.geometry._core import length_vector_xy
from compas.geometry._core import cross_vectors


__all__ = [
    'angles_vectors',
    'angles_vectors_xy',
    'angles_vectors',
    'angles_vectors_xy',
    'angles_points',
    'angles_points_xy',
    'angle_vectors',
    'angle_vectors_signed',
    'angle_vectors_xy',
    'angle_points',
    'angle_points_xy',
    'angle_planes',
]


def angle_vectors(u, v, deg=False, tol=0.0):
    """Compute the smallest angle between two vectors.

    Parameters
    ----------
    u : [float, float, float] | :class:`~compas.geometry.Vector`
        XYZ components of the first vector.
    v : [float, float, float] | :class:`~compas.geometry.Vector`
        XYZ components of the second vector.
    deg : bool, optional
        If True, returns the angle in degrees.
    tol : float, optional
        Tolerance for the length of the vectors.

    Returns
    -------
    float
        The smallest angle in radians (in degrees if ``deg == True``).
        The angle is always positive.

    Examples
    --------
    >>> angle_vectors([0.0, 1.0, 0.0], [1.0, 0.0, 0.0])
    1.57079

    """
    L = length_vector(u) * length_vector(v)
    if tol and L < tol:
        return 0
    a = dot_vectors(u, v) / L
    a = max(min(a, 1), -1)

    if deg:
        return degrees(acos(a))
    return acos(a)


def angle_vectors_signed(u, v, normal, deg=False, threshold=1e-3):
    """Computes the signed angle between two vectors.

    It calculates the angle such that rotating vector u about the normal by
    angle would result in a vector that looks into the same direction as v.

    Parameters
    ----------
    u : [float, float, float] | :class:`~compas.geometry.Vector`
        XYZ components of the first vector.
    v : [float, float, float] | :class:`~compas.geometry.Vector`
        XYZ components of the second vector.
    normal : [float, float, float] | :class:`~compas.geometry.Vector`
        XYZ components of the plane's normal spanned by u and v.
    deg : bool, optional
        If True, returns the angle in degrees.
    threshold : float, optional
        The threshold (radians) used to consider if the angle is zero.

    Returns
    -------
    float
        The signed angle in radians (in degrees if deg == True).

    Examples
    --------
    >>> normal = [0.0, 0.0, 1.0]
    >>> angle_vectors_signed([0.0, 1.0, 0.0], [1.0, 0.0, 0.0], normal)
    -1.57079
    """
    angle = angle_vectors(u, v)
    normal_uv = cross_vectors(u, v)

    if length_vector(normal_uv) > threshold:
        # check if normal_uv has the same direction as normal
        angle_btw_normals = angle_vectors(normal, normal_uv)
        if angle_btw_normals > threshold:
            angle *= -1

    if deg:
        return degrees(angle)
    else:
        return angle


def angle_vectors_xy(u, v, deg=False, tol=1e-4):
    """Compute the smallest angle between the XY components of two vectors.

    Parameters
    ----------
    u : [float, float] or [float, float, float] | :class:`~compas.geometry.Vector`
        The first 2D or 3D vector (Z will be ignored).
    v : [float, float] or [float, float, float] | :class:`~compas.geometry.Vector`
        The second 2D or 3D vector (Z will be ignored).
    deg : bool, optional
        If True, returns the angle in degrees.
    tol : float, optional
        Tolerance for the length of the vectors.

    Returns
    -------
    float
        The smallest angle in radians (in degrees if ``deg == True``).
        The angle is always positive.

    Examples
    --------
    >>>

    """
    L = length_vector_xy(u) * length_vector_xy(v)
    if L < tol:
        return 0
    a = dot_vectors_xy(u, v) / L
    a = max(min(a, 1), -1)
    if deg:
        return degrees(acos(a))
    return acos(a)


def angle_points(a, b, c, deg=False):
    r"""Compute the smallest angle between the vectors defined by three points.

    Parameters
    ----------
    a : [float, float, float] | :class:`~compas.geometry.Point`
        XYZ coordinates.
    b : [float, float, float] | :class:`~compas.geometry.Point`
        XYZ coordinates.
    c : [float, float, float] | :class:`~compas.geometry.Point`
        XYZ coordinates.
    deg : bool, optional
        If True, returns the angle in degrees.

    Returns
    -------
    float
        The smallest angle in radians (in degrees if ``deg == True``).
        The angle is always positive.

    Notes
    -----
    The vectors are defined in the following way

    .. math::

        \mathbf{u} = \mathbf{b} - \mathbf{a} \\
        \mathbf{v} = \mathbf{c} - \mathbf{a}

    Z components may be provided, but are simply ignored.

    """
    u = subtract_vectors(b, a)
    v = subtract_vectors(c, a)
    return angle_vectors(u, v, deg)


def angle_points_xy(a, b, c, deg=False):
    r"""Compute the smallest angle between the vectors defined by the XY components of three points.

    Parameters
    ----------
    a : [float, float] or [float, float, float] | :class:`~compas.geometry.Point`
        XY(Z) coordinates of a 2D or 3D point (Z will be ignored).
    b : [float, float] or [float, float, float] | :class:`~compas.geometry.Point`
        XY(Z) coordinates of a 2D or 3D point (Z will be ignored).
    c : [float, float] or [float, float, float] | :class:`~compas.geometry.Point`
        XY(Z) coordinates of a 2D or 3D point (Z will be ignored).
    deg : bool, optional
        If True, returns the angle in degrees.

    Returns
    -------
    float
        The smallest angle in radians (in degrees if ``deg == True``).
        The angle is always positive.

    Notes
    -----
    The vectors are defined in the following way

    .. math::

        \mathbf{u} = \mathbf{b} - \mathbf{a} \\
        \mathbf{v} = \mathbf{c} - \mathbf{a}

    Z components may be provided, but are simply ignored.

    """
    u = subtract_vectors_xy(b, a)
    v = subtract_vectors_xy(c, a)
    return angle_vectors_xy(u, v, deg)


def angles_vectors(u, v, deg=False):
    """Compute the the 2 angles formed by a pair of vectors.

    Parameters
    ----------
    u : [float, float, float] | :class:`~compas.geometry.Vector`
        XYZ components of the first vector.
    v : [float, float, float] | :class:`~compas.geometry.Vector`
        XYZ components of the second vector.
    deg : bool, optional
        If True, returns the angle in degrees.

    Returns
    -------
    float
        The smallest angle in radians, or in degrees if ``deg == True``.
    float
        The other angle.

    Examples
    --------
    >>>

    """
    if deg:
        a = angle_vectors(u, v, deg)
        return a, 360. - a
    a = angle_vectors(u, v)
    return a, pi * 2 - a


def angles_vectors_xy(u, v, deg=False):
    """Compute the angles between the XY components of two vectors.

    Parameters
    ----------
    u : [float, float] or [float, float, float] | :class:`~compas.geometry.Vector`
        XY(Z) coordinates of the first vector.
    v : [float, float] or [float, float, float] | :class:`~compas.geometry.Vector`
        XY(Z) coordinates of the second vector.
    deg : bool, optional
        If True, returns the angle in degrees.

    Returns
    -------
    float
        The smallest angle in radians, or in degrees if ``deg == True``.
    float
        The other angle.

    Notes
    -----
    Z components may be provided, but are simply ignored.

    Examples
    --------
    >>>

    """
    if deg:
        a = angle_vectors_xy(u, v, deg)
        return a, 360. - a
    a = angle_vectors_xy(u, v)
    return a, pi * 2 - a


def angles_points(a, b, c, deg=False):
    r"""Compute the two angles between two vectors defined by three points.

    Parameters
    ----------
    a : [float, float, float] | :class:`~compas.geometry.Point`
        XYZ coordinates.
    b : [float, float, float] | :class:`~compas.geometry.Point`
        XYZ coordinates.
    c : [float, float, float] | :class:`~compas.geometry.Point`
        XYZ coordinates.
    deg : bool, optional
        If True, returns the angle in degrees.

    Returns
    -------
    float
        The smallest angle in radians, or in degrees if ``deg == True``.
    float
        The other angle.

    Notes
    -----
    The vectors are defined in the following way

    .. math::

        \mathbf{u} = \mathbf{b} - \mathbf{a} \\
        \mathbf{v} = \mathbf{c} - \mathbf{a}

    Examples
    --------
    >>>

    """
    u = subtract_vectors(b, a)
    v = subtract_vectors(c, a)
    return angles_vectors(u, v, deg)


def angles_points_xy(a, b, c, deg=False):
    r"""Compute the two angles between the two vectors defined by the XY components of three points.

    Parameters
    ----------
    a : [float, float] or [float, float, float] | :class:`~compas.geometry.Point`
        XY(Z) coordinates.
    b : [float, float] or [float, float, float] | :class:`~compas.geometry.Point`
        XY(Z) coordinates.
    c : [float, float] or [float, float, float] | :class:`~compas.geometry.Point`
        XY(Z) coordinates.
    deg : bool, optional
        If True, returns the angle in degrees.

    Returns
    -------
    float
        The smallest angle in radians, or in degrees if ``deg == True``.
    float
        The other angle.

    Notes
    -----
    The vectors are defined in the following way

    .. math::

        \mathbf{u} = \mathbf{b} - \mathbf{a} \\
        \mathbf{v} = \mathbf{c} - \mathbf{a}

    Z components may be provided, but are simply ignored.

    Examples
    --------
    >>>

    """
    u = subtract_vectors_xy(b, a)
    v = subtract_vectors_xy(c, a)
    return angles_vectors_xy(u, v, deg)


def angle_planes(a, b, deg=False):
    """Compute the smallest angle between the two normal vectors of two planes.

    Parameters
    ----------
    a : [point, vector] | :class:`~compas.geometry.Plane`
        The first plane.
    b : [point, vector] | :class:`~compas.geometry.Plane`
        The second plane.
    deg : bool, optional
        If True, returns the angle in degrees.

    Returns
    -------
    float
        The smallest angle in radians, or in degrees if ``deg == True``.
    float
        The other angle.

    Examples
    --------
    >>> plane_a = [0.0, 0.0, 0.0], [0.0, 0.0, 1.0]
    >>> plane_b = [0.0, 0.0, 0.0], [1.0, 0.0, 0.0]
    >>> angle_planes(plane_a, plane_b, True)
    90.0
    """
    return angle_vectors(a[1], b[1], deg)
