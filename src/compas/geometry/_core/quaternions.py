import math

from compas.tolerance import TOL


def quaternion_norm(q):
    """Calculates the length (euclidean norm) of a quaternion.

    Parameters
    ----------
    q : [float, float, float, float] | :class:`compas.geometry.Quaternion`
        Quaternion or sequence of four floats ``[w, x, y, z]``.

    Returns
    -------
    float
        The length (euclidean norm) of a quaternion.

    See Also
    --------
    quaternion_is_unit
    quaternion_unitize
    quaternion_multiply
    quaternion_canonize
    quaternion_conjugate

    References
    ----------
    * Quaternion Norm: http://mathworld.wolfram.com/QuaternionNorm.html

    """
    return math.sqrt(sum([x * x for x in q]))


def quaternion_unitize(q):
    """Makes a quaternion unit-length.

    Parameters
    ----------
    q : [float, float, float, float] | :class:`compas.geometry.Quaternion`
        Quaternion or sequence of four floats ``[w, x, y, z]``.

    Returns
    -------
    [float, float, float, float]
        Quaternion of length 1 as a list of four real values ``[nw, nx, ny, nz]``.

    See Also
    --------
    quaternion_is_unit
    quaternion_norm
    quaternion_multiply
    quaternion_canonize
    quaternion_conjugate

    """
    n = quaternion_norm(q)

    if TOL.is_zero(n):
        raise ValueError("The given quaternion has zero length.")

    return [x / n for x in q]


def quaternion_is_unit(q, tol=None):
    """Checks if a quaternion is unit-length.

    Parameters
    ----------
    q : [float, float, float, float] | :class:`compas.geometry.Quaternion`
        Quaternion or sequence of four floats ``[w, x, y, z]``.
    tol : float, optional
        The tolerance for comparing the quaternion norm to 1.
        Default is :attr:`TOL.absolute`.

    Returns
    -------
    bool
        True if the quaternion is unit-length,
        and False if otherwise.

    See Also
    --------
    quaternion_unitize
    quaternion_norm
    quaternion_multiply
    quaternion_canonize
    quaternion_conjugate

    """
    n = quaternion_norm(q)
    return TOL.is_close(n, 1.0, rtol=0.0, atol=tol)


def quaternion_multiply(r, q):
    """Multiplies two quaternions.

    Parameters
    ----------
    r : [float, float, float, float] | :class:`compas.geometry.Quaternion`
        Quaternion or sequence of four floats ``[w, x, y, z]``.
    q : [float, float, float, float] | :class:`compas.geometry.Quaternion`
        Quaternion or sequence of four floats ``[w, x, y, z]``.

    Returns
    -------
    [float, float, float, float]
        Quaternion :math:`p = rq` as a list of four real values ``[pw, px, py, pz]``.

    See Also
    --------
    quaternion_is_unit
    quaternion_norm
    quaternion_unitize
    quaternion_canonize
    quaternion_conjugate

    Notes
    -----
    Multiplication of two quaternions :math:`p = rq` can be interpreted as applying rotation :math:`r` to an orientation :math:`q`,
    provided that both :math:`r` and :math:`q` are unit-length.
    The result is also unit-length.
    Multiplication of quaternions is not commutative!

    References
    ----------
    * Quaternion: http://mathworld.wolfram.com/Quaternion.html

    """
    rw, rx, ry, rz = r
    qw, qx, qy, qz = q
    pw = rw * qw - rx * qx - ry * qy - rz * qz
    px = rw * qx + rx * qw + ry * qz - rz * qy
    py = rw * qy - rx * qz + ry * qw + rz * qx
    pz = rw * qz + rx * qy - ry * qx + rz * qw
    return [pw, px, py, pz]


def quaternion_canonize(q):
    """Converts a quaternion into a canonic form if needed.

    Parameters
    ----------
    q : [float, float, float, float] | :class:`compas.geometry.Quaternion`
        Quaternion or sequence of four floats ``[w, x, y, z]``.

    Returns
    -------
    [float, float, float, float]
        Quaternion in a canonic form as a list of four real values ``[cw, cx, cy, cz]``.

    See Also
    --------
    quaternion_is_unit
    quaternion_norm
    quaternion_unitize
    quaternion_multiply
    quaternion_conjugate

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
    q : [float, float, float, float] | :class:`compas.geometry.Quaternion`
        Quaternion or sequence of four floats ``[w, x, y, z]``.

    Returns
    -------
    [float, float, float, float]
        Conjugate quaternion as a list of four real values ``[cw, cx, cy, cz]``.

    See Also
    --------
    quaternion_is_unit
    quaternion_norm
    quaternion_unitize
    quaternion_multiply
    quaternion_canonize

    References
    ----------
    *  Quaternion Conjugate: http://mathworld.wolfram.com/QuaternionConjugate.html

    """
    return [q[0], -q[1], -q[2], -q[3]]
