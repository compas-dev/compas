from collections.abc import Iterator
from collections.abc import Sequence
from typing import TYPE_CHECKING
from typing import Self

from compas._typing import CoordinateType
from compas.data import Data
from compas.linalg.matrices import matrix_determinant
from compas.linalg.matrices import matrix_inverse
from compas.linalg.matrices import multiply_matrices
from compas.linalg.matrices import transpose_matrix
from compas.linalg.transformations import basis_vectors_from_matrix
from compas.linalg.transformations import decompose_matrix
from compas.linalg.transformations import identity_matrix
from compas.linalg.transformations import matrix_from_euler_angles
from compas.linalg.transformations import matrix_from_frame
from compas.linalg.transformations import matrix_from_translation
from compas.linalg.transformations import translation_from_matrix
from compas.tolerance import TOL

if TYPE_CHECKING:
    from compas.geometry import Frame
    from compas.geometry import Projection
    from compas.geometry import Rotation
    from compas.geometry import Scale
    from compas.geometry import Shear
    from compas.geometry import Translation
    from compas.geometry import Vector

Matrix = list[list[float]]


class Transformation(Data):
    """Class representing a general 4x4 transformation matrix.

    It is the base class for transformations like `Rotation`,
    `Translation`, `Scale`, `Reflection`,
    `Projection` and `Shear`.

    The class allows to concatenate Transformations by multiplication, to
    calculate the inverse transformation and to decompose a transformation into
    its components of rotation, translation, scale, shear, and perspective.
    The matrix follows the row-major order, such that translation components
    x, y, z are in the right column of the matrix, i.e. `M[0][3], M[1][3],
    M[2][3] = x, y, z`.

    Parameters
    ----------
    matrix
        The 4x4 transformation matrix.
    name
        The name of the transformation.

    Examples
    --------
    >>> from compas.geometry import Frame
    >>> f1 = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
    >>> T = Transformation.from_frame(f1)
    >>> Sc, Sh, R, Tl, P = T.decomposed()
    >>> Tinv = T.inverse()

    """

    # ==========================================================================
    # Data
    # ==========================================================================

    @property
    def __data__(self) -> dict[str, Matrix]:
        return {"matrix": self.matrix}

    # ==========================================================================
    # Dunder methods
    # ==========================================================================

    def __init__(self, matrix: Matrix | None = None, name: str | None = None) -> None:
        super().__init__(name=name)
        if not matrix:
            matrix = identity_matrix(4)
        self.matrix = matrix

    def __mul__(self, other: "Transformation") -> "Transformation":
        return self.concatenated(other)

    def __imul__(self, other: "Transformation") -> "Transformation":
        return self.concatenated(other)

    def __getitem__(self, key: tuple[int, int]) -> float:
        i, j = key
        return self.matrix[i][j]

    def __setitem__(self, key: tuple[int, int], value: float) -> None:
        i, j = key
        self.matrix[i][j] = value

    def __iter__(self) -> Iterator[list[float]]:
        return iter(self.matrix)

    def __eq__(self, other: object, tol: float | None = None) -> bool:
        try:
            A = self.matrix
            B = getattr(other, "matrix")
            return TOL.is_allclose(A, B, rtol=0, atol=tol)
        except (AttributeError, TypeError):
            return False

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __repr__(self) -> str:
        if type(self) is Transformation:
            return f"Transformation({self.matrix!r})"
        return f"{type(self).__name__}({self.matrix!r}, check=False)"

    def __str__(self) -> str:
        s = "[[%s],\n" % ",".join([("%.4f" % n).rjust(10) for n in self.matrix[0]])
        s += " [%s],\n" % ",".join([("%.4f" % n).rjust(10) for n in self.matrix[1]])
        s += " [%s],\n" % ",".join([("%.4f" % n).rjust(10) for n in self.matrix[2]])
        s += " [%s]]\n" % ",".join([("%.4f" % n).rjust(10) for n in self.matrix[3]])
        return s

    def __len__(self) -> int:
        return len(self.matrix)

    # ==========================================================================
    # Properties
    # ==========================================================================

    @property
    def scale(self) -> "Scale":
        """The scale component of the transformation."""
        S, H, R, T, P = self.decomposed()
        return S

    @property
    def shear(self) -> "Shear":
        """The shear component of the transformation."""
        S, H, R, T, P = self.decomposed()
        return H

    @property
    def rotation(self) -> "Rotation":
        """The rotation component of the transformation."""
        S, H, R, T, P = self.decomposed()
        return R

    @property
    def translation(self) -> "Translation":
        """The translation component of the transformation."""
        S, H, R, T, P = self.decomposed()
        return T

    @property
    def projection(self) -> "Projection":
        """The projection component of the transformation."""
        S, H, R, T, P = self.decomposed()
        return P

    @property
    def translation_vector(self) -> "Vector":
        """The translation component as a vector."""
        from compas.geometry import Vector

        vector = translation_from_matrix(self.matrix)
        return Vector(vector[0], vector[1], vector[2])

    @property
    def basis_vectors(self) -> tuple["Vector", "Vector"]:
        """The first two basis vectors of the rotation component."""
        from compas.geometry import Vector

        x, y = basis_vectors_from_matrix(self.rotation.matrix)
        return Vector(x[0], x[1], x[2]), Vector(y[0], y[1], y[2])

    @property
    def list(self) -> list[float]:
        """The matrix entries flattened in row-major order."""
        return [a for c in self.matrix for a in c]

    @property
    def determinant(self) -> float:
        """The determinant of the transformation matrix."""
        return matrix_determinant(self.matrix)

    # ==========================================================================
    # Constructors
    # ==========================================================================

    @classmethod
    def from_matrix(cls, matrix: Matrix) -> Self:
        """Creates a transformation from a list[list[float]] object.

        Parameters
        ----------
        matrix
            The 4x4 transformation matrix.

        Returns
        -------
        `compas.geometry.Transformation`
            The transformation.

        """
        return cls(matrix)

    @classmethod
    def from_list(cls, numbers: Sequence[float]) -> Self:
        """Creates a transformation from a list of 16 numbers.

        Parameters
        ----------
        numbers
            A list of 16 numbers

        Returns
        -------
        `compas.geometry.Transformation`
            The transformation.

        Notes
        -----
        Since the transformation matrix follows the row-major order, the
        translational components must be at the list's indices 3, 7, 11.

        Examples
        --------
        >>> numbers = [1, 0, 0, 3, 0, 1, 0, 4, 0, 0, 1, 5, 0, 0, 0, 1]
        >>> T = Transformation.from_list(numbers)

        """
        matrix = identity_matrix(4)
        for i in range(4):
            for j in range(4):
                matrix[i][j] = float(numbers[i * 4 + j])
        return cls(matrix)

    @classmethod
    def from_euler_angles(
        cls,
        euler_angles: Sequence[float],
        static: bool = True,
        axes: str = "xyz",
        point: CoordinateType = (0.0, 0.0, 0.0),
    ) -> Self:
        """Construct a transformation from a rotation represented by Euler angles.

        Parameters
        ----------
        euler_angles
            Three numbers that represent the angles of rotations about the defined axes.
        static
            If True the rotations are applied to a static frame.
            If False, to a rotational.
        axes
            A 3 character string specifying the order of the axes.
        point
            The point of the frame.

        Returns
        -------
        `compas.geometry.Transformation`
            The transformation.

        """
        R = matrix_from_euler_angles(euler_angles, static, axes)
        T = matrix_from_translation(point)
        M = multiply_matrices(T, R)
        return cls.from_matrix(M)

    # should not one of the two just have a "to" function
    @classmethod
    def from_frame(cls, frame: "Frame") -> Self:
        """Construct a transformation from world XY to frame.

        Parameters
        ----------
        frame
            A frame describing the targeted Cartesian coordinate system.

        Returns
        -------
        `compas.geometry.Transformation`
            The transformation.

        Notes
        -----
        It is the same as from_frame_to_frame(Frame.worldXY(), frame).

        Examples
        --------
        >>> from compas.geometry import Frame
        >>> f1 = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
        >>> T = Transformation.from_frame(f1)
        >>> f2 = Frame.from_transformation(T)
        >>> f1 == f2
        True

        """
        return cls(matrix_from_frame(frame))

    @classmethod
    def from_frame_to_frame(cls, frame_from: "Frame", frame_to: "Frame") -> Self:
        """Construct a transformation between two frames.

        This transformation allows to transform geometry from one Cartesian
        coordinate system defined by `frame_from` to another Cartesian
        coordinate system defined by `frame_to`.

        Parameters
        ----------
        frame_from
            A frame defining the original Cartesian coordinate system.
        frame_to
            A frame defining the targeted Cartesian coordinate system.

        Returns
        -------
        `compas.geometry.Transformation`
            The transformation.

        Examples
        --------
        >>> from compas.geometry import Frame
        >>> f1 = Frame([2, 2, 2], [0.12, 0.58, 0.81], [-0.80, 0.53, -0.26])
        >>> f2 = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
        >>> T = Transformation.from_frame_to_frame(f1, f2)
        >>> f1.transform(T)
        >>> f1 == f2
        True

        """
        T1 = cls.from_frame(frame_from)
        T2 = cls.from_frame(frame_to)
        return cls(multiply_matrices(T2.matrix, matrix_inverse(T1.matrix)))

    @classmethod
    def from_change_of_basis(cls, frame_from: "Frame", frame_to: "Frame") -> Self:
        """Construct a change of basis transformation between two frames.

        A basis change is essentially a remapping of geometry from one
        coordinate system to another.

        Parameters
        ----------
        frame_from
            A frame defining the original Cartesian coordinate system.
        frame_to
            A frame defining the targeted Cartesian coordinate system.

        Returns
        -------
        `compas.geometry.Transformation`
            The transformation representing a change of basis.

        Examples
        --------
        >>> from compas.geometry import Point, Frame
        >>> f1 = Frame([2, 2, 2], [0.12, 0.58, 0.81], [-0.80, 0.53, -0.26])
        >>> f2 = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
        >>> T = Transformation.from_change_of_basis(f1, f2)
        >>> p_f1 = Point(1, 1, 1)  # point in f1
        >>> point = p_f1.transformed(T)  # point represented in f2
        >>> print(point)
        Point(x=1.395, y=0.955, z=1.934)

        """
        T1 = cls.from_frame(frame_from)
        T2 = cls.from_frame(frame_to)
        return cls(multiply_matrices(matrix_inverse(T2.matrix), T1.matrix))

    # ==========================================================================
    # Methods
    # ==========================================================================

    def transpose(self) -> None:
        """Transpose the matrix of this transformation.

        Returns
        -------
        None
            The transformation is transposed in-place.

        """
        self.matrix = transpose_matrix(self.matrix)

    def transposed(self) -> Self:
        """Create a transposed copy of this transformation.

        Returns
        -------
        `compas.geometry.Transformation`
            The transposed transformation object.

        """
        T = self.copy()
        T.transpose()
        return T

    def invert(self) -> None:
        """Invert this transformation.

        Returns
        -------
        None
            The transformation is transposed in-place.

        """
        self.matrix = matrix_inverse(self.matrix)

    def inverse(self) -> Self:
        """Returns the inverse transformation.

        Returns
        -------
        `compas.geometry.Transformation`
            The inverse transformation.

        Examples
        --------
        >>> from compas.geometry import Frame
        >>> f = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
        >>> T = Transformation.from_frame(f)
        >>> I = Transformation(identity_matrix(4))
        >>> I == T * T.inverse()
        True

        """
        T = self.copy()
        T.invert()
        return T

    inverted = inverse

    def decomposed(self) -> tuple["Scale", "Shear", "Rotation", "Translation", "Projection"]:
        """Decompose the `Transformation` into its components.

        Returns
        -------
        tuple[Scale, Shear, Rotation, Translation, Projection]
            The scale, shear, rotation, translation, and projection components,
            in that order.

        Examples
        --------
        >>> from compas.geometry import Scale, Translation, Rotation
        >>> trans1 = [1, 2, 3]
        >>> angle1 = [-2.142, 1.141, -0.142]
        >>> scale1 = [0.123, 2, 0.5]
        >>> T1 = Translation.from_vector(trans1)
        >>> R1 = Rotation.from_euler_angles(angle1)
        >>> S1 = Scale.from_factors(scale1)
        >>> M = T1 * R1 * S1
        >>> S, H, R, T, P = M.decomposed()
        >>> S1 == S
        True
        >>> R1 == R
        True
        >>> T1 == T
        True

        """
        from .projection import Projection
        from .rotation import Rotation
        from .scale import Scale
        from .shear import Shear
        from .translation import Translation

        s, h, a, t, p = decompose_matrix(self.matrix)
        S = Scale.from_factors(s)
        H = Shear.from_entries(h)
        R = Rotation.from_euler_angles(a, static=True, axes="xyz")
        T = Translation.from_vector(t)
        P = Projection.from_entries(p)
        return S, H, R, T, P

    def concatenate(self, other: "Transformation") -> None:
        """Concatenate another transformation to this transformation.

        Parameters
        ----------
        other
            The transformation object to concatenate.

        Returns
        -------
        None
            This transformation object is changed in-place.

        Notes
        -----
        Rz * Ry * Rx means that Rx is first transformation, Ry second, and Rz third.

        """
        self.matrix = multiply_matrices(self.matrix, other.matrix)

    def concatenated(self, other: "Transformation") -> "Transformation":
        """Concatenate two transformations into one `Transformation`.

        Parameters
        ----------
        other
            The transformation object to concatenate.

        Returns
        -------
        `compas.geometry.Transformation`
            The new transformation that is the concatenation of this one and the other.

        Notes
        -----
        Rz * Ry * Rx means that Rx is first transformation, Ry second, and Rz third.

        """
        cls = type(self)
        if isinstance(other, cls):
            return cls(multiply_matrices(self.matrix, other.matrix))
        return Transformation(multiply_matrices(self.matrix, other.matrix))
