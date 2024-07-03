from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import math
from sys import float_info

from compas.geometry import Geometry
from compas.geometry import Rotation
from compas.geometry import quaternion_canonize
from compas.geometry import quaternion_conjugate
from compas.geometry import quaternion_from_matrix
from compas.geometry import quaternion_is_unit
from compas.geometry import quaternion_multiply
from compas.geometry import quaternion_norm
from compas.geometry import quaternion_unitize
from compas.tolerance import TOL


class Quaternion(Geometry):
    r"""A quaternion is defined by 4 components, X, Y, Z, and W.

    Parameters
    ----------
    w : float
        The scalar (real) part of a quaternion.
    x : float
        X component of the vector (complex, imaginary) part of a quaternion.
    y : float
        Y component of the vector (complex, imaginary) part of a quaternion.
    z : float
        Z component of the vector (complex, imaginary) part of a quaternion.
    name : str, optional
        The name of the transformation.

    Attributes
    ----------
    w : float
        The W component of the quaternion.
    x : float
        The X component of the quaternion.
    y : float
        The Y component of the quaternion.
    z : float
        The Z component of the quaternion.
    wxyz : list[float], read-only
        Quaternion as a list of float in the 'wxyz' convention.
    xyzw : list[float], read-only
        Quaternion as a list of float in the 'xyzw' convention.
    norm : float, read-only
        The length (euclidean norm) of the quaternion.
    is_unit : bool, read-only
        True if the quaternion is unit-length.
        False otherwise.

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

    DATASCHEMA = {
        "type": "object",
        "properties": {
            "w": {"type": "number"},
            "x": {"type": "number"},
            "y": {"type": "number"},
            "z": {"type": "number"},
        },
        "required": ["w", "x", "y", "z"],
    }

    @property
    def __data__(self):
        return {"w": self.w, "x": self.x, "y": self.y, "z": self.z}

    def __init__(self, w, x, y, z, name=None):
        super(Quaternion, self).__init__(name=name)
        self._w = None
        self._x = None
        self._y = None
        self._z = None
        self.w = w
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return "{0}({1}, {2}, {3}, {4})".format(type(self).__name__, self.w, self.x, self.y, self.z)

    def __str__(self):
        return "{0}({1}, {2}, {3}, {4})".format(
            type(self).__name__,
            TOL.format_number(self.w),
            TOL.format_number(self.x),
            TOL.format_number(self.y),
            TOL.format_number(self.z),
        )

    def __eq__(self, other, tol=None):
        if not hasattr(other, "__iter__") or not hasattr(other, "__len__") or len(self) != len(other):
            return False
        return TOL.is_allclose(self, other, rtol=0, atol=tol)

    def __getitem__(self, key):
        if key == 0:
            return self.w
        if key == 1:
            return self.x
        if key == 2:
            return self.y
        if key == 3:
            return self.z
        raise KeyError(key)

    def __setitem__(self, key, value):
        if key == 0:
            self.w = value
            return
        if key == 1:
            self.x = value
            return
        if key == 2:
            self.y = value
            return
        if key == 3:
            self.z = value
            return
        raise KeyError(key)

    def __iter__(self):
        return iter(self.wxyz)

    def __len__(self):
        return 4

    # ==========================================================================
    # Properties
    # ==========================================================================

    @property
    def w(self):
        return self._w

    @w.setter
    def w(self, w):
        self._w = float(w)

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        self._x = float(x)

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        self._y = float(y)

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, z):
        self._z = float(z)

    @property
    def wxyz(self):
        return [self.w, self.x, self.y, self.z]

    @property
    def xyzw(self):
        return [self.x, self.y, self.z, self.w]

    @property
    def norm(self):
        return quaternion_norm(self)

    @property
    def is_unit(self):
        return quaternion_is_unit(self)

    # ==========================================================================
    # Operators
    # ==========================================================================

    def __mul__(self, other):
        """Multiply operator for two quaternions.

        Parameters
        ----------
        other : [float, float, float, float] | :class:`compas.geometry.Quaternion`
            A Quaternion.

        Returns
        -------
        :class:`compas.geometry.Quaternion`
            The product :math:`P = R * Q` of this quaternion (R) multiplied by other quaternion (Q).

        Notes
        -----
        Multiplication of two quaternions :math:`R * Q` can be interpreted as applying rotation R to an orientation Q,
        provided that both R and Q are unit-length.
        The result is also unit-length.
        Multiplication of quaternions is not commutative!

        Examples
        --------
        >>> Q = Quaternion(1.0, 1.0, 1.0, 1.0).unitized()
        >>> R = Quaternion(0.0, -0.1, 0.2, -0.3).unitized()
        >>> P = R * Q
        >>> P.is_unit
        True

        """
        p = quaternion_multiply(list(self), list(other))
        return Quaternion(*p)

    # ==========================================================================
    # Constructors
    # ==========================================================================

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
        >>> from compas.tolerance import TOL
        >>> from compas.geometry import Frame
        >>> q = [1.0, -2.0, 3.0, -4.0]
        >>> F = Frame.from_quaternion(q)
        >>> Q = Quaternion.from_frame(F)
        >>> TOL.is_allclose(Q.canonized(), quaternion_canonize(quaternion_unitize(q)))
        True

        """
        w, x, y, z = frame.quaternion
        return cls(w, x, y, z)

    @classmethod
    def from_matrix(cls, M):
        """Create a Quaternion from a transformation matrix.

        Parameters
        ----------
        M : list[list[float]]

        Returns
        -------
        :class:`compas.geometry.Quaternion`
            The new quaternion.

        Examples
        --------
        >>> from compas.geometry import matrix_from_euler_angles
        >>> ea = [0.2, 0.6, 0.2]
        >>> M = matrix_from_euler_angles(ea)
        >>> Quaternion.from_matrix(M)
        Quaternion(0.949, 0.066, 0.302, 0.066)

        """
        return cls(*quaternion_from_matrix(M))

    @classmethod
    def from_rotation(cls, R):
        """Create a Quaternion from a Rotatation.

        Parameters
        ----------
        R : :class:`compas.geometry.Rotation`

        Returns
        -------
        :class:`compas.geometry.Quaternion`
            The new quaternion.

        Examples
        --------
        >>> from compas.geometry import Frame, Rotation
        >>> R = Rotation.from_frame(Frame.worldYZ())
        >>> Quaternion.from_rotation(R)
        Quaternion(0.500, 0.500, 0.500, 0.500)

        """
        return cls.from_matrix(R.matrix)

    # ==========================================================================
    # Methods
    # ==========================================================================

    def unitize(self):
        """Scales the quaternion to make it unit-length.

        Returns
        -------
        None

        Examples
        --------
        >>> q = Quaternion(1.0, 1.0, 1.0, 1.0)
        >>> q.is_unit
        False
        >>> q.unitize()
        >>> q.is_unit
        True

        """
        qu = quaternion_unitize(list(self))
        self.w, self.x, self.y, self.z = qu

    def unitized(self):
        """Returns a quaternion with a unit-length.

        Returns
        -------
        :class:`compas.geometry.Quaternion`

        Examples
        --------
        >>> q = Quaternion(1.0, 1.0, 1.0, 1.0)
        >>> q.is_unit
        False
        >>> p = q.unitized()
        >>> p.is_unit
        True

        """
        qu = quaternion_unitize(list(self))
        return Quaternion(*qu)

    def canonize(self):
        """Makes the quaternion canonic.

        Returns
        -------
        None

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
        qc = quaternion_canonize(list(self))
        self.w, self.x, self.y, self.z = qc  # type: ignore

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
        qc = quaternion_canonize(list(self))
        return Quaternion(*qc)  # type: ignore

    def conjugate(self):
        """Conjugate the quaternion.

        Returns
        -------
        None

        Examples
        --------
        >>> q = Quaternion(1.0, 1.0, 1.0, 1.0)
        >>> q.conjugate()
        >>> q
        Quaternion(1.000, -1.000, -1.000, -1.000)

        """
        qc = quaternion_conjugate(list(self))
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
        qc = quaternion_conjugate(list(self))
        return Quaternion(*qc)

    def dot(self, other):
        """Computes the cosine of the angle between the two quaternions"""
        return self.w * other.w + self.x * other.x + self.y * other.y + self.z * other.z

    def slerp(self, other, t):
        """Slerp: spherical interpolation of two quaternions.

        Parameters
        ----------
        other : :class:`compas.geometry.Quaternion`
            The other quaternion to interpolate between.
        t : float
            A parameter in the range [0-1].

        Returns
        -------
        :class:`compas.geometry.Quaternion`

        Examples
        --------
        >>> q1 = Quaternion(1, 0, 0, 0)
        >>> q2 = Quaternion(0, 1, 0, 0)
        >>> t = 0.5
        >>> interpolated_quaternion = Quaternion.slerp(q1, q2, t)

        """
        epsilon = float_info.epsilon

        q1 = self.unitized()
        q2 = other.unitized()

        cosom = q1.dot(q2)

        interpolated = Rotation()
        quat = list(interpolated.quaternion)

        # rotate around the shortest angle
        if cosom < 0.0:
            cosom = -cosom
            quat[0] = -q1[0]
            quat[1] = -q1[1]
            quat[2] = -q1[2]
            quat[3] = -q1[3]

        else:
            quat[0] = q1[0]
            quat[1] = q1[1]
            quat[2] = q1[2]
            quat[3] = q1[3]

        if (1.0 - cosom) > epsilon:
            omega = math.acos(cosom)
            sinom = math.sin(omega)
            sc1 = math.sin((1.0 - t) * omega) / sinom
            sc2 = math.sin(t * omega) / sinom
        else:
            sc1 = 1.0 - t
            sc2 = t

        qw_interp = sc1 * quat[0] + sc2 * q2[0]
        qx_interp = sc1 * quat[1] + sc2 * q2[1]
        qy_interp = sc1 * quat[2] + sc2 * q2[2]
        qz_interp = sc1 * quat[3] + sc2 * q2[3]

        return Quaternion(qw_interp, qx_interp, qy_interp, qz_interp)
