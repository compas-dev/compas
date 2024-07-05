"""
This library for transformations partly derived and was re-implemented from the
following online resources:

    * http://www.lfd.uci.edu/~gohlke/code/transformations.py.html
    * http://www.euclideanspace.com/maths/geometry/rotations/
    * http://code.activestate.com/recipes/578108-determinant-of-matrix-of-any-order/
    * http://blog.acipo.com/matrix-inversion-in-javascript/

Many thanks to Christoph Gohlke, Martin John Baker, Sachin Joglekar and Andrew
Ippoliti for providing code and documentation.
"""

from compas.geometry import Transformation
from compas.geometry import axis_and_angle_from_matrix
from compas.geometry import basis_vectors_from_matrix
from compas.geometry import cross_vectors
from compas.geometry import decompose_matrix
from compas.geometry import euler_angles_from_matrix
from compas.geometry import length_vector
from compas.geometry import matrix_from_axis_and_angle
from compas.geometry import matrix_from_euler_angles
from compas.geometry import matrix_from_frame
from compas.geometry import matrix_from_quaternion
from compas.geometry import normalize_vector
from compas.itertools import flatten
from compas.tolerance import TOL


class Rotation(Transformation):
    """Class representing a rotation transformation.

    The class contains methods for converting rotation matrices to axis-angle
    representations, Euler angles, quaternion and basis vectors.

    Parameters
    ----------
    matrix : list[list[float]], optional
        A 4x4 matrix (or similar) representing a rotation.
    check : bool, optional
        If ``True``, the provided matrix will be checked for validity.
    name : str, optional
        The name of the transformation.

    Attributes
    ----------
    quaternion : :class:`compas.geometry.Quaternion`, read-only
        The quaternion from the rotation.
    axis_and_angle : tuple[:class:`compas.geometry.Vector`, float], read-only
        The axis and the angle of the rotation.
    axis_angle_vector : :class:`compas.geometry.Vector`, read-only
        The axis-angle vector of the rotation.
    basis_vectors : tuple[:class:`compas.geometry.Vector`, :class:`compas.geometry.Vector`], read-only
        The basis vectors of the rotation.

    Raises
    ------
    ValueError
        If ``check`` is ``True`` and the provided transformation matrix is not a rotation.

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

    def __init__(self, matrix=None, check=False, name=None):
        if matrix and check:
            _, _, angles, _, _ = decompose_matrix(matrix)
            if not TOL.is_allclose(flatten(matrix), flatten(matrix_from_euler_angles(angles))):
                raise ValueError("This is not a proper rotation matrix.")
        super(Rotation, self).__init__(matrix=matrix, name=name)

    @property
    def quaternion(self):
        from compas.geometry import Quaternion

        return Quaternion.from_matrix(self.matrix)

    @property
    def axis_and_angle(self):
        from compas.geometry import Vector

        axis, angle = axis_and_angle_from_matrix(self.matrix)
        return Vector(*axis), angle

    @property
    def axis_angle_vector(self):
        axis, angle = self.axis_and_angle
        return axis.scaled(angle)

    @property
    def basis_vectors(self):
        from compas.geometry import Vector

        xaxis, yaxis = basis_vectors_from_matrix(self.matrix)
        return Vector(*xaxis), Vector(*yaxis)

    @classmethod
    def from_axis_and_angle(cls, axis, angle, point=[0, 0, 0]):
        """Construct a rotation transformation from a rotation axis and an angle and an optional point of rotation.

        The rotation is based on the right hand rule, i.e. anti-clockwise if the
        axis of rotation points towards the observer.

        Parameters
        ----------
        axis : [float, float, float] | :class:`compas.geometry.Vector`
            Three numbers that represent the axis of rotation.
        angle : float
            The rotation angle in radians.
        point : [float, float, float] | :class:`compas.geometry.Point`
            A point to perform a rotation around an origin other than [0, 0, 0].

        Returns
        -------
        :class:`compas.geometry.Rotation`

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
        >>> allclose(axis1, axis2)
        True
        >>> allclose([angle1], [angle2])
        True

        """
        matrix = matrix_from_axis_and_angle(axis, angle, point=point)
        return cls(matrix)

    @classmethod
    def from_basis_vectors(cls, xaxis, yaxis):
        """Construct a rotation transformation from basis vectors (= orthonormal vectors).

        Parameters
        ----------
        xaxis : [float, float, float] | :class:`compas.geometry.Vector`
            The x-axis of the frame.
        yaxis : [float, float, float] | :class:`compas.geometry.Vector`
            The y-axis of the frame.

        Returns
        -------
        :class:`compas.geometry.Rotation`

        Examples
        --------
        >>> xaxis = [0.68, 0.68, 0.27]
        >>> yaxis = [-0.67, 0.73, -0.15]
        >>> R = Rotation.from_basis_vectors(xaxis, yaxis)

        """
        xaxis = normalize_vector(list(xaxis))
        yaxis = normalize_vector(list(yaxis))
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
    def from_frame(cls, frame):
        """Construct a rotation transformationn from world XY to frame.

        Parameters
        ----------
        frame : [point, vector, vector] | :class:`compas.geometry.Frame`
            A frame describing the targeted Cartesian coordinate system.

        Returns
        -------
        :class:`compas.geometry.Rotation`

        Notes
        -----
        Creating a rotation from a frame means that we omit all translational
        components. If that is unwanted, use ``Transformation.from_frame(frame)``.

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
    def from_quaternion(cls, quaternion):
        """Construct a rotation transformation` from quaternion coefficients.

        Parameters
        ----------
        quaternion : [float, float, float, float] | :class:`compas.geometry.Quaternion`
            Four numbers that represents the four coefficient values of a quaternion.

        Returns
        -------
        :class:`compas.geometry.Rotation`

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
    def from_axis_angle_vector(cls, axis_angle_vector, point=[0, 0, 0]):
        """Construct a rotation transformation from an axis-angle vector.

        Parameters
        ----------
        axis_angle_vector : [float, float, float] | :class:`compas.geometry.Vector`
            Three numbers that represent the axis of rotation and angle of rotation through the vector's magnitude.
        point : [float, float, float] | :class:`compas.geometry.Point`, optional
            A point to perform a rotation around an origin other than [0, 0, 0].

        Returns
        -------
        :class:`compas.geometry.Rotation`

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

    # why is this repeated here?
    @classmethod
    def from_euler_angles(cls, euler_angles, static=True, axes="xyz", **kwargs):
        """Construct a rotation transformation from Euler angles.

        In 3D space any orientation can be achieved by composing three
        elemental rotations, rotations about the axes (x,y,z) of a coordinate
        system. A triple of Euler angles can be interpreted in 24 ways, which
        depends on if the rotations are applied to a static (extrinsic) or
        rotating (intrinsic) frame and the order of axes.

        Parameters
        ----------
        euler_angles: [float, float, float]
            Three numbers that represent the angles of rotations about the
            defined axes.
        static: bool, optional
            If True the rotations are applied to a static frame.
            If False, to a rotational.
        axes: str, optional
            A 3 character string specifying order of the axes.

        Returns
        -------
        :class:`compas.geometry.Rotation`

        Examples
        --------
        >>> from compas.tolerance import TOL
        >>> ea1 = 1.4, 0.5, 2.3
        >>> args = False, "xyz"
        >>> R1 = Rotation.from_euler_angles(ea1, *args)
        >>> ea2 = R1.euler_angles(*args)
        >>> TOL.is_allclose(ea1, ea2)
        True

        >>> alpha, beta, gamma = ea1
        >>> xaxis, yaxis, zaxis = [1, 0, 0], [0, 1, 0], [0, 0, 1]
        >>> Rx = Rotation.from_axis_and_angle(xaxis, alpha)
        >>> Ry = Rotation.from_axis_and_angle(yaxis, beta)
        >>> Rz = Rotation.from_axis_and_angle(zaxis, gamma)
        >>> R2 = Rx * Ry * Rz
        >>> R1 == R2
        True

        """
        return super(Rotation, cls).from_euler_angles(euler_angles, static, axes)

    # split up into two properties
    # euler_angles
    # rotating_euler_angles
    # xyz seems irelevant
    # could be added to base Transformation
    # always relevant
    def euler_angles(self, static=True, axes="xyz"):
        """Returns Euler angles from the rotation according to specified
        axis sequence and rotation type.

        Parameters
        ----------
        static : bool, optional
            If True the rotations are applied to a static frame.
            If False, to a rotational.
        axes : str, optional
            A 3 character string specifying the order of the axes.

        Returns
        -------
        [float, float, float]
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
