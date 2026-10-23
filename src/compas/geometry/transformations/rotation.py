from typing import TYPE_CHECKING
from typing import Self

from compas._typing import CoordinatesType
from compas._typing import CoordinateType
from compas._typing import FloatSequenceType
from compas.itertools import flatten
from compas.linalg.transformations import axis_and_angle_from_matrix
from compas.linalg.transformations import basis_vectors_from_matrix
from compas.linalg.transformations import decompose_matrix
from compas.linalg.transformations import euler_angles_from_matrix
from compas.linalg.transformations import matrix_from_axis_and_angle
from compas.linalg.transformations import matrix_from_euler_angles
from compas.linalg.transformations import matrix_from_frame
from compas.linalg.transformations import matrix_from_quaternion
from compas.linalg.vectors import cross_vectors
from compas.linalg.vectors import length_vector
from compas.linalg.vectors import normalize_vector
from compas.tolerance import TOL

from .transformation import Matrix
from .transformation import Transformation

if TYPE_CHECKING:
    from compas.geometry import Quaternion
    from compas.geometry import Vector


class Rotation(Transformation):
    """Class representing a rotation transformation.

    The class contains methods for converting rotation matrices to axis-angle
    representations, Euler angles, quaternion and basis vectors.

    Parameters
    ----------
    matrix
        A 4x4 matrix (or similar) representing a rotation.
    check
        If `True`, the provided matrix will be checked for validity.
    name
        The name of the transformation.

    Raises
    ------
    ValueError
        If `check` is `True` and the provided transformation matrix is not a rotation.

    Examples
    --------
    >>> from compas.geometry import Frame
    >>> f1 = Frame([0, 0, 0], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
    >>> R = Rotation.from_frame(f1)
    >>> args = False, "xyz"
    >>> alpha, beta, gamma = R.euler_angles(*args)
    >>> xaxis, yaxis, zaxis = [1, 0, 0], [0, 1, 0], [0, 0, 1]
    >>> Rx = Rotation.from_axis_and_angle(xaxis, alpha)
    >>> Ry = Rotation.from_axis_and_angle(yaxis, beta)
    >>> Rz = Rotation.from_axis_and_angle(zaxis, gamma)
    >>> f2 = Frame.worldXY()
    >>> f1 == f2.transformed(Rx * Ry * Rz)
    True

    """

    # ==========================================================================
    # Dunder methods
    # ==========================================================================

    def __init__(self, matrix: Matrix | None = None, check: bool = False, name: str | None = None) -> None:
        if matrix and check:
            _, _, angles, _, _ = decompose_matrix(matrix)
            if not TOL.is_allclose(flatten(matrix), flatten(matrix_from_euler_angles(angles))):
                raise ValueError("This is not a proper rotation matrix.")
        super().__init__(matrix=matrix, name=name)

    # ==========================================================================
    # Properties
    # ==========================================================================

    @property
    def quaternion(self) -> "Quaternion":
        """The quaternion representation of this rotation."""
        from compas.geometry import Quaternion

        return Quaternion.from_matrix(self.matrix)

    @property
    def axis_and_angle(self) -> tuple["Vector", float]:
        """The unit axis and angle representation of this rotation."""
        from compas.geometry import Vector

        axis, angle = axis_and_angle_from_matrix(self.matrix)
        return Vector(axis[0], axis[1], axis[2]), angle

    @property
    def axis_angle_vector(self) -> "Vector":
        """The axis-angle vector representation of this rotation."""
        axis, angle = self.axis_and_angle
        return axis.scaled(angle)

    @property
    def basis_vectors(self) -> tuple["Vector", "Vector"]:
        """The first two basis vectors represented by this rotation."""
        from compas.geometry import Vector

        xaxis, yaxis = basis_vectors_from_matrix(self.matrix)
        return Vector(xaxis[0], xaxis[1], xaxis[2]), Vector(yaxis[0], yaxis[1], yaxis[2])

    # ==========================================================================
    # Constructors
    # ==========================================================================

    @classmethod
    def from_axis_and_angle(cls, axis: CoordinateType, angle: float, point: CoordinateType | None = None) -> Self:
        """Construct a rotation transformation from a rotation axis and an angle and an optional point of rotation.

        The rotation is based on the right hand rule, i.e. anti-clockwise if the
        axis of rotation points towards the observer.

        Parameters
        ----------
        axis
            Three numbers that represent the axis of rotation.
        angle
            The rotation angle in radians.
        point
            A point to perform a rotation around an origin other than [0, 0, 0].

        Returns
        -------
        Self
            The constructed rotation.

        Notes
        -----
        The rotation is based on the right hand rule, i.e. anti-clockwise
        if the axis of rotation points towards the observer.

        Examples
        --------
        >>> axis1 = normalize_vector([-0.043, -0.254, 0.617])
        >>> angle1 = 0.1
        >>> R = Rotation.from_axis_and_angle(axis1, angle1)
        >>> axis2, angle2 = R.axis_and_angle
        >>> TOL.is_allclose(axis1, axis2)
        True
        >>> TOL.is_allclose([angle1], [angle2])
        True

        """
        matrix = matrix_from_axis_and_angle(axis, angle, point=point)
        return cls(matrix)

    @classmethod
    def from_basis_vectors(cls, xaxis: CoordinateType, yaxis: CoordinateType) -> Self:
        """Construct a rotation transformation from basis vectors (= orthonormal vectors).

        Parameters
        ----------
        xaxis
            The x-axis of the frame.
        yaxis
            The y-axis of the frame.

        Returns
        -------
        Self
            The constructed rotation.

        Examples
        --------
        >>> xaxis = [0.68, 0.68, 0.27]
        >>> yaxis = [-0.67, 0.73, -0.15]
        >>> R = Rotation.from_basis_vectors(xaxis, yaxis)

        """
        xaxis = normalize_vector(xaxis)
        yaxis = normalize_vector(yaxis)
        zaxis = cross_vectors(xaxis, yaxis)
        yaxis = cross_vectors(zaxis, xaxis)
        matrix = [
            [xaxis[0], yaxis[0], zaxis[0], 0],
            [xaxis[1], yaxis[1], zaxis[1], 0],
            [xaxis[2], yaxis[2], zaxis[2], 0],
            [0, 0, 0, 1],
        ]
        return cls(matrix)

    @classmethod
    def from_frame(cls, frame: CoordinatesType) -> Self:
        """Construct a rotation transformation from world XY to a frame.

        Parameters
        ----------
        frame
            A frame describing the targeted Cartesian coordinate system.

        Returns
        -------
        Self
            The constructed rotation.

        Notes
        -----
        Creating a rotation from a frame means that we omit all translational
        components. If that is unwanted, use `Transformation.from_frame(frame)`.

        Examples
        --------
        >>> from compas.geometry import Frame
        >>> f1 = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
        >>> T = Transformation.from_frame(f1)
        >>> f2 = Frame.from_transformation(T)
        >>> f1 == f2
        True

        """
        matrix = matrix_from_frame(frame)
        matrix[0][3] = 0.0
        matrix[1][3] = 0.0
        matrix[2][3] = 0.0
        return cls(matrix)

    @classmethod
    def from_quaternion(cls, quaternion: FloatSequenceType) -> Self:
        """Construct a rotation transformation from quaternion coefficients.

        Parameters
        ----------
        quaternion
            Four numbers that represents the four coefficient values of a quaternion.

        Returns
        -------
        Self
            The constructed rotation.

        Examples
        --------
        >>> from compas.tolerance import TOL
        >>> q1 = [0.945, -0.021, -0.125, 0.303]
        >>> R = Rotation.from_quaternion(q1)
        >>> q2 = R.quaternion
        >>> TOL.is_allclose(q1, q2, atol=1e-3)
        True

        """
        matrix = matrix_from_quaternion(quaternion)
        return cls(matrix)

    @classmethod
    def from_axis_angle_vector(cls, axis_angle_vector: CoordinateType, point: CoordinateType = (0.0, 0.0, 0.0)) -> Self:
        """Construct a rotation transformation from an axis-angle vector.

        Parameters
        ----------
        axis_angle_vector
            Three numbers that represent the axis of rotation and angle of rotation through the vector's magnitude.
        point
            A point to perform a rotation around an origin other than [0, 0, 0].

        Returns
        -------
        Self
            The constructed rotation.

        Examples
        --------
        >>> from compas.tolerance import TOL
        >>> aav1 = [-0.043, -0.254, 0.617]
        >>> R = Rotation.from_axis_angle_vector(aav1)
        >>> aav2 = R.axis_angle_vector
        >>> TOL.is_allclose(aav1, aav2, atol=1e-3)
        True

        """
        angle = length_vector(axis_angle_vector)
        return cls.from_axis_and_angle(axis_angle_vector, angle, point)

    # ==========================================================================
    # Methods
    # ==========================================================================

    def euler_angles(self, static: bool = True, axes: str = "xyz") -> list[float]:
        """Return Euler angles for an axis sequence and rotation type.

        Parameters
        ----------
        static
            If True the rotations are applied to a static frame.
            If False, to a rotational.
        axes
            A 3 character string specifying the order of the axes.

        Returns
        -------
        list[float]
            The 3 Euler angles.

        Examples
        --------
        >>> from compas.tolerance import TOL
        >>> ea1 = 1.4, 0.5, 2.3
        >>> args = False, "xyz"
        >>> R1 = Rotation.from_euler_angles(ea1, *args)
        >>> ea2 = R1.euler_angles(*args)
        >>> TOL.is_allclose(ea1, ea2)
        True

        """
        return euler_angles_from_matrix(self.matrix, static, axes)
