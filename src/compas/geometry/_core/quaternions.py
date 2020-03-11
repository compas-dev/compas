"""
This module contains functions that operate on and/or return quaternions.

Notes
-----
The default convention to represent a quaternion :math:`q` in this module is by four real values **w**, **x**, **y**, **z**.
The first value **w** is the scalar (real) part, and **x**, **y**, **z** form the vector (complex, imaginary) part [1]_, so that:

:math:`q = w + xi + yj + zk`

where :math:`i, j, k` are basis components with following multiplication rules [2]_:

:math:`ii = jj = kk = ijk = -1`

:math:`ij = k,\\qquad ji = -k`

:math:`jk = i,\\qquad kj = -i`

:math:`ki = j,\\qquad ik = -j`

Quaternions are associative but not commutative.

**Quaternion as rotation.**
A rotation through an angle :math:`\\theta` around an axis defined by a euclidean unit vector :math:`u = u_{x}i + u_{y}j + u_{z}k`
can be represented as a quaternion:

:math:`q = cos(\\frac{\\theta}{2}) + sin(\\frac{\\theta}{2})  [u_{x}i + u_{y}j + u_{z}k]`

i.e.:

:math:`w = cos(\\frac{\\theta}{2})`

:math:`x = sin(\\frac{\\theta}{2})  u_{x}`

:math:`y = sin(\\frac{\\theta}{2})  u_{y}`

:math:`z = sin(\\frac{\\theta}{2})  u_{z}`

For a quaternion to represent a rotation or orientation, it must be unit-length.
A quaternion representing a rotation :math:`p` resulting from applying a rotation :math:`r` to a rotation :math:`q`, i.e.:
:math:`p = rq`,
is also unit-length.

References
----------
.. [1] http://mathworld.wolfram.com/Quaternion.html
.. [2] http://mathworld.wolfram.com/HamiltonsRules.html
.. [3] https://github.com/matthew-brett/transforms3d/blob/master/transforms3d/quaternions.py
"""
import math

from compas.geometry._core import allclose


__all__ = [
    'quaternion_norm',
    'quaternion_unitize',
    'quaternion_is_unit',
    'quaternion_multiply',
    'quaternion_canonize',
    'quaternion_conjugate',
]

ATOL = 1e-6  # absolute tolerance


def quaternion_norm(q):
    """Calculates the length (euclidean norm) of a quaternion.

    Parameters
    ----------
    q : list
        Quaternion as a list of four real values ``[w, x, y, z]``.

    Returns
    -------
    float
        The length (euclidean norm) of a quaternion.

    References
    ----------
    .. _mathworld quaternion norm: http://mathworld.wolfram.com/QuaternionNorm.html

    """
    return math.sqrt(sum([x * x for x in q]))


def quaternion_unitize(q):
    """Makes a quaternion unit-length.

    Parameters
    ----------
    q : list
        Quaternion as a list of four real values ``[w, x, y, z]``.

    Returns
    -------
    list
        Quaternion of length 1 as a list of four real values ``[nw, nx, ny, nz]``.
    """
    n = quaternion_norm(q)
    if allclose([n], [0.0], ATOL):
        raise ValueError("The given quaternion has zero length.")
    else:
        return [x / n for x in q]


def quaternion_is_unit(q, tol=ATOL):
    """Checks if a quaternion is unit-length.

    Parameters
    ----------
    q : list
        Quaternion as a list of four real values ``[w, x, y, z]``.
    tol : float, optional
        Requested decimal precision.

    Returns
    -------
    bool
        ``True`` if the quaternion is unit-length, and ``False`` if otherwise.
    """
    n = quaternion_norm(q)
    return allclose([n], [1.0], tol)


def quaternion_multiply(r, q):
    """Multiplies two quaternions.

    Parameters
    ----------
    r : list
        Quaternion as a list of four real values ``[rw, rx, ry, rz]``.
    q : list
        Quaternion as a list of four real values ``[qw, qx, qy, qz]``.

    Returns
    -------
    list
        Quaternion :math:`p = rq` as a list of four real values ``[pw, px, py, pz]``.

    Notes
    -----
    Multiplication of two quaternions :math:`p = rq` can be interpreted as applying rotation :math:`r` to an orientation :math:`q`,
    provided that both :math:`r` and :math:`q` are unit-length.
    The result is also unit-length.
    Multiplication of quaternions is not commutative!

    References
    ----------
    .. _mathworld quaternion: http://mathworld.wolfram.com/Quaternion.html

    """
    rw, rx, ry, rz = r
    qw, qx, qy, qz = q
    pw = rw*qw - rx*qx - ry*qy - rz*qz
    px = rw*qx + rx*qw + ry*qz - rz*qy
    py = rw*qy - rx*qz + ry*qw + rz*qx
    pz = rw*qz + rx*qy - ry*qx + rz*qw
    return [pw, px, py, pz]


def quaternion_canonize(q):
    """Converts a quaternion into a canonic form if needed.

    Parameters
    ----------
    q : list
        Quaternion as a list of four real values ``[w, x, y, z]``.

    Returns
    -------
    list
        Quaternion in a canonic form as a list of four real values ``[cw, cx, cy, cz]``.

    Notes
    -----
    Canonic form means the scalar component is a non-negative number.
    """
    if q[0] < 0.0:
        return [-x for x in q]
    return q[:]


def quaternion_conjugate(q):
    """Conjugate of a quaternion.

    Parameters
    ----------
    q : list
        Quaternion as a list of four real values ``[w, x, y, z]``.

    Returns
    -------
    list
        Conjugate quaternion as a list of four real values ``[cw, cx, cy, cz]``.

    References
    ----------
    .. _mathworld quaternion conjugate: http://mathworld.wolfram.com/QuaternionConjugate.html
    """
    return [q[0], -q[1], -q[2], -q[3]]


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    import doctest
    doctest.testmod(globs=globals())
