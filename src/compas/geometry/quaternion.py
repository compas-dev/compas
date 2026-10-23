import math
from collections.abc import Iterator
from collections.abc import Sequence
from sys import float_info
from typing import TYPE_CHECKING
from typing import Protocol
from typing import Self
from typing import runtime_checkable

from compas.geometry import Geometry
from compas.geometry import Rotation
from compas.linalg.quaternions import quaternion_canonize
from compas.linalg.quaternions import quaternion_conjugate
from compas.linalg.quaternions import quaternion_is_unit
from compas.linalg.quaternions import quaternion_multiply
from compas.linalg.quaternions import quaternion_norm
from compas.linalg.quaternions import quaternion_unitize
from compas.linalg.transformations import quaternion_from_matrix
from compas.tolerance import TOL

if TYPE_CHECKING:
    from compas.geometry import Frame


@runtime_checkable
class _QuaternionComponents(Protocol):
    def __len__(self) -> int: ...

    def __iter__(self) -> Iterator[float]: ...


class Quaternion(Geometry):
    r"""A quaternion represented by one scalar and three vector components.

    Parameters
    ----------
    w
        The scalar component.
    x
        The X component of the vector part.
    y
        The Y component of the vector part.
    z
        The Z component of the vector part.
    name
        The optional name.

    Notes
    -----
    COMPAS uses the `[w, x, y, z]` convention:

    $$
    q = w + xi + yj + zk
    $$

    A unit quaternion can represent a rotation of $\theta$ around the unit
    axis $(u_x, u_y, u_z)$:

    $$
    q = \cos(\theta / 2) + \sin(\theta / 2)(u_x i + u_y j + u_z k)
    $$

    Quaternion multiplication is associative but not commutative. Multiplying
    `R * Q` composes the rotations represented by `R` and `Q` when both are
    unit quaternions.

    References
    ----------
    * [Quaternion](https://mathworld.wolfram.com/Quaternion.html)
    * [Hamilton's rules](https://mathworld.wolfram.com/HamiltonsRules.html)
    * [transforms3d quaternion implementation](https://github.com/matthew-brett/transforms3d/blob/master/transforms3d/quaternions.py)

    Examples
    --------
    >>> q = Quaternion(1.0, 1.0, 1.0, 1.0).unitized()
    >>> r = Quaternion(0.0, -0.1, 0.2, -0.3).unitized()
    >>> (r * q).is_unit
    True

    """

    # ==========================================================================
    # Data
    # ==========================================================================

    @property
    def __data__(self) -> dict[str, float]:
        return {"w": self.w, "x": self.x, "y": self.y, "z": self.z}

    # ==========================================================================
    # Dunder methods
    # ==========================================================================

    def __init__(self, w: float, x: float, y: float, z: float, name: str | None = None) -> None:
        super().__init__(name=name)
        self._w = 0.0
        self._x = 0.0
        self._y = 0.0
        self._z = 0.0
        self.w = w
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self) -> str:
        return "{0}({1}, {2}, {3}, {4})".format(type(self).__name__, self.w, self.x, self.y, self.z)

    def __str__(self) -> str:
        return "{0}({1}, {2}, {3}, {4})".format(
            type(self).__name__,
            TOL.format_number(self.w),
            TOL.format_number(self.x),
            TOL.format_number(self.y),
            TOL.format_number(self.z),
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, _QuaternionComponents) or len(self) != len(other):
            return False
        return TOL.is_allclose(self, other, rtol=0)

    def __getitem__(self, key: int) -> float:
        if key == 0:
            return self.w
        if key == 1:
            return self.x
        if key == 2:
            return self.y
        if key == 3:
            return self.z
        raise KeyError(key)

    def __setitem__(self, key: int, value: float) -> None:
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

    def __iter__(self) -> Iterator[float]:
        return iter(self.wxyz)

    def __len__(self) -> int:
        return 4

    def __mul__(self, other: "Quaternion | Sequence[float]") -> Self:
        """Multiply operator for two quaternions.

        Parameters
        ----------
        other
            The other quaternion.

        Returns
        -------
        Self
            The Hamilton product of this quaternion and `other`.

        Notes
        -----
        Multiplication of two unit quaternions `R * Q` can be interpreted as
        applying rotation `R` to orientation `Q`. Multiplication is not
        commutative.

        Examples
        --------
        >>> Q = Quaternion(1.0, 1.0, 1.0, 1.0).unitized()
        >>> R = Quaternion(0.0, -0.1, 0.2, -0.3).unitized()
        >>> P = R * Q
        >>> P.is_unit
        True

        """
        p = quaternion_multiply(list(self), list(other))
        return type(self)(p[0], p[1], p[2], p[3])

    # ==========================================================================
    # Properties
    # ==========================================================================

    @property
    def w(self) -> float:
        """The scalar component."""
        return self._w

    @w.setter
    def w(self, w: float) -> None:
        self._w = float(w)

    @property
    def x(self) -> float:
        """The X component of the vector part."""
        return self._x

    @x.setter
    def x(self, x: float) -> None:
        self._x = float(x)

    @property
    def y(self) -> float:
        """The Y component of the vector part."""
        return self._y

    @y.setter
    def y(self, y: float) -> None:
        self._y = float(y)

    @property
    def z(self) -> float:
        """The Z component of the vector part."""
        return self._z

    @z.setter
    def z(self, z: float) -> None:
        self._z = float(z)

    @property
    def wxyz(self) -> list[float]:
        """The components in `[w, x, y, z]` order."""
        return [self.w, self.x, self.y, self.z]

    @property
    def xyzw(self) -> list[float]:
        """The components in `[x, y, z, w]` order."""
        return [self.x, self.y, self.z, self.w]

    @property
    def norm(self) -> float:
        """The Euclidean norm."""
        return quaternion_norm(self)

    @property
    def is_unit(self) -> bool:
        """Whether the quaternion has unit length within the tolerance."""
        return quaternion_is_unit(self)

    # ==========================================================================
    # Constructors
    # ==========================================================================

    @classmethod
    def from_frame(cls, frame: "Frame") -> Self:
        """Creates a quaternion object from a frame.

        Parameters
        ----------
        frame
            The frame.

        Returns
        -------
        Self
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
    def from_matrix(cls, M: Sequence[Sequence[float]]) -> Self:
        """Create a Quaternion from a transformation matrix.

        Parameters
        ----------
        M
            The transformation matrix.

        Returns
        -------
        Self
            The new quaternion.

        Examples
        --------
        >>> from compas.linalg import matrix_from_euler_angles
        >>> ea = [0.2, 0.6, 0.2]
        >>> M = matrix_from_euler_angles(ea)
        >>> Quaternion.from_matrix(M)
        Quaternion(0.949, 0.066, 0.302, 0.066)

        """
        w, x, y, z = quaternion_from_matrix(M)
        return cls(w, x, y, z)

    @classmethod
    def from_rotation(cls, R: Rotation) -> Self:
        """Create a quaternion from a rotation.

        Parameters
        ----------
        R
            The rotation.

        Returns
        -------
        Self
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

    def unitize(self) -> None:
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
        qu = quaternion_unitize(list(self))
        self.w, self.x, self.y, self.z = qu

    def unitized(self) -> Self:
        """Returns a quaternion with a unit-length.

        Returns
        -------
        Self
            The unitized quaternion.

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
        return type(self)(qu[0], qu[1], qu[2], qu[3])

    def canonize(self) -> None:
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
        qc = quaternion_canonize(list(self))
        self.w, self.x, self.y, self.z = qc

    def canonized(self) -> Self:
        """Returns a quaternion in canonic form.

        Returns
        -------
        Self
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
        return type(self)(qc[0], qc[1], qc[2], qc[3])

    def conjugate(self) -> None:
        """Conjugate the quaternion.

        Examples
        --------
        >>> q = Quaternion(1.0, 1.0, 1.0, 1.0)
        >>> q.conjugate()
        >>> q
        Quaternion(1.000, -1.000, -1.000, -1.000)

        """
        qc = quaternion_conjugate(list(self))
        self.w, self.x, self.y, self.z = qc

    def conjugated(self) -> Self:
        """Returns a conjugate quaternion.

        Returns
        -------
        Self
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
        return type(self)(qc[0], qc[1], qc[2], qc[3])

    def dot(self, other: "Quaternion") -> float:
        """Compute the dot product with another quaternion.

        Parameters
        ----------
        other
            The other quaternion.

        Returns
        -------
        float
            The dot product.

        """
        return self.w * other.w + self.x * other.x + self.y * other.y + self.z * other.z

    def slerp(self, other: "Quaternion", t: float) -> Self:
        """Slerp: spherical interpolation of two quaternions.

        Parameters
        ----------
        other
            The other quaternion to interpolate between.
        t
            The interpolation parameter.

        Returns
        -------
        Self
            The interpolated quaternion.

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

        return type(self)(qw_interp, qx_interp, qy_interp, qz_interp)
