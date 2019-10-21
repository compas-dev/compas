import math

from compas.geometry import quaternion_multiply
from compas.geometry import quaternion_conjugate
from compas.geometry import quaternion_unitize
from compas.geometry import quaternion_canonize
from compas.geometry import quaternion_norm
from compas.geometry import quaternion_is_unit


from compas.geometry.primitives import Primitive

__all__ = ['Quaternion']


class Quaternion(Primitive):
    r"""Creates a ``Quaternion`` object.

    Parameters
    ----------
    w : float
        The scalar (real) part of a quaternion.
    x, y, z : float
        Components of the vector (complex, imaginary) part of a quaternion.


    Examples
    --------
    >>> Q = Quaternion(1.0, 1.0, 1.0, 1.0).unitized()
    >>> R = Quaternion(0.0,-0.1, 0.2,-0.3).unitized()
    >>> P = R*Q
    >>> P.is_unit
    True

    Notes
    -----
    The default convention to represent a quaternion :math:`q` in this module is by four real values :math:`w`, :math:`x`, :math:`y`, :math:`z`.
    The first value :math:`w` is the scalar (real) part, and :math:`x`, :math:`y`, :math:`z` form the vector (complex, imaginary) part [1]_, so that:

    .. math::

        q = w + xi + yj + zk

    where :math:`i, j, k` are basis components with following multiplication rules [2]_:

    .. math::

        \begin{align}
        ii &= jj = kk = ijk = -1 \\
        ij &= k, \quad ji = -k \\
        jk &= i, \quad kj = -i \\
        ki &= j, \quad ik = -j
        \end{align}

    Quaternions are associative but not commutative.

    **Quaternion as rotation.**

    A rotation through an angle :math:`\theta` around an axis defined by a euclidean unit vector :math:`u = u_{x}i + u_{y}j + u_{z}k`
    can be represented as a quaternion:

    .. math::

        q = cos(\frac{\theta}{2}) + sin(\frac{\theta}{2}) [u_{x}i + u_{y}j + u_{z}k]

    i.e.:

    .. math::

        \begin{align}
        w = cos(\frac{\theta}{2})
        x = sin(\frac{\theta}{2}) u_{x}
        y = sin(\frac{\theta}{2}) u_{y}
        z = sin(\frac{\theta}{2}) u_{z}

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

    def __init__(self, w, x, y, z):

        self.w = float(w)
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __iter__(self):
        return iter(self.wxyz)

    def __repr__(self):
        return 'Quaternion({:.{prec}f}, {:.{prec}f}, {:.{prec}f}, {:.{prec}f})'.format(*self, prec=6)

    def __mul__(self, other):
        """Multiply operator for two quaternions.

        Parameters
        ----------
        other
            A Quaternion object.

        Returns
        -------
        Quaternion
            The product P = R * Q of this quaternion (R) multiplied by other quaternion (Q).

        Examples
        --------
        >>> Q = Quaternion(1.0, 1.0, 1.0, 1.0).unitized()
        >>> R = Quaternion(0.0,-0.1, 0.2,-0.3).unitized()
        >>> P = R*Q
        >>> P.is_unit
        True

        Notes
        -----
        Multiplication of two quaternions R*Q can be interpreted as applying rotation R to an orientation Q,
        provided that both R and Q are unit-length.
        The result is also unit-length.
        Multiplication of quaternions is not commutative!
        """

        p = quaternion_multiply(list(self), list(other))
        return Quaternion(*p)

    @classmethod
    def from_frame(cls, frame):
        """Creates a ``Quaternion`` object from a ``Frame`` object.

        Parameters
        ----------
        frame : :obj:`Frame`

        Returns
        -------
        :obj:`Quaternion`
            The new constructed ``Quaternion`` object.

        Example
        -------
        >>> from compas.geometry import Frame
        >>> q = [1., -2., 3., -4.]
        >>> F = Frame.from_quaternion(q)
        >>> Q = Quaternion.from_frame(F)
        >>> allclose(list(Q.canonized()), quaternion_canonize(quaternion_unitize(q)))
        True
        """

        w, x, y, z = frame.quaternion
        return cls(w, x, y, z)

    @property
    def wxyz(self):
        """list of float : Quaternion as a list of float in the "wxyz" convention.
        """
        return [self.w, self.x, self.y, self.z]

    @property
    def xyzw(self):
        """list of float : Quaternion as a list of float in the "xyzw" convention.
        """
        return [self.x, self.y, self.z, self.w]

    @property
    def norm(self):
        """float : The length (euclidean norm) of the quaternion.
        """
        return quaternion_norm(self)

    @property
    def is_unit(self):
        """bool : ``True`` if the quaternion is unit-length or ``False`` if otherwise.
        """
        return quaternion_is_unit(self)

    def unitize(self):
        """Scales the quaternion to make it unit-length.
        """
        qu = quaternion_unitize(self)
        self.w, self.x, self.y, self.z = qu

    def unitized(self):
        """Returns a :obj:`Quaternion` with a unit-length.
        """
        qu = quaternion_unitize(self)
        return Quaternion(*qu)

    def canonize(self):
        """Makes the quaternion canonic.
        """
        qc = quaternion_canonize(self)
        self.w, self.x, self.y, self.z = qc

    def canonized(self):
        """Returns a :obj:`Quaternion` in a canonic form.
        """
        qc = quaternion_canonize(self)
        return Quaternion(*qc)

    def conjugate(self):
        """Returns a conjugate :obj:`Quaternion`.
        """
        qc = quaternion_conjugate(self)
        return Quaternion(*qc)

    # ==========================================================================
    # access
    # ==========================================================================

    def __getitem__(self, key):
        if key == 0:
            return self.w
        if key == 1:
            return self.x
        if key == 2:
            return self.y
        if key == 3:
            return self.z
        raise KeyError

    def __setitem__(self, key, value):
        if key == 0:
            self.w = value
            return
        if key == 1:
            self.x = value
            return
        if key == 2:
            self.y = value
        if key == 3:
            self.z = value
        raise KeyError

    # ==========================================================================
    # comparison
    # ==========================================================================

    def __eq__(self, other, tol=1e-05):
        for v1, v2 in zip(self, other):
            if math.fabs(v1 - v2) > tol:
                return False
        return True


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    from compas.geometry import allclose
    import doctest
    doctest.testmod(globs=globals())
