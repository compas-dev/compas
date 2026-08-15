from math import acos
from math import degrees
from math import pi
from typing import Optional
from typing import Sequence

from compas._typing import CoordinateType
from compas.linalg.vectors import cross_vectors
from compas.linalg.vectors import dot_vectors
from compas.linalg.vectors import dot_vectors_xy
from compas.linalg.vectors import length_vector
from compas.linalg.vectors import length_vector_xy
from compas.linalg.vectors import subtract_vectors
from compas.linalg.vectors import subtract_vectors_xy
from compas.tolerance import TOL


def angle_vectors(u: CoordinateType, v: CoordinateType, deg: bool = False, tol: Optional[float] = None) -> float:
    """Compute the smallest angle between two vectors.

    Parameters
    ----------
    u
        XYZ components of the first vector.
    v
        XYZ components of the second vector.
    deg
        If True, returns the angle in degrees.
    tol
        The tolerance for comparing values to zero.
        Default is `TOL.absolute`.

    Returns
    -------
    float
        The smallest angle in radians (in degrees if `deg == True`).
        The angle is always positive.

    Examples
    --------
    >>> angle_vectors([0.0, 1.0, 0.0], [1.0, 0.0, 0.0])
    1.57079

    """
    L = length_vector(u) * length_vector(v)
    if TOL.is_zero(L, tol):
        return 0
    a = dot_vectors(u, v) / L
    a = max(min(a, 1), -1)
    angle = acos(a)

    # a = length_vector(u)
    # b = length_vector(v)
    # if a < tol or b < tol:
    #     return 0
    # c = length_vector(subtract_vectors(u, v))
    # if c < tol:
    #     return 0
    # if b >= c and c >= 0:
    #     mu = c - (a - b)
    # elif c > b and b >= 0:
    #     mu = b - (a - c)
    # else:
    #     raise Exception("Invalid input vectors.")
    # angle = 2 * atan(sqrt(((a - b) + c) * mu / ((a + (b + c)) * ((a - c) + b))))

    # a = normalize_vector(u)
    # b = normalize_vector(v)
    # angle = 2 * atan2(length_vector(subtract_vectors(a, b)), length_vector(add_vectors(a, b)))

    if deg:
        return degrees(angle)
    return angle


def angle_vectors_signed(
    u: CoordinateType,
    v: CoordinateType,
    normal: CoordinateType,
    deg: bool = False,
    tol: Optional[float] = None,
) -> float:
    """Computes the signed angle between two vectors.

    Returns the smallest angle between 2 vectors, with the sign of the angle based on the direction of the normal vector according to the right hand rule of rotation.

    Parameters
    ----------
    u
        XYZ components of the first vector.
    v
        XYZ components of the second vector.
    normal
        XYZ components of the plane's normal spanned by u and v.
    deg
        If True, returns the angle in degrees.
    tol
        The tolerance for comparing values to zero.
        Default is `TOL.absolute`.


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

    if not TOL.is_zero(length_vector(normal_uv), tol):
        if TOL.is_negative(dot_vectors(normal, normal_uv), tol):
            angle *= -1

    if deg:
        return degrees(angle)
    else:
        return angle


def angle_vectors_projected(
    u: Sequence[float],
    v: Sequence[float],
    normal: Sequence[float],
    deg: bool = False,
    tol: Optional[float] = None,
) -> float:
    """Computes the signed angle between two vectors.

    Retuns the angle between 2 vectors projected onto a plane defined by a normal vector.
    This can be positive or negative depending on the direction of the normal vector and the order of the input vectors

    Parameters
    ----------
    u
        XYZ components of the first vector.
    v
        XYZ components of the second vector.
    normal
        XYZ components of the plane's normal spanned by u and v.
    deg
        If True, returns the angle in degrees.
    tol
        The tolerance for comparing values to zero.
        Default is `TOL.absolute`.

    Returns
    -------
    float
        The signed angle in radians (in degrees if deg == True).

    Examples
    --------
    >>> normal = [0.0, 0.0, 1.0]
    >>> angle_vectors_projected([0.0, 1.0, -1.0], [1.0, 0.0, 1.0], normal)
    -1.57079

    """
    u_cross = cross_vectors(u, normal)
    v_cross = cross_vectors(v, normal)

    return angle_vectors_signed(u_cross, v_cross, normal, deg, tol)


def angle_vectors_xy(u: Sequence[float], v: Sequence[float], deg: bool = False, tol: Optional[float] = None) -> float:
    """Compute the smallest angle between the XY components of two vectors.

    Parameters
    ----------
    u
        The first 2D or 3D vector (Z will be ignored).
    v
        The second 2D or 3D vector (Z will be ignored).
    deg
        If True, returns the angle in degrees.
    tol
        The tolerance for comparing values to zero.
        Default is `TOL.absolute`.

    Returns
    -------
    float
        The smallest angle in radians (in degrees if `deg == True`).
        The angle is always positive.

    """
    L = length_vector_xy(u) * length_vector_xy(v)
    if TOL.is_zero(L, tol):
        return 0
    a = dot_vectors_xy(u, v) / L
    a = max(min(a, 1), -1)
    if deg:
        return degrees(acos(a))
    return acos(a)


def angle_points(a: Sequence[float], b: Sequence[float], c: Sequence[float], deg: bool = False) -> float:
    r"""Compute the smallest angle between the vectors defined by three points.

    Parameters
    ----------
    a
        XYZ coordinates.
    b
        XYZ coordinates.
    c
        XYZ coordinates.
    deg
        If True, returns the angle in degrees.

    Returns
    -------
    float
        The smallest angle in radians (in degrees if `deg == True`).
        The angle is always positive.

    Notes
    -----
    The vectors are defined in the following way

    $$
        \mathbf{u} = \mathbf{b} - \mathbf{a} \\
        \mathbf{v} = \mathbf{c} - \mathbf{a}
    $$

    Z components may be provided, but are simply ignored.

    """
    u = subtract_vectors(b, a)
    v = subtract_vectors(c, a)
    return angle_vectors(u, v, deg)


def angle_points_xy(a: Sequence[float], b: Sequence[float], c: Sequence[float], deg: bool = False) -> float:
    r"""Compute the smallest angle between the vectors defined by the XY components of three points.

    Parameters
    ----------
    a
        XY(Z) coordinates of a 2D or 3D point (Z will be ignored).
    b
        XY(Z) coordinates of a 2D or 3D point (Z will be ignored).
    c
        XY(Z) coordinates of a 2D or 3D point (Z will be ignored).
    deg
        If True, returns the angle in degrees.

    Returns
    -------
    float
        The smallest angle in radians (in degrees if `deg == True`).
        The angle is always positive.

    Notes
    -----
    The vectors are defined in the following way

    $$
        \mathbf{u} = \mathbf{b} - \mathbf{a} \\
        \mathbf{v} = \mathbf{c} - \mathbf{a}
    $$

    Z components may be provided, but are simply ignored.

    """
    u = subtract_vectors_xy(b, a)
    v = subtract_vectors_xy(c, a)
    return angle_vectors_xy(u, v, deg)


def angles_vectors(u: CoordinateType, v: CoordinateType, deg: bool = False) -> tuple[float, float]:
    """Compute the the 2 angles formed by a pair of vectors.

    Parameters
    ----------
    u
        XYZ components of the first vector.
    v
        XYZ components of the second vector.
    deg
        If True, returns the angle in degrees.

    Returns
    -------
    tuple[float, float]
        The smallest angle and the other angle, in radians or degrees if `deg == True`.

    """
    if deg:
        a = angle_vectors(u, v, deg)
        return a, 360.0 - a
    a = angle_vectors(u, v)
    return a, pi * 2 - a


def angles_vectors_xy(u: Sequence[float], v: Sequence[float], deg: bool = False) -> tuple[float, float]:
    """Compute the angles between the XY components of two vectors.

    Parameters
    ----------
    u
        XY(Z) coordinates of the first vector.
    v
        XY(Z) coordinates of the second vector.
    deg
        If True, returns the angle in degrees.

    Returns
    -------
    tuple[float, float]
        The smallest angle and the other angle, in radians or degrees if `deg == True`.

    Notes
    -----
    Z components may be provided, but are simply ignored.

    """
    if deg:
        a = angle_vectors_xy(u, v, deg)
        return a, 360.0 - a
    a = angle_vectors_xy(u, v)
    return a, pi * 2 - a


def angles_points(a: Sequence[float], b: Sequence[float], c: Sequence[float], deg: bool = False) -> tuple[float, float]:
    r"""Compute the two angles between two vectors defined by three points.

    Parameters
    ----------
    a
        XYZ coordinates.
    b
        XYZ coordinates.
    c
        XYZ coordinates.
    deg
        If True, returns the angle in degrees.

    Returns
    -------
    tuple[float, float]
        The smallest angle and the other angle, in radians or degrees if `deg == True`.

    Notes
    -----
    The vectors are defined in the following way

    $$
        \mathbf{u} = \mathbf{b} - \mathbf{a} \\
        \mathbf{v} = \mathbf{c} - \mathbf{a}
    $$

    """
    u = subtract_vectors(b, a)
    v = subtract_vectors(c, a)
    return angles_vectors(u, v, deg)


def angles_points_xy(a: Sequence[float], b: Sequence[float], c: Sequence[float], deg: bool = False) -> tuple[float, float]:
    r"""Compute the two angles between the two vectors defined by the XY components of three points.

    Parameters
    ----------
    a
        XY(Z) coordinates.
    b
        XY(Z) coordinates.
    c
        XY(Z) coordinates.
    deg
        If True, returns the angle in degrees.

    Returns
    -------
    tuple[float, float]
        The smallest angle and the other angle, in radians or degrees if `deg == True`.

    Notes
    -----
    The vectors are defined in the following way

    $$
        \mathbf{u} = \mathbf{b} - \mathbf{a} \\
        \mathbf{v} = \mathbf{c} - \mathbf{a}
    $$

    Z components may be provided, but are simply ignored.

    """
    u = subtract_vectors_xy(b, a)
    v = subtract_vectors_xy(c, a)
    return angles_vectors_xy(u, v, deg)


def angle_planes(
    a: tuple[Sequence[float], Sequence[float]],
    b: tuple[Sequence[float], Sequence[float]],
    deg: bool = False,
) -> float:
    """Compute the smallest angle between the two normal vectors of two planes.

    Parameters
    ----------
    a
        The first plane.
    b
        The second plane.
    deg
        If True, returns the angle in degrees.

    Returns
    -------
    float
        The smallest angle in radians, or in degrees if `deg == True`.

    Examples
    --------
    >>> plane_a = [0.0, 0.0, 0.0], [0.0, 0.0, 1.0]
    >>> plane_b = [0.0, 0.0, 0.0], [1.0, 0.0, 0.0]
    >>> angle_planes(plane_a, plane_b, True)
    90.0

    """
    return angle_vectors(a[1], b[1], deg)
