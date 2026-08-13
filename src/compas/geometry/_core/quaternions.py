import math
from typing import Optional
from typing import Sequence

from compas.tolerance import TOL


def quaternion_norm(q: Sequence[float]) -> float:
    """Calculates the length (euclidean norm) of a quaternion.

    Parameters
    ----------
    q
        Sequence of four floats `[w, x, y, z]`.

    Returns
    -------
    float
        The length (euclidean norm) of a quaternion.

    See Also
    --------
    [`quaternion_is_unit`][compas.geometry.quaternion_is_unit]
    [`quaternion_unitize`][compas.geometry.quaternion_unitize]
    [`quaternion_multiply`][compas.geometry.quaternion_multiply]
    [`quaternion_canonize`][compas.geometry.quaternion_canonize]
    [`quaternion_conjugate`][compas.geometry.quaternion_conjugate]

    References
    ----------
    * [Quaternion Norm](https://mathworld.wolfram.com/QuaternionNorm.html)

    """
    return math.sqrt(sum([x * x for x in q]))


def quaternion_unitize(q: Sequence[float]) -> list[float]:
    """Makes a quaternion unit-length.

    Parameters
    ----------
    q
        Sequence of four floats `[w, x, y, z]`.

    Returns
    -------
    list[float]
        Quaternion of length 1 as a list of four real values `[nw, nx, ny, nz]`.

    See Also
    --------
    [`quaternion_is_unit`][compas.geometry.quaternion_is_unit]
    [`quaternion_norm`][compas.geometry.quaternion_norm]
    [`quaternion_multiply`][compas.geometry.quaternion_multiply]
    [`quaternion_canonize`][compas.geometry.quaternion_canonize]
    [`quaternion_conjugate`][compas.geometry.quaternion_conjugate]

    """
    n = quaternion_norm(q)

    if TOL.is_zero(n):
        raise ValueError("The given quaternion has zero length.")

    return [x / n for x in q]


def quaternion_is_unit(q: Sequence[float], tol: Optional[float] = None) -> bool:
    """Checks if a quaternion is unit-length.

    Parameters
    ----------
    q
        Sequence of four floats `[w, x, y, z]`.
    tol
        The tolerance for comparing the quaternion norm to 1.
        Default is `TOL.absolute`.

    Returns
    -------
    bool
        True if the quaternion is unit-length,
        and False if otherwise.

    See Also
    --------
    [`quaternion_unitize`][compas.geometry.quaternion_unitize]
    [`quaternion_norm`][compas.geometry.quaternion_norm]
    [`quaternion_multiply`][compas.geometry.quaternion_multiply]
    [`quaternion_canonize`][compas.geometry.quaternion_canonize]
    [`quaternion_conjugate`][compas.geometry.quaternion_conjugate]

    """
    n = quaternion_norm(q)
    return TOL.is_close(n, 1.0, rtol=0.0, atol=tol)


def quaternion_multiply(r: Sequence[float], q: Sequence[float]) -> list[float]:
    """Multiplies two quaternions.

    Parameters
    ----------
    r
        Sequence of four floats `[w, x, y, z]`.
    q
        Sequence of four floats `[w, x, y, z]`.

    Returns
    -------
    list[float]
        Quaternion `p = rq` as a list of four real values `[pw, px, py, pz]`.

    See Also
    --------
    [`quaternion_is_unit`][compas.geometry.quaternion_is_unit]
    [`quaternion_norm`][compas.geometry.quaternion_norm]
    [`quaternion_unitize`][compas.geometry.quaternion_unitize]
    [`quaternion_canonize`][compas.geometry.quaternion_canonize]
    [`quaternion_conjugate`][compas.geometry.quaternion_conjugate]

    Notes
    -----
    Multiplication of two quaternions `p = rq` can be interpreted as applying rotation `r` to an orientation `q`,
    provided that both `r` and `q` are unit-length.
    The result is also unit-length.
    Multiplication of quaternions is not commutative!

    References
    ----------
    * [Quaternion](https://mathworld.wolfram.com/Quaternion.html)

    """
    rw, rx, ry, rz = r
    qw, qx, qy, qz = q
    pw = rw * qw - rx * qx - ry * qy - rz * qz
    px = rw * qx + rx * qw + ry * qz - rz * qy
    py = rw * qy - rx * qz + ry * qw + rz * qx
    pz = rw * qz + rx * qy - ry * qx + rz * qw
    return [pw, px, py, pz]


def quaternion_canonize(q: Sequence[float]) -> Sequence[float]:
    """Converts a quaternion into a canonic form if needed.

    Parameters
    ----------
    q
        Sequence of four floats `[w, x, y, z]`.

    Returns
    -------
    Sequence[float]
        Quaternion in canonic form as a sequence of four real values `[cw, cx, cy, cz]`.

    See Also
    --------
    [`quaternion_is_unit`][compas.geometry.quaternion_is_unit]
    [`quaternion_norm`][compas.geometry.quaternion_norm]
    [`quaternion_unitize`][compas.geometry.quaternion_unitize]
    [`quaternion_multiply`][compas.geometry.quaternion_multiply]
    [`quaternion_conjugate`][compas.geometry.quaternion_conjugate]

    Notes
    -----
    Canonic form means the scalar component is a non-negative number.

    """
    if q[0] < 0.0:
        return [-x for x in q]
    return q[:]


def quaternion_conjugate(q: Sequence[float]) -> list[float]:
    """Conjugate of a quaternion.

    Parameters
    ----------
    q
        Sequence of four floats `[w, x, y, z]`.

    Returns
    -------
    list[float]
        Conjugate quaternion as a list of four real values `[cw, cx, cy, cz]`.

    See Also
    --------
    [`quaternion_is_unit`][compas.geometry.quaternion_is_unit]
    [`quaternion_norm`][compas.geometry.quaternion_norm]
    [`quaternion_unitize`][compas.geometry.quaternion_unitize]
    [`quaternion_multiply`][compas.geometry.quaternion_multiply]
    [`quaternion_canonize`][compas.geometry.quaternion_canonize]

    References
    ----------
    * [Quaternion Conjugate](https://mathworld.wolfram.com/QuaternionConjugate.html)

    """
    return [q[0], -q[1], -q[2], -q[3]]
