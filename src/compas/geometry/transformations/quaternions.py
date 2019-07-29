"""
This module contains functions that operate on and/or return quaternions.

Default convention to represent a quaternion in this module is a tuple of four real values [qw,qx,qy,qz].
The first value qw is the scalar (real) part, and qx,qy,qz form the vector (complex, imaginary) part, so that:
q = qw + qx*i + qy*j + qz*k,
where i,j,k are basis components.

Quaternion algebra basics:
i*i = j*j = k*k = i*j*k = -1
i*j = k    j*i = -k
j*k = i    k*j = -i
k*i = j    i*k = -j

Quaternion as rotation:
A rotation through an angle theta around an axis defined by a euclidean unit vector u = ux*i + uy*j + uz*k
can be represented as a quaternion:
q = cos(theta/2) + sin(theta/2) * [ux*i + uy*j + uz*k]
i.e.:
qw = cos(theta/2)
qx = sin(theta/2) * ux
qy = sin(theta/2) * uy
qz = sin(theta/2) * uz

For a quaternion to represent a rotation or orientation, it must be unit-length.

References
----------
.. https://github.com/matthew-brett/transforms3d/blob/master/transforms3d/quaternions.py
.. http://mathworld.wolfram.com/Quaternion.html
"""

from compas.geometry.transformations import quaternion_from_matrix
from compas.geometry.transformations import matrix_from_quaternion
from compas.geometry.transformations import euler_angles_from_matrix
from compas.geometry.transformations import matrix_from_euler_angles
from compas.geometry.transformations import axis_and_angle_from_matrix
from compas.geometry.transformations import matrix_from_axis_and_angle

#from compas.geometry.basic import allclose
import math


__all__ = [
    'quaternion_norm',
    'quaternion_unitize',
    'quaternion_is_unit',
    'quaternion_multiply',
    'quaternion_canonic',
    'quaternion_conjugate',
    'quaternion_from_euler_angles',
    'euler_angles_from_quaternion',
    'quaternion_from_axis_angle',
    'axis_angle_from_quaternion']


# ----------------------------------------------------------------------
ATOL = 1e-16  # absolute tolerance
RTOL = 1e-3  # relative tolerance


def isclose(a, b, atol=ATOL, rtol=RTOL):
    # https://docs.scipy.org/doc/numpy/reference/generated/numpy.isclose.html#numpy.isclose
    # absolute(a - b) <= (atol + rtol * absolute(b))

    return abs(a - b) <= (atol + rtol * abs(b))

# ----------------------------------------------------------------------


def quaternion_norm(q):
    """Calculates the length (euclidean norm) of a quaternion.

    Parameters
    ----------
    q : list
        Quaternion as a tuple of four real values [qw,qx,qy,qz].

    Returns
    -------
    float
        The length (euclidean norm) of a quaternion.

    Note
    ----
    .. _mathworld quaternion norm
    http://mathworld.wolfram.com/QuaternionNorm.html
    """
    return math.sqrt(sum([x*x for x in q]))


def quaternion_unitize(q):
    """Makes a quaternion unit-length.
    Parameters
    ----------
    q : list
        Quaternion as a tuple of four real values [qw,qx,qy,qz].

    Returns
    -------
    list
        A quaternion of length 1.0.
    """
    n = quaternion_norm(q)
    if isclose(n, 0.0):
        raise ValueError("The given quaternion has zero length.")
    else:
        return [x/n for x in q]


def quaternion_is_unit(q):
    """Checks if a quaternion is unit-length.
    Parameters
    ----------
    q : list
        Quaternion as a tuple of four real values [qw,qx,qy,qz].

    Returns
    -------
    bool
        True if the quaternion is unit-length, and False if otherwise.
    """
    n = quaternion_norm(q)
    return isclose(n, 1.0)


def quaternion_multiply(r, q):
    """Multiplies two quaternions.
    Parameters
    ----------
    r : list
        Quaternion as a tuple of four real values [qw,qx,qy,qz].
    q : list
        Quaternion as a tuple of four real values [qw,qx,qy,qz].

    Returns
    -------
    list
        A quaternion p = r * q.

    Note
    ----
    Multiplication of two quaternions r * q can be interpreted as applying rotation r to an orientation q,
    provided both r and q are unit-length.
    The result is also unit-length.
    Multiplication of quaternions is not commutative!

    .. _mathworld quaternion:
    http://mathworld.wolfram.com/Quaternion.html
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
        Quaternion as a tuple of four real values [qw,qx,qy,qz].

    Returns
    -------
    list
        A quaternion in a canonic form.

    Note
    ----
    Canonic form means the scalar component is a non-negative number.

    """
    if q[0] < 0.0:
        return [-x for x in q]
    else:
        return [x for x in q]


def quaternion_conjugate(q):
    """Conjugate of a quaternion.

    Parameters
    ----------
    q : list
        Quaternion as a tuple of four real values [qw,qx,qy,qz].

    Returns
    -------
    list
        A conjugate quaternion.

    Note
    ----
    .. _mathworld quaternion conjugate
    http://mathworld.wolfram.com/QuaternionConjugate.html

    """
    return [q[0], -q[1], -q[2], -q[3]]


# ----------------------------------------------------------------------
# quaternion_from_matrix(m) - already in compas/geometry/transformations/matrices.py
# matrix_from_quaternion(q) - already in compas/geometry/transformations/matrices.py
# ----------------------------------------------------------------------


def quaternion_from_euler_angles(e, static=True, axes='xyz'):
    """Returns a quaternion from Euler angles.

    Parameters
    ----------
    euler_angles : list of float
        Three numbers that represent the angles of rotations about the specified axes.
    static : bool, optional
        If True, the rotations are applied to a static frame.
        If False, the rotations are applied to a rotational frame.
        Defaults to True.
    axes : str, optional
        A three-character string specifying the order of the axes.
        Defaults to 'xyz'.

    Returns
    -------
    list of float
        Quaternion [qw,qx,qy,qz] as a list of four real values.
    """

    m = matrix_from_euler_angles(e, static=True, axes='xyz')
    q = quaternion_from_matrix(m)
    return q


def euler_angles_from_quaternion(q, static=True, axes='xyz'):
    """Returns Euler angles from a quaternion.

    Parameters
    ----------
    quaternion : list of float
        Quaternion [qw,qx,qy,qz] as a list of four real values.
    static : bool, optional
        If True, the rotations are applied to a static frame.
        If False, the rotations are applied to a rotational frame.
        Defaults to True.
    axes : str, optional
        A three-character string specifying the order of the axes.
        Defaults to 'xyz'.

    Returns
    -------
    list of float
        Three Euler angles.
    """
    m = matrix_from_quaternion(q)
    e = euler_angles_from_matrix(m, static, axes)
    return e

# ----------------------------------------------------------------------


def quaternion_from_axis_angle(axis, angle):
    """Returns a quaternion describing a rotation around the given axis by the given angle.

    Parameters
    ----------
    axis : list
        Coordinates [x,y,z] of the rotation axis vector.
    angle : float
        Angle of rotation in radians.

    Returns
    -------
    quaternion : list
        Quaternion [qw,qx,qy,qz] as a list of four real values.

    Example
    -------
    >>> axis =  [1.0, 0.0, 0.0]
    >>> angle = math.pi/2
    >>> q = quaternion_from_axis_angle(axis,angle)
    >>> print(q)
    [0.7071067811865476, 0.7071067811865475, 0.0, 0.0]
    """
    m = matrix_from_axis_and_angle(axis, angle, point=None, rtype='list')
    q = quaternion_from_matrix(m)
    return q


def axis_angle_from_quaternion(q):
    """Returns an axis and angle of rotation from the given quaternion.

    Parameters
    ----------
    quaternion : list
        Quaternion [qw,qx,qy,qz] as a list of four real values.

    Returns
    -------
    axis : list of float
        Coordinates [x,y,z] of the rotation axis vector.
    angle : float
        Angle of rotation in radians.

    Example
    -------
    >>> q = [1,1,0,0]
    >>> axis,angle = axis_angle_from_quaternion(q)
    >>> print("axis = ", axis, " angle = ", angle)
    axis =  [1.0, 0.0, 0.0]  angle =  1.5707963267948966
    """

    m = matrix_from_quaternion(q)
    axis, angle = axis_and_angle_from_matrix(m)
    return axis, angle


if __name__ == "__main__":
    import doctest
    doctest.testmod(globs=globals())
