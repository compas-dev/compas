from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import math

from compas.geometry import quaternion_multiply
from compas.geometry import quaternion_conjugate
from compas.geometry import quaternion_unitize
from compas.geometry import quaternion_canonize
from compas.geometry import quaternion_norm
from compas.geometry import quaternion_is_unit
from compas.geometry import quaternion_from_matrix

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

    Attributes
    ----------
    wxyz : list of float, read-only
        Quaternion data listing the real part first.
    xyzw : list of float, read-only
        Quaternion data listing the real part last.
    norm : float, read-only
        The length of the quaternion.
    is_unit : bool, read-only
        True if the quaternion has unit length.

    Notes
    -----
    The default convention to represent a quaternion :math:`q` in this module
    is by four real values :math:`w`, :math:`x`, :math:`y`, :math:`z`.
    The first value :math:`w` is the scalar (real) part,
    and :math:`x`, :math:`y`, :math:`z` form the vector (complex, imaginary) part [1]_, so that:

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

    A rotation through an angle :math:`\theta` around an axis
    defined by a euclidean unit vector :math:`u = u_{x}i + u_{y}j + u_{z}k`
    can be represented as a quaternion:

    .. math::

        q = cos(\frac{\theta}{2}) + sin(\frac{\theta}{2}) [u_{x}i + u_{y}j + u_{z}k]

    i.e.:

    .. math::

        \begin{align}
        w &= cos(\frac{\theta}{2}) \\
        x &= sin(\frac{\theta}{2}) u_{x} \\
        y &= sin(\frac{\theta}{2}) u_{y} \\
        z &= sin(\frac{\theta}{2}) u_{z}
        \end{align}

    For a quaternion to represent a rotation or orientation, it must be unit-length.
    A quaternion representing a rotation :math:`p` resulting from applying a rotation
    :math:`r` to a rotation :math:`q`, i.e.: :math:`p = rq`,
    is also unit-length.

    References
    ----------
    .. [1] http://mathworld.wolfram.com/Quaternion.html
    .. [2] http://mathworld.wolfram.com/HamiltonsRules.html
    .. [3] https://github.com/matthew-brett/transforms3d/blob/master/transforms3d/quaternions.py

    Examples
    --------
    >>> Q = Quaternion(1.0, 1.0, 1.0, 1.0).unitized()
    >>> R = Quaternion(0.0,-0.1, 0.2,-0.3).unitized()
    >>> P = R*Q
    >>> P.is_unit
    True
    """

    __slots__ = ['_w', '_x', '_y', '_z']

    def __init__(self, w, x, y, z):
        super(Quaternion, self).__init__()
        self._w = None
        self._x = None
        self._y = None
        self._z = None
        self.w = w
        self.x = x
        self.y = y
        self.z = z

    @property
    def w(self):
        """float : The W component of the quaternion."""
        return self._w

    @w.setter
    def w(self, w):
        self._w = float(w)

    @property
    def x(self):
        """float : The X component of the quaternion."""
        return self._x

    @x.setter
    def x(self, x):
        self._x = float(x)

    @property
    def y(self):
        """float : The Y component of the quaternion."""
        return self._y

    @y.setter
    def y(self, y):
        self._y = float(y)

    @property
    def z(self):
        """float : The Z component of the quaternion."""
        return self._z

    @z.setter
    def z(self, z):
        self._z = float(z)

    @property
    def data(self):
        return {'w': self.w, 'x': self.x, 'y': self.y, 'z': self.z}

    @data.setter
    def data(self, data):
        self.w = data['w']
        self.x = data['x']
        self.y = data['y']
        self.z = data['z']

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

    # ==========================================================================
    # customization
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

    def __eq__(self, other, tol=1e-05):
        for v1, v2 in zip(self, other):
            if math.fabs(v1 - v2) > tol:
                return False
        return True

    def __iter__(self):
        return iter(self.wxyz)

    def __repr__(self):
        return 'Quaternion({:.{prec}f}, {:.{prec}f}, {:.{prec}f}, {:.{prec}f})'.format(self.w, self.x, self.y, self.z, prec=3)

    def __mul__(self, other):
        """Multiply operator for two quaternions.

        Parameters
        ----------
        other : :class:`compas.geometry.Quaternion` or list
            A Quaternion.

        Returns
        -------
        :class:`compas.geometry.Quaternion`
            The product P = R * Q of this quaternion (R) multiplied by other quaternion (Q).

        Notes
        -----
        Multiplication of two quaternions R*Q can be interpreted as applying rotation R to an orientation Q,
        provided that both R and Q are unit-length.
        The result is also unit-length.
        Multiplication of quaternions is not commutative!

        Examples
        --------
        >>> Q = Quaternion(1.0, 1.0, 1.0, 1.0).unitized()
        >>> R = Quaternion(0.0,-0.1, 0.2,-0.3).unitized()
        >>> P = R*Q
        >>> P.is_unit
        True
        """
        p = quaternion_multiply(list(self), list(other))
        return Quaternion(*p)

    # ==========================================================================
    # constructors
    # ==========================================================================

    @classmethod
    def from_data(cls, data):
        """Construct a quaternion from a data dict.

        Parameters
        ----------
        data : dict
            The data dictionary.

        Returns
        -------
        :class:`compas.geometry.Quaternion`
            The constructed quaternion.

        Examples
        --------
        >>>
        """
        return cls(data['w'], data['x'], data['y'], data['z'])

    @classmethod
    def from_frame(cls, frame):
        """Creates a quaternion object from a frame.

        Parameters
        ----------
        frame : :class:`compas.geometry.Frame`

        Returns
        -------
        :class:`compas.geometry.Quaternion`
            The new quaternion.

        Examples
        --------
        >>> from compas.geometry import Frame
        >>> q = [1., -2., 3., -4.]
        >>> F = Frame.from_quaternion(q)
        >>> Q = Quaternion.from_frame(F)
        >>> allclose(list(Q.canonized()), quaternion_canonize(quaternion_unitize(q)))
        True
        """
        w, x, y, z = frame.quaternion
        return cls(w, x, y, z)

    @classmethod
    def from_matrix(cls, M):
        """Create a :class:`Quaternion` from a transformation matrix.

        Parameters
        ----------
        M : :obj:`list` of :obj:`list` of :obj:`float`

        Returns
        -------
        :class:`compas.geometry.Quaternion`
            The new quaternion.

        Example
        -------
        >>> from compas.geometry import matrix_from_euler_angles
        >>> ea = [0.2, 0.6, 0.2]
        >>> M = matrix_from_euler_angles(ea)
        >>> Quaternion.from_matrix(M)
        Quaternion(0.949, 0.066, 0.302, 0.066)
        """
        return cls(*quaternion_from_matrix(M))

    @classmethod
    def from_rotation(cls, R):
        """Create a :class:`Quaternion` from a :class:`compas.geometry.Rotatation`.

        Parameters
        ----------
        R : :class:`compas.geometry.Rotation`

        Returns
        -------
        :class:`compas.geometry.Quaternion`
            The new quaternion.

        Example
        -------
        >>> from compas.geometry import Frame, Rotation
        >>> R = Rotation.from_frame(Frame.worldYZ())
        >>> Quaternion.from_rotation(R)
        Quaternion(0.500, 0.500, 0.500, 0.500)

        """
        return cls.from_matrix(R.matrix)

    # ==========================================================================
    # methods
    # ==========================================================================

    def unitize(self):
        """Scales the quaternion to make it unit-length.

        Examples
        --------
        >>> q = Quaternion(1.0, 1.0, 1.0, 1.0)
        >>> q.is_unit
        False
        >>> q.unitize()
        >>> q.is_unit
        True
        """
        qu = quaternion_unitize(self)
        self.w, self.x, self.y, self.z = qu

    def unitized(self):
        """Returns a quaternion with a unit-length.

        Examples
        --------
        >>> q = Quaternion(1.0, 1.0, 1.0, 1.0)
        >>> q.is_unit
        False
        >>> p = q.unitized()
        >>> p.is_unit
        True
        """
        qu = quaternion_unitize(self)
        return Quaternion(*qu)

    def canonize(self):
        """Makes the quaternion canonic.

        Examples
        --------
        >>> from compas.geometry import Frame
        >>> q = Quaternion.from_frame(Frame.worldZX())
        >>> q
        Quaternion(-0.500, 0.500, 0.500, 0.500)
        >>> q.canonize()
        >>> q
        Quaternion(0.500, -0.500, -0.500, -0.500)
        """
        qc = quaternion_canonize(self)
        self.w, self.x, self.y, self.z = qc

    def canonized(self):
        """Returns a quaternion in canonic form.

        Returns
        -------
        :class:`compas.geometry.Quaternion`
            A quaternion in canonic form.

        Examples
        --------
        >>> from compas.geometry import Frame
        >>> q = Quaternion.from_frame(Frame.worldZX())
        >>> q
        Quaternion(-0.500, 0.500, 0.500, 0.500)
        >>> p = q.canonized()
        >>> p
        Quaternion(0.500, -0.500, -0.500, -0.500)
        """
        qc = quaternion_canonize(self)
        return Quaternion(*qc)

    def conjugate(self):
        """Conjugate the quaternion.

        Examples
        --------
        >>> q = Quaternion(1.0, 1.0, 1.0, 1.0)
        >>> q.conjugate()
        >>> q
        Quaternion(1.000, -1.000, -1.000, -1.000)
        """
        qc = quaternion_conjugate(self)
        self.w, self.x, self.y, self.z = qc

    def conjugated(self):
        """Returns a conjugate quaternion.

        Returns
        -------
        :class:`compas.geometry.Quaternion`
            The conjugated quaternion.

        Examples
        --------
        >>> q = Quaternion(1.0, 1.0, 1.0, 1.0)
        >>> p = q.conjugated()
        >>> q
        Quaternion(1.000, 1.000, 1.000, 1.000)
        >>> p
        Quaternion(1.000, -1.000, -1.000, -1.000)
        """
        qc = quaternion_conjugate(self)
        return Quaternion(*qc)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import doctest

    from compas.geometry import allclose  # noqa: F401

    doctest.testmod(globs=globals())
