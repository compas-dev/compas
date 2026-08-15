from typing import Iterator
from typing import Optional
from typing import Sequence
from typing import Union
from typing import cast
from typing import overload

from typing_extensions import Self

from compas.geometry import Geometry
from compas.geometry import angle_vectors
from compas.geometry import angle_vectors_signed
from compas.geometry import angles_vectors
from compas.geometry import transform_vectors
from compas.linalg.vectors import cross_vectors
from compas.linalg.vectors import dot_vectors
from compas.linalg.vectors import length_vector
from compas.linalg.vectors import subtract_vectors
from compas.tolerance import TOL

from ._typing import CoordinateType
from ._typing import TransformationType


class Vector(Geometry):
    """A vector is defined by XYZ components and a homogenisation factor.

    Parameters
    ----------
    x
        The X component of the vector.
    y
        The Y component of the vector.
    z
        The Z component of the vector.
    name
        The name of the vector.

    Attributes
    ----------
    x : float
        The X coordinate of the point.
    y : float
        The Y coordinate of the point.
    z : float
        The Z coordinate of the point.
    length : float, read-only
        The length of this vector.

    Examples
    --------
    >>> u = Vector(1, 0, 0)
    >>> v = Vector(0, 1, 0)
    >>> print(u)
    Vector(x=1.000, y=0.000, z=0.000)
    >>> print(v)
    Vector(x=0.000, y=1.000, z=0.000)

    >>> u.x
    1.0
    >>> u[0]
    1.0
    >>> u.length
    1.0

    >>> result = u + v
    >>> print(result)
    Vector(x=1.000, y=1.000, z=0.000)

    >>> result = u + [0.0, 1.0, 0.0]
    >>> print(result)
    Vector(x=1.000, y=1.000, z=0.000)

    >>> result = u * 2
    >>> print(result)
    Vector(x=2.000, y=0.000, z=0.000)

    >>> u.dot(v)
    0.0

    >>> w = u.cross(v)
    >>> print(w)
    Vector(x=0.000, y=0.000, z=1.000)

    """

    @property
    def __data__(self) -> list[float]:  # type: ignore[override]
        return list(self)

    @classmethod
    def __from_data__(cls, data: Sequence[float]) -> Self:  # type: ignore[override]
        coordinates = cast(tuple[float, float, float], data)
        return cls(*coordinates)

    def __init__(self, x: float, y: float, z: float = 0.0, name: Optional[str] = None) -> None:
        super(Vector, self).__init__(name=name)
        self._x = 0.0
        self._y = 0.0
        self._z = 0.0
        self._direction: Optional[Vector] = None
        self._magnitude: Optional[float] = None
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self) -> str:
        return "{0}(x={1}, y={2}, z={3})".format(
            type(self).__name__,
            self.x,
            self.y,
            self.z,
        )

    def __str__(self) -> str:
        return "{0}(x={1}, y={2}, z={3})".format(
            type(self).__name__,
            TOL.format_number(self.x),
            TOL.format_number(self.y),
            TOL.format_number(self.z),
        )

    def __len__(self) -> int:
        return 3

    @overload
    def __getitem__(self, key: int) -> float: ...

    @overload
    def __getitem__(self, key: slice) -> list[float]: ...

    def __getitem__(self, key: Union[int, slice]) -> Union[float, list[float]]:
        if isinstance(key, slice):
            return [self[i] for i in range(*key.indices(len(self)))]
        i = key % 3
        if i == 0:
            return self.x
        if i == 1:
            return self.y
        if i == 2:
            return self.z
        raise KeyError

    def __setitem__(self, key: int, value: float) -> None:
        i = key % 3
        if i == 0:
            self.x = value
            return
        if i == 1:
            self.y = value
            return
        if i == 2:
            self.z = value
            return
        raise KeyError

    def __iter__(self) -> Iterator[float]:
        return iter([self.x, self.y, self.z])

    def __eq__(self, other: object) -> bool:
        return TOL.is_allclose(self, other)

    def __add__(self, other: CoordinateType) -> "Vector":
        return Vector(self.x + other[0], self.y + other[1], self.z + other[2])

    def __sub__(self, other: CoordinateType) -> "Vector":
        return Vector(self.x - other[0], self.y - other[1], self.z - other[2])

    def __mul__(self, other: Union[float, CoordinateType]) -> "Vector":
        if isinstance(other, (int, float)):
            return Vector(self.x * other, self.y * other, self.z * other)

        try:
            z = other[2] if len(other) > 2 else 0.0
            return Vector(self.x * other[0], self.y * other[1], self.z * z)
        except TypeError:
            raise TypeError("Cannot cast {} {} to Vector".format(other, type(other)))

    def __truediv__(self, other: Union[float, CoordinateType]) -> "Vector":
        if isinstance(other, (int, float)):
            return Vector(self.x / other, self.y / other, self.z / other)

        try:
            z = other[2] if len(other) > 2 else 0.0
            return Vector(self.x / other[0], self.y / other[1], self.z / z)
        except TypeError:
            raise TypeError("Cannot cast {} {} to Vector".format(other, type(other)))

    def __pow__(self, n: float) -> "Vector":
        return Vector(self.x**n, self.y**n, self.z**n)

    def __neg__(self) -> Self:
        return self.scaled(-1.0)

    def __iadd__(self, other: CoordinateType) -> Self:
        self.x += other[0]
        self.y += other[1]
        self.z += other[2]
        return self

    def __isub__(self, other: CoordinateType) -> Self:
        self.x -= other[0]
        self.y -= other[1]
        self.z -= other[2]
        return self

    def __imul__(self, n: float) -> Self:
        self.x *= n
        self.y *= n
        self.z *= n
        return self

    def __itruediv__(self, n: float) -> Self:
        self.x /= n
        self.y /= n
        self.z /= n
        return self

    def __ipow__(self, n: float) -> Self:
        self.x **= n
        self.y **= n
        self.z **= n
        return self

    def __rmul__(self, n: float) -> "Vector":
        return self.__mul__(n)

    def __radd__(self, other: CoordinateType) -> "Vector":
        return self.__add__(other)

    def __rsub__(self, other: CoordinateType) -> "Vector":
        try:
            z = other[2] if len(other) > 2 else 0.0
            return Vector(other[0] - self.x, other[1] - self.y, z - self.z)
        except TypeError:
            raise TypeError("Cannot cast {} {} to Vector".format(other, type(other)))

    def __rtruediv__(self, other: CoordinateType) -> "Vector":
        try:
            z = other[2] if len(other) > 2 else 0.0
            return Vector(other[0] / self.x, other[1] / self.y, z / self.z)
        except TypeError:
            raise TypeError("Cannot cast {} {} to Vector".format(other, type(other)))

    # ==========================================================================
    # Properties
    # ==========================================================================

    @property
    def x(self) -> float:
        return self._x

    @x.setter
    def x(self, x: float) -> None:
        self._x = float(x)
        self._direction = None
        self._magnitude = None

    @property
    def y(self) -> float:
        return self._y

    @y.setter
    def y(self, y: float) -> None:
        self._y = float(y)
        self._direction = None
        self._magnitude = None

    @property
    def z(self) -> float:
        return self._z

    @z.setter
    def z(self, z: float) -> None:
        self._z = float(z)
        self._direction = None
        self._magnitude = None

    @property
    def magnitude(self) -> float:
        if self._magnitude is None:
            self._magnitude = length_vector(self)
        return self._magnitude

    @property
    def length(self) -> float:
        return self.magnitude

    @property
    def direction(self) -> "Vector":
        if not self._direction:
            self._direction = self.unitized()
        return self._direction

    # ==========================================================================
    # Constructors
    # ==========================================================================

    @classmethod
    def Xaxis(cls) -> Self:
        """Construct a unit vector along the X axis.

        Returns
        -------
        Vector
            A vector with components `x = 1.0, y = 0.0, z = 0.0`.

        Examples
        --------
        >>> Vector.Xaxis() == [1, 0, 0]
        True

        """
        return cls(1.0, 0.0, 0.0)

    @classmethod
    def Yaxis(cls) -> Self:
        """Construct a unit vector along the Y axis.

        Returns
        -------
        Vector
            A vector with components `x = 0.0, y = 1.0, z = 0.0`.

        Examples
        --------
        >>> Vector.Yaxis() == [0, 1, 0]
        True

        """
        return cls(0.0, 1.0, 0.0)

    @classmethod
    def Zaxis(cls) -> Self:
        """Construct a unit vector along the Z axis.

        Returns
        -------
        Vector
            A vector with components `x = 0.0, y = 0.0, z = 1.0`.

        Examples
        --------
        >>> Vector.Zaxis() == [0, 0, 1]
        True

        """
        return cls(0.0, 0.0, 1.0)

    @classmethod
    def from_start_end(cls, start: CoordinateType, end: CoordinateType) -> Self:
        """Construct a vector from start and end points.

        Parameters
        ----------
        start
            The start point.
        end
            The end point.

        Returns
        -------
        Vector
            The vector from start to end.

        Examples
        --------
        >>> vector = Vector.from_start_end([1.0, 0.0, 0.0], [1.0, 1.0, 0.0])
        >>> print(vector)
        Vector(x=0.000, y=1.000, z=0.000)

        """
        v = subtract_vectors(end, start)
        coordinates = cast(tuple[float, float, float], v)
        return cls(*coordinates)

    # ==========================================================================
    # Static
    # ==========================================================================

    @staticmethod
    def transform_collection(collection: Sequence["Vector"], transformation: TransformationType) -> None:
        """Transform a collection of vector objects.

        Parameters
        ----------
        collection
            The collection of vectors.
        transformation
            The transformation.

        Examples
        --------
        >>> from compas.geometry import Rotation
        >>> R = Rotation.from_axis_and_angle(Vector.Zaxis(), math.radians(90))
        >>> u = Vector(1.0, 0.0, 0.0)
        >>> vectors = [u]
        >>> Vector.transform_collection(vectors, R)
        >>> v = vectors[0]
        >>> print(v)
        Vector(x=0.000, y=1.000, z=0.000)
        >>> u is v
        True

        """
        data = transform_vectors(collection, transformation)
        for vector, xyz in zip(collection, data):
            vector.x = xyz[0]
            vector.y = xyz[1]
            vector.z = xyz[2]

    @staticmethod
    def transformed_collection(collection: Sequence["Vector"], transformation: TransformationType) -> list["Vector"]:
        """Create a collection of transformed vectors.

        Parameters
        ----------
        collection
            The collection of vectors.
        transformation
            The transformation.

        Returns
        -------
        list[Vector]
            The transformed vectors.

        Examples
        --------
        >>> from compas.geometry import Rotation
        >>> R = Rotation.from_axis_and_angle(Vector.Zaxis(), math.radians(90))
        >>> u = Vector(1.0, 0.0, 0.0)
        >>> vectors = [u]
        >>> vectors = Vector.transformed_collection(vectors, R)
        >>> v = vectors[0]
        >>> print(v)
        Vector(x=0.000, y=1.000, z=0.000)
        >>> u is v
        False

        """
        vectors = [vector.copy() for vector in collection]
        Vector.transform_collection(vectors, transformation)
        return vectors

    @staticmethod
    def length_vectors(vectors: Sequence[CoordinateType]) -> list[float]:
        """Compute the length of multiple vectors.

        Parameters
        ----------
        vectors
            A list of vectors.

        Returns
        -------
        list[float]
            A list of lengths.

        Examples
        --------
        >>> result = Vector.length_vectors([[1.0, 0.0, 0.0], [2.0, 0.0, 0.0]])
        >>> print(result)
        [1.0, 2.0]

        """
        return [length_vector(vector) for vector in vectors]

    @staticmethod
    def sum_vectors(vectors: Sequence[CoordinateType]) -> "Vector":
        """Compute the sum of multiple vectors.

        Parameters
        ----------
        vectors
            A list of vectors.

        Returns
        -------
        Vector
            A vector that is the sum of the vectors.

        Examples
        --------
        >>> result = Vector.sum_vectors([[1.0, 0.0, 0.0], [2.0, 0.0, 0.0]])
        >>> print(result)
        Vector(x=3.000, y=0.000, z=0.000)

        """
        data = [sum(axis) for axis in zip(*vectors)]
        coordinates = cast(tuple[float, float, float], data)
        return Vector(*coordinates)

    @staticmethod
    def dot_vectors(left: Sequence[CoordinateType], right: Sequence[CoordinateType]) -> list[float]:
        """Compute the dot product of two lists of vectors.

        Parameters
        ----------
        left
            A list of vectors.
        right
            A list of vectors.

        Returns
        -------
        list[float]
            A list of dot products.

        Examples
        --------
        >>> result = Vector.dot_vectors([[1.0, 0.0, 0.0], [2.0, 0.0, 0.0]], [[1.0, 0.0, 0.0], [2.0, 0.0, 0.0]])
        >>> print(result)
        [1.0, 4.0]

        """
        return [dot_vectors(u, v) for u, v in zip(left, right)]

    @staticmethod
    def cross_vectors(left: Sequence[CoordinateType], right: Sequence[CoordinateType]) -> list["Vector"]:
        """Compute the cross product of two lists of vectors.

        Parameters
        ----------
        left
            A list of vectors.
        right
            A list of vectors.

        Returns
        list[Vector]
            A list of cross products.

        Examples
        --------
        >>> result = Vector.cross_vectors([[1.0, 0.0, 0.0], [2.0, 0.0, 0.0]], [[0.0, 1.0, 0.0], [0.0, 0.0, 2.0]])
        >>> print(result)
        [Vector(x=0.000, y=0.000, z=1.000), Vector(x=0.000, y=-4.000, z=0.000)]

        """
        # cross_vectors(u,v) from src\compas\geometry\_core\_algebra.py
        vectors = []
        for u, v in zip(left, right):
            coordinates = cast(tuple[float, float, float], cross_vectors(u, v))
            vectors.append(Vector(*coordinates))
        return vectors

    @staticmethod
    def angles_vectors(left: Sequence[CoordinateType], right: Sequence[CoordinateType]) -> list[tuple[float, float]]:
        """Compute both angles between corresponding pairs of two lists of vectors.

        Parameters
        ----------
        left
            A list of vectors.
        right
            A list of vectors.

        Returns
        -------
        list[tuple[float, float]]
            A list of angle pairs.

        Examples
        --------
        >>> result = Vector.angles_vectors([[1.0, 0.0, 0.0], [2.0, 0.0, 0.0]], [[0.0, 1.0, 0.0], [0.0, 0.0, 2.0]])
        >>> print(result)
        [(1.5707963267948966, 4.71238898038469), (1.5707963267948966, 4.71238898038469)]

        """
        return [angles_vectors(u, v) for u, v in zip(left, right)]

    @staticmethod
    def angle_vectors(left: Sequence[CoordinateType], right: Sequence[CoordinateType]) -> list[float]:
        """Compute the smallest angle between corresponding pairs of two lists of vectors.

        Parameters
        ----------
        left
            A list of vectors.
        right
            A list of vectors.

        Returns
        -------
        list[float]
            A list of angles.

        Examples
        --------
        >>> result = Vector.angle_vectors([[1.0, 0.0, 0.0], [2.0, 0.0, 0.0]], [[0.0, 1.0, 0.0], [0.0, 0.0, 2.0]])
        >>> print(result)
        [1.5707963267948966, 1.5707963267948966]

        """
        return [angle_vectors(u, v) for u, v in zip(left, right)]

    # ==========================================================================
    # Helpers
    # ==========================================================================

    def copy(self) -> Self:
        """Make a copy of this vector.

        Returns
        -------
        Vector
            The copy.

        Examples
        --------
        >>> u = Vector(0.0, 0.0, 0.0)
        >>> v = u.copy()
        >>> u == v
        True
        >>> u is v
        False

        """
        cls = type(self)
        return cls(self.x, self.y, self.z)

    # ==========================================================================
    # Methods
    # ==========================================================================

    def unitize(self) -> None:
        """Scale this vector to unit length.

        Examples
        --------
        >>> u = Vector(1.0, 2.0, 3.0)
        >>> u.unitize()
        >>> u.length
        1.0

        """
        length = self.length
        self.x = self.x / length
        self.y = self.y / length
        self.z = self.z / length

    def unitized(self) -> Self:
        """Returns a unitized copy of this vector.

        Returns
        -------
        Vector
            A unitized copy of the vector.

        Examples
        --------
        >>> u = Vector(1.0, 2.0, 3.0)
        >>> v = u.unitized()
        >>> u.length == 1.0
        False
        >>> v.length == 1.0
        True

        """
        v = self.copy()
        v.unitize()
        return v

    def invert(self) -> None:
        """Invert the direction of this vector

        Notes
        -----
        a negation of a vector is similar to inverting a vector

        Examples
        --------
        >>> u = Vector(1.0, 0.0, 0.0)
        >>> v = u.copy()
        >>> u.invert()
        >>> u == v
        False
        >>> u.invert()
        >>> u == v
        True
        >>> v == --v
        True

        """
        self.scale(-1.0)

    flip = invert

    def inverted(self) -> Self:
        """Returns a inverted copy of this vector

        Returns
        -------
        Vector
            The inverted copy.

        Examples
        --------
        >>> u = Vector(1.0, 0.0, 0.0)
        >>> v = u.inverted()
        >>> w = u + v
        >>> w.length
        0.0

        """
        return self.scaled(-1.0)

    flipped = inverted

    def scale(self, n: float) -> None:
        """Scale this vector by a factor n.

        Parameters
        ----------
        n
            The scaling factor.

        Examples
        --------
        >>> u = Vector(1.0, 0.0, 0.0)
        >>> u.scale(3.0)
        >>> u.length
        3.0

        """
        self.x *= n
        self.y *= n
        self.z *= n

    def scaled(self, n: float) -> Self:
        """Returns a scaled copy of this vector.

        Parameters
        ----------
        n
            The scaling factor.

        Returns
        -------
        Vector
            A scaled copy of the vector.

        Examples
        --------
        >>> u = Vector(1.0, 0.0, 0.0)
        >>> v = u.scaled(3.0)
        >>> u.length
        1.0
        >>> v.length
        3.0

        """
        v = self.copy()
        v.scale(n)
        return v

    def dot(self, other: CoordinateType) -> float:
        """The dot product of this vector and another vector.

        Parameters
        ----------
        other
            The other vector.

        Returns
        -------
        float
            The dot product.

        Examples
        --------
        >>> u = Vector(1.0, 0.0, 0.0)
        >>> v = Vector(0.0, 1.0, 0.0)
        >>> u.dot(v)
        0.0

        """
        return dot_vectors(self, other)

    def cross(self, other: CoordinateType) -> "Vector":
        """The cross product of this vector and another vector.

        Parameters
        ----------
        other
            The other vector.

        Returns
        -------
        Vector
            The cross product.

        Examples
        --------
        >>> u = Vector(1.0, 0.0, 0.0)
        >>> v = Vector(0.0, 1.0, 0.0)
        >>> w = u.cross(v)
        >>> print(w)
        Vector(x=0.000, y=0.000, z=1.000)

        """
        coordinates = cast(tuple[float, float, float], cross_vectors(self, other))
        return Vector(*coordinates)

    def angle(self, other: CoordinateType, degrees: bool = False) -> float:
        """Compute the smallest angle between this vector and another vector.

        Parameters
        ----------
        other
            The other vector.
        degrees
            If True, return the angle in degrees.

        Returns
        -------
        float
            The smallest angle between the two vectors.

        Examples
        --------
        >>> u = Vector(1.0, 0.0, 0.0)
        >>> v = Vector(0.0, 1.0, 0.0)
        >>> u.angle(v) == 0.5 * math.pi
        True

        """
        return angle_vectors(self, other, deg=degrees)

    def angle_signed(self, other: CoordinateType, normal: CoordinateType) -> float:
        """Compute the signed angle between this vector and another vector.

        Parameters
        ----------
        other
            The other vector.
        normal
            The plane's normal spanned by this and the other vector.

        Returns
        -------
        float
            The signed angle between the two vectors.

        Examples
        --------
        >>> u = Vector(1.0, 0.0, 0.0)
        >>> v = Vector(0.0, 1.0, 0.0)
        >>> u.angle_signed(v, Vector(0.0, 0.0, 1.0)) == 0.5 * math.pi
        True
        >>> u.angle_signed(v, Vector(0.0, 0.0, -1.0)) == -0.5 * math.pi
        True

        """
        return angle_vectors_signed(self, other, normal)

    def angles(self, other: CoordinateType) -> tuple[float, float]:
        """Compute both angles between this vector and another vector.

        Parameters
        ----------
        other
            The other vector.

        Returns
        -------
        tuple[float, float]
            The angles between the two vectors, with the smallest angle first.

        Examples
        --------
        >>> u = Vector(1.0, 0.0, 0.0)
        >>> v = Vector(0.0, 1.0, 0.0)
        >>> u.angles(v)[0] == 0.5 * math.pi
        True

        """
        return angles_vectors(self, other)

    def component(self, other: CoordinateType) -> "Vector":
        """Compute the component of this vector in the direction of another vector.

        Parameters
        ----------
        other
            The other vector.

        Returns
        -------
        Vector
            The component in the direction of the other vector.

        """
        cosa = self.dot(other)
        component = Vector(other[0], other[1], other[2])
        L = component.length
        component.scale(cosa / L)
        return component

    def transform(self, transformation: TransformationType) -> None:
        """Transform this vector.

        Parameters
        ----------
        transformation
            The transformation.

        Examples
        --------
        >>> from compas.geometry import Rotation
        >>> u = Vector(1.0, 0.0, 0.0)
        >>> R = Rotation.from_axis_and_angle([0.0, 0.0, 1.0], math.radians(90))
        >>> u.transform(R)
        >>> print(u)
        Vector(x=0.000, y=1.000, z=0.000)

        """
        transformed_vector = transform_vectors([self], transformation)[0]
        self.x = transformed_vector[0]
        self.y = transformed_vector[1]
        self.z = transformed_vector[2]

    def transformed(self, transformation: TransformationType) -> Self:
        """Return a transformed copy of this vector.

        Parameters
        ----------
        transformation
            The transformation.

        Returns
        -------
        Vector
            The transformed copy.

        Examples
        --------
        >>> from compas.geometry import Rotation
        >>> u = Vector(1.0, 0.0, 0.0)
        >>> R = Rotation.from_axis_and_angle([0.0, 0.0, 1.0], math.radians(90))
        >>> v = u.transformed(R)
        >>> print(v)
        Vector(x=0.000, y=1.000, z=0.000)

        """
        vector = self.copy()
        vector.transform(transformation)
        return vector
