from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from math import pi
from math import degrees
from math import acos

from compas.geometry.basic import subtract_vectors
from compas.geometry.basic import subtract_vectors_xy
from compas.geometry.basic import dot_vectors
from compas.geometry.basic import dot_vectors_xy
from compas.geometry.basic import length_vector
from compas.geometry.basic import length_vector_xy


__all__ = [
    'angles_vectors',
    'angles_vectors_xy',
    'angles_vectors',
    'angles_vectors_xy',
    'angles_points',
    'angles_points_xy',
    'angle_vectors',
    'angle_vectors_xy',
    'angle_points',
    'angle_points_xy',
]


def angle_vectors(u, v, deg=False):
    """Compute the smallest angle between two vectors.

    Parameters
    ----------
    u : sequence of float
        XYZ components of the first vector.
    v : sequence of float
        XYZ components of the second vector.
    deg : boolean
        returns angle in degrees if True

    Returns
    -------
    float
        The smallest angle in radians (in degrees if deg == True).
        The angle is always positive.

    Examples
    --------
    >>> angle_vectors([0.0, 1.0, 0.0], [1.0, 0.0, 0.0])

    """
    a = dot_vectors(u, v) / (length_vector(u) * length_vector(v))
    a = max(min(a, 1), -1)

    if deg:
        return degrees(acos(a))
    return acos(a)


def angle_vectors_xy(u, v, deg=False):
    """Compute the smallest angle between the XY components of two vectors.

    Parameters
    ----------
    u : sequence of float
        The first 2D or 3D vector (Z will be ignored).
    v : sequence of float)
        The second 2D or 3D vector (Z will be ignored).
    deg : boolean
        returns angle in degrees if True

    Returns
    -------
    float
        The smallest angle between the vectors in radians (in degrees if deg == True).
        The angle is always positive.

    Examples
    --------
    >>>

    """
    a = dot_vectors_xy(u, v) / (length_vector_xy(u) * length_vector_xy(v))
    a = max(min(a, 1), -1)
    if deg:
        return degrees(acos(a))
    return acos(a)


def angle_points(a, b, c, deg=False):
    r"""Compute the smallest angle between the vectors defined by three points.

    Parameters
    ----------
    a : sequence of float
        XYZ coordinates.
    b : sequence of float
        XYZ coordinates.
    c : sequence of float
        XYZ coordinates.
    deg : boolean
        returns angle in degrees if True

    Returns
    -------
    float
        The smallest angle between the vectors in radians (in degrees if deg == True).
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
    a : sequence of float
        XY(Z) coordinates of a 2D or 3D point (Z will be ignored).
    b : sequence of float)
        XY(Z) coordinates of a 2D or 3D point (Z will be ignored).
    c : sequence of float)
        XY(Z) coordinates of a 2D or 3D point (Z will be ignored).
    deg : boolean
        returns angle in degrees if True

    Returns
    -------
    float
        The smallest angle between the vectors in radians (in degrees if deg == True).
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
    u : sequence of float
        XYZ components of the first vector.
    v : sequence of float
        XYZ components of the second vector.
    deg : boolean
        returns angles in degrees if True

    Returns
    -------
    tuple
        The smallest angle between the vectors in radians (in degrees if deg == True).
        The smallest angle is returned first.

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
    u : sequence of float
        XY(Z) coordinates of the first vector.
    v : sequence of float
        XY(Z) coordinates of the second vector.
    deg : boolean
        returns angles in degrees if True

    Returns
    -------
    tuple
        The smallest angle between the vectors in radians (in degrees if deg == True).
        The smallest angle is returned first.

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
    a : sequence of float)
        XYZ coordinates.
    b : sequence of float)
        XYZ coordinates.
    c : sequence of float)
        XYZ coordinates.
    deg : boolean
        returns angles in degrees if True

    Returns
    -------
    tuple
        The smallest angle between the vectors in radians (in degrees if deg == True).
        The smallest angle is returned first.

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
    a : sequence of float)
        XY(Z) coordinates.
    b : sequence of float)
        XY(Z) coordinates.
    c : sequence of float)
        XY(Z) coordinates.
    deg : boolean
        returns angles in degrees if True

    Returns
    -------
    tuple
        The smallest angle between the vectors in radians (in degrees if deg == True).
        The smallest angle is returned first.

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


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    deg = False

    u = [1., 0., 0.]
    v = [1., 1., 0.]
    o = [0., 0., 0.]

    print (angle_vectors(u, v, deg))
    print (angle_vectors_xy(u, v, deg))

    print (angle_points(o, u, v, deg))
    print (angle_points_xy(o, u, v, deg))

    print (angles_vectors(u, v, deg))
    print (angles_vectors_xy(u, v, deg))

    print (angles_points(o, u, v, deg))
    print (angles_points_xy(o, u, v, deg))
