import math
from typing import Optional
from typing import Sequence

from compas._typing import FloatSequenceType
from compas.tolerance import TOL

from .transformations import axis_and_angle_from_matrix
from .transformations import euler_angles_from_matrix
from .transformations import matrix_from_axis_and_angle
from .transformations import matrix_from_euler_angles
from .transformations import matrix_from_quaternion
from .transformations import quaternion_from_matrix


def quaternion_norm(q: FloatSequenceType) -> float:
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
    [`quaternion_is_unit`][compas.linalg.quaternion_is_unit]
    [`quaternion_unitize`][compas.linalg.quaternion_unitize]
    [`quaternion_multiply`][compas.linalg.quaternion_multiply]
    [`quaternion_canonize`][compas.linalg.quaternion_canonize]
    [`quaternion_conjugate`][compas.linalg.quaternion_conjugate]

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
    [`quaternion_is_unit`][compas.linalg.quaternion_is_unit]
    [`quaternion_norm`][compas.linalg.quaternion_norm]
    [`quaternion_multiply`][compas.linalg.quaternion_multiply]
    [`quaternion_canonize`][compas.linalg.quaternion_canonize]
    [`quaternion_conjugate`][compas.linalg.quaternion_conjugate]

    """
    n = quaternion_norm(q)

    if TOL.is_zero(n):
        raise ValueError("The given quaternion has zero length.")

    return [x / n for x in q]


def quaternion_is_unit(q: FloatSequenceType, tol: Optional[float] = None) -> bool:
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
    [`quaternion_unitize`][compas.linalg.quaternion_unitize]
    [`quaternion_norm`][compas.linalg.quaternion_norm]
    [`quaternion_multiply`][compas.linalg.quaternion_multiply]
    [`quaternion_canonize`][compas.linalg.quaternion_canonize]
    [`quaternion_conjugate`][compas.linalg.quaternion_conjugate]

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
    [`quaternion_is_unit`][compas.linalg.quaternion_is_unit]
    [`quaternion_norm`][compas.linalg.quaternion_norm]
    [`quaternion_unitize`][compas.linalg.quaternion_unitize]
    [`quaternion_canonize`][compas.linalg.quaternion_canonize]
    [`quaternion_conjugate`][compas.linalg.quaternion_conjugate]

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
    [`quaternion_is_unit`][compas.linalg.quaternion_is_unit]
    [`quaternion_norm`][compas.linalg.quaternion_norm]
    [`quaternion_unitize`][compas.linalg.quaternion_unitize]
    [`quaternion_multiply`][compas.linalg.quaternion_multiply]
    [`quaternion_conjugate`][compas.linalg.quaternion_conjugate]

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
    [`quaternion_is_unit`][compas.linalg.quaternion_is_unit]
    [`quaternion_norm`][compas.linalg.quaternion_norm]
    [`quaternion_unitize`][compas.linalg.quaternion_unitize]
    [`quaternion_multiply`][compas.linalg.quaternion_multiply]
    [`quaternion_canonize`][compas.linalg.quaternion_canonize]

    References
    ----------
    * [Quaternion Conjugate](https://mathworld.wolfram.com/QuaternionConjugate.html)

    """
    return [q[0], -q[1], -q[2], -q[3]]


def quaternion_from_euler_angles(e: Sequence[float], static: bool = True, axes: str = "xyz") -> list[float]:
    """Returns a quaternion from Euler angles.

    Parameters
    ----------
    e
        Three numbers that represent the angles of rotations about the specified axes.
    static
        If True, the rotations are applied to a static frame.
        If False, the rotations are applied to a rotational frame.
    axes
        A three-character string specifying the order of the axes.

    Returns
    -------
    list[float]
        Quaternion as a list of four real values `[w, x, y, z]`.

    """
    m = matrix_from_euler_angles(e, static, axes)
    q = quaternion_from_matrix(m)
    return q


def euler_angles_from_quaternion(q: Sequence[float], static: bool = True, axes: str = "xyz") -> list[float]:
    """Returns Euler angles from a quaternion.

    Parameters
    ----------
    q
        Quaternion as a list of four real values `[w, x, y, z]`.
    static
        If True, the rotations are applied to a static frame.
        If False, the rotations are applied to a rotational frame.
    axes
        A three-character string specifying the order of the axes.

    Returns
    -------
    list[float]
        Euler angles as a list of three real values `[a, b, c]`.

    """
    m = matrix_from_quaternion(q)
    e = euler_angles_from_matrix(m, static, axes)
    return e


def quaternion_from_axis_angle(axis: Sequence[float], angle: float) -> list[float]:
    """Returns a quaternion describing a rotation around the given axis by the given angle.

    Parameters
    ----------
    axis
        XYZ coordinates of the rotation axis vector.
    angle
        Angle of rotation in radians.

    Returns
    -------
    list[float]
        Quaternion as a list of four real values `[qw, qx, qy, qz]`.

    Examples
    --------
    >>> axis = [1.0, 0.0, 0.0]
    >>> angle = math.pi / 2
    >>> q = quaternion_from_axis_angle(axis, angle)
    >>> allclose(q, [math.sqrt(2) / 2, math.sqrt(2) / 2, 0, 0])
    True

    """
    m = matrix_from_axis_and_angle(axis, angle, None)
    q = quaternion_from_matrix(m)
    return q


def axis_angle_from_quaternion(q: Sequence[float]) -> tuple[list[float], float]:
    """Returns an axis and an angle of rotation from the given quaternion.

    Parameters
    ----------
    q
        Quaternion as a list of four real values `[qw, qx, qy, qz]`.

    Returns
    -------
    tuple[list[float], float]
        The rotation axis and rotation angle in radians.

    Examples
    --------
    >>> q = [1.0, 1.0, 0.0, 0.0]
    >>> axis, angle = axis_angle_from_quaternion(q)
    >>> allclose(axis, [1.0, 0.0, 0.0])
    True
    >>> allclose([angle], [math.pi / 2], 1e-6)
    True

    """
    m = matrix_from_quaternion(q)
    axis, angle = axis_and_angle_from_matrix(m)
    return axis, angle
