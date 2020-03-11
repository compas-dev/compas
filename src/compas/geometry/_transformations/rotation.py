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
from compas.geometry import normalize_vector
from compas.geometry import cross_vectors
from compas.geometry import length_vector

from compas.geometry._transformations import matrix_from_euler_angles
from compas.geometry._transformations import euler_angles_from_matrix
from compas.geometry._transformations import matrix_from_axis_and_angle
from compas.geometry._transformations import axis_and_angle_from_matrix
from compas.geometry._transformations import matrix_from_quaternion
from compas.geometry._transformations import quaternion_from_matrix
from compas.geometry._transformations import basis_vectors_from_matrix
from compas.geometry._transformations import matrix_from_frame
from compas.geometry._transformations import Transformation


__all__ = ['Rotation']


class Rotation(Transformation):
    """``Rotation`` extends ``Transformation`` to represent a 4x4 rotation matrix.

    The class contains methods for converting rotation matrices to axis-angle
    representations, Euler angles, quaternion and basis vectors.

    Examples
    --------
    >>> from compas.geometry import Frame
    >>> f1 = Frame([0, 0, 0], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
    >>> R = Rotation.from_frame(f1)
    >>> args = False, 'xyz'
    >>> alpha, beta, gamma = R.euler_angles(*args)
    >>> xaxis, yaxis, zaxis = [1, 0, 0], [0, 1, 0], [0, 0, 1]
    >>> Rx = Rotation.from_axis_and_angle(xaxis, alpha)
    >>> Ry = Rotation.from_axis_and_angle(yaxis, beta)
    >>> Rz = Rotation.from_axis_and_angle(zaxis, gamma)
    >>> f2 = Frame.worldXY()
    >>> f1 == f2.transformed(Rx * Ry * Rz)
    True

    """

    @classmethod
    def from_basis_vectors(cls, xaxis, yaxis):
        """Creates a ``Rotation`` from basis vectors (= orthonormal vectors).

        Parameters
        ----------
        xaxis : :class:`Vector`
            The x-axis of the frame.
        yaxis : :class:`Vector`
            The y-axis of the frame.

        Examples
        --------
        >>> xaxis = [0.68, 0.68, 0.27]
        >>> yaxis = [-0.67, 0.73, -0.15]
        >>> R = Rotation.from_basis_vectors(xaxis, yaxis)
        """
        xaxis = normalize_vector(list(xaxis))
        yaxis = normalize_vector(list(yaxis))
        zaxis = cross_vectors(xaxis, yaxis)
        yaxis = cross_vectors(zaxis, xaxis)  # correction

        R = cls()
        R.matrix[0][0], R.matrix[1][0], R.matrix[2][0] = xaxis
        R.matrix[0][1], R.matrix[1][1], R.matrix[2][1] = yaxis
        R.matrix[0][2], R.matrix[1][2], R.matrix[2][2] = zaxis
        return R

    @classmethod
    def from_frame(cls, frame):
        """Computes a change of basis transformation from world XY to frame.

        It is the same as from_frame_to_frame(Frame.worldXY(), frame).

        Parameters
        ----------
        frame : :class:`Frame`
            A frame describing the targeted Cartesian coordinate system.

        Examples
        --------
        >>> from compas.geometry import Frame
        >>> f1 = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
        >>> T = Transformation.from_frame(f1)
        >>> f2 = Frame.from_transformation(T)
        >>> f1 == f2
        True
        """
        R = cls()
        R.matrix = matrix_from_frame(frame)
        R.matrix[0][3], R.matrix[1][3], R.matrix[2][3] = [0., 0., 0.]
        return R

    @classmethod
    def from_quaternion(cls, quaternion):
        """Calculates a ``Rotation`` from quaternion coefficients.

        Parameters
        ----------
        quaternion : :class:`Quaternion`
            Four numbers that represents the four coefficient values of a quaternion.

        Examples
        --------
        >>> q1 = [0.945, -0.021, -0.125, 0.303]
        >>> R = Rotation.from_quaternion(q1)
        >>> q2 = R.quaternion
        >>> allclose(q1, q2, tol=1e-3)
        True
        """
        R = matrix_from_quaternion(quaternion)
        return cls(R)

    @classmethod
    def from_axis_angle_vector(cls, axis_angle_vector, point=[0, 0, 0]):
        """Calculates a ``Rotation`` from an axis-angle vector.

        Parameters
        ----------
        axis_angle_vector : list of float
            Three numbers that represent the axis of rotation and angle of rotation through the vector's magnitude.
        point : list of float, optional
            A point to perform a rotation around an origin other than [0, 0, 0].

        Examples
        --------
        >>> aav1 = [-0.043, -0.254, 0.617]
        >>> R = Rotation.from_axis_angle_vector(aav1)
        >>> aav2 = R.axis_angle_vector
        >>> allclose(aav1, aav2)
        True
        """

        axis_angle_vector = list(axis_angle_vector)
        angle = length_vector(axis_angle_vector)
        return cls.from_axis_and_angle(axis_angle_vector, angle, point)

    @classmethod
    def from_axis_and_angle(cls, axis, angle, point=[0, 0, 0]):
        """Calculates a ``Rotation`` from a rotation axis and an angle and an optional point of rotation.

        The rotation is based on the right hand rule, i.e. anti-clockwise if the
        axis of rotation points towards the observer.

        Parameters
        ----------
        axis : list of float
            Three numbers that represent the axis of rotation.
        angle : float
            The rotation angle in radians.
        point : :class:`Point` or list of float
            A point to perform a rotation around an origin other than [0, 0, 0].

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

        Notes
        -----
        The rotation is based on the right hand rule, i.e. anti-clockwise
        if the axis of rotation points towards the observer.

        """
        M = matrix_from_axis_and_angle(axis, angle, point)
        return cls(M)

    @classmethod
    def from_euler_angles(cls, euler_angles, static=True, axes='xyz'):
        """Calculates a ``Rotation`` from Euler angles.

        In 3D space any orientation can be achieved by composing three
        elemental rotations, rotations about the axes (x,y,z) of a coordinate
        system. A triple of Euler angles can be interpreted in 24 ways, which
        depends on if the rotations are applied to a static (extrinsic) or
        rotating (intrinsic) frame and the order of axes.

        Parameters
        ----------
        euler_angles: list of float
            Three numbers that represent the angles of rotations about the
            defined axes.
        static: bool, optional
            If true the rotations are applied to a static frame. If not, to a
            rotational. Defaults to true.
        axes: str, optional
            A 3 character string specifying order of the axes. Defaults to 'xyz'.

        Examples
        --------
        >>> ea1 = 1.4, 0.5, 2.3
        >>> args = False, 'xyz'
        >>> R1 = Rotation.from_euler_angles(ea1, *args)
        >>> ea2 = R1.euler_angles(*args)
        >>> allclose(ea1, ea2)
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
        M = matrix_from_euler_angles(euler_angles, static, axes)
        return Rotation(M)

    @property
    def quaternion(self):
        """Returns the Quaternion from the ``Rotation``.

        Returns
        -------
        :class:`Quaternion`

        Examples
        --------
        >>> q1 = [0.945, -0.021, -0.125, 0.303]
        >>> R = Rotation.from_quaternion(q1)
        >>> q2 = R.quaternion
        >>> allclose(q1, q2, tol=1e-3)
        True
        """
        from compas.geometry import Quaternion
        return Quaternion(*quaternion_from_matrix(self.matrix))

    @property
    def axis_and_angle(self):
        """Returns the axis and the angle of the ``Rotation``.

        Returns
        -------
        tuple: (:class:`Vector`, float)

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
        from compas.geometry import Vector
        axis, angle = axis_and_angle_from_matrix(self.matrix)
        return Vector(*axis), angle

    @property
    def axis_angle_vector(self):
        """Returns the axis-angle vector of the ``Rotation``.

        Returns
        -------
        :class:`Vector`

        Examples
        --------
        >>> aav1 = [-0.043, -0.254, 0.617]
        >>> R = Rotation.from_axis_angle_vector(aav1)
        >>> aav2 = R.axis_angle_vector
        >>> allclose(aav1, aav2)
        True
        """
        axis, angle = self.axis_and_angle
        return axis.scaled(angle)

    def euler_angles(self, static=True, axes='xyz'):
        """Returns Euler angles from the ``Rotation`` according to specified
        axis sequence and rotation type.

        Parameters
        ----------
        static : bool, optional
            If true the rotations are applied to a static frame. If not, to a
            rotational. Defaults to True.
        axes : str, optional
            A 3 character string specifying the order of the axes. Defaults to
            'xyz'.

        Returns
        -------
        list of float: The 3 Euler angles.

        Examples
        --------
        >>> ea1 = 1.4, 0.5, 2.3
        >>> args = False, 'xyz'
        >>> R1 = Rotation.from_euler_angles(ea1, *args)
        >>> ea2 = R1.euler_angles(*args)
        >>> allclose(ea1, ea2)
        True
        """
        return euler_angles_from_matrix(self.matrix, static, axes)

    @property
    def basis_vectors(self):
        """Returns the basis vectors of the ``Rotation``.

        Returns
        -------
        tuple: (:class:`Vector`, :class:`Vector`)

        """
        from compas.geometry import Vector
        xaxis, yaxis = basis_vectors_from_matrix(self.matrix)
        return Vector(*xaxis), Vector(*yaxis)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import doctest

    from compas.geometry import Frame  # noqa: F401
    from compas.geometry import allclose  # noqa: F401

    doctest.testmod(globs=globals())
