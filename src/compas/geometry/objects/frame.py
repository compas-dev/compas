from __future__ import print_function

import math

from compas.geometry.basic import cross_vectors
from compas.geometry.basic import normalize_vector
from compas.geometry.basic import subtract_vectors
from compas.geometry.basic import allclose

from compas.geometry.objects.xform import Transformation
from compas.geometry.objects.xform import Rotation

from compas.geometry.transformations import matrix_from_basis_vectors
from compas.geometry.transformations import basis_vectors_from_matrix
from compas.geometry.transformations import quaternion_from_matrix
from compas.geometry.transformations import matrix_from_quaternion
from compas.geometry.transformations import axis_angle_vector_from_matrix
from compas.geometry.transformations import matrix_from_axis_angle_vector
from compas.geometry.transformations import euler_angles_from_matrix
from compas.geometry.transformations import matrix_from_euler_angles
from compas.geometry.transformations import decompose_matrix


__author__  = ['Romana Rust <rust@arch.ethz.ch>', ]
__license__ = 'MIT License'
__email__   = 'rust@arch.ethz.ch'


class Frame(object):
    """The ``Frame`` consists of a point and and two orthonormal base vectors.

    It represents a plane in three dimensions with a defined origin and
    orientation.

    Attributes:
        point (:obj:`list` of :obj:`float`, optional): The origin of the frame.
            Defaults to [0, 0, 0].
        xaxis (:obj:`list` of :obj:`float`, optional): The x-axis of the frame.
            Defaults to [1, 0, 0].
        yaxis (:obj:`list` of :obj:`float`, optional): The y-axis of the frame.
            Defaults to [0, 1, 0].

    Examples:
        >>> f = Frame([0, 0, 0], [1, 0, 0], [0, 1, 0])
        >>> f = Frame.from_points([1, 1, 1], [2, 4, 5], [4, 2, 3])
        >>> f = Frame.from_euler_angles([0.5, 1., 0.2])
        >>> f = Frame.worldXY()
    """

    def __init__(self, point=[0, 0, 0], xaxis=[1, 0, 0], yaxis=[0, 1, 0]):
        self.point = [float(f) for f in list(point)]
        self.xaxis = list(normalize_vector(list(xaxis)))
        self.yaxis = list(normalize_vector(list(yaxis)))
        zaxis      = list(normalize_vector(cross_vectors(self.xaxis, self.yaxis)))
        self.yaxis = list(cross_vectors(zaxis, self.xaxis))

    def copy(self):
        """Returns a copy of the frame.
        """
        cls = type(self)
        return cls(self.point[:], self.xaxis[:], self.yaxis[:])

    @classmethod
    def worldXY(cls):
        """Returns the world XY frame.
        """
        return cls([0, 0, 0], [1, 0, 0], [0, 1, 0])

    @classmethod
    def worldZX(cls):
        """Returns the world ZX frame.
        """
        return cls([0, 0, 0], [0, 0, 1], [1, 0, 0])

    @classmethod
    def worldYZ(cls):
        """Returns the world YZ frame.
        """
        return cls([0, 0, 0], [0, 1, 0], [0, 0, 1])

    @classmethod
    def from_points(cls, point, point_xaxis, point_xyplane):
        """Calculates a frame from 3 points.

        Args:
            point (:obj:`list` of :obj:`float`): The origin of the frame.
            point_xaxis (:obj:`list` of :obj:`float`): A point on the x-axis of
                the frame.
            point_xyplane (:obj:`list` of :obj:`float`): A point within the
                xy-plane of the frame.

        Example:
            >>> f = Frame.from_points([1, 1, 1], [2, 4, 5], [4, 2, 3])
        """
        xaxis = subtract_vectors(point_xaxis, point)
        xyvec = subtract_vectors(point_xyplane, point)
        yaxis = list(cross_vectors(cross_vectors(xaxis, xyvec), xaxis))
        return cls(point, xaxis, yaxis)

    @classmethod
    def from_rotation(cls, rotation, point=[0, 0, 0]):
        """Calculates a frame from a ``Rotation``.

        Args:
            rotation (:class:`Rotation`): The rotation defines the orientation
                of the frame.
            point (:obj:`list` of :obj:`float`, optional): The point of the
                frame. Defaults to [0, 0, 0].

        Example:
            >>> f1 = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
            >>> R = Rotation.from_frame(f1)
            >>> f2 = Frame.from_rotation(R, point = f1.point)
            >>> f1 == f2
            True
        """
        xaxis, yaxis = rotation.basis_vectors
        return cls(point, xaxis, yaxis)

    @classmethod
    def from_transformation(cls, transformation):
        """Calculates a frame from a ``Transformation``.

        Args:
            transformation (:class:`Transformation`): The transformation
                defines the orientation of the frame through the rotation and
                the point through the translation.

        Example:
            >>> f1 = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
            >>> T = Transformation.from_frame(f1)
            >>> f2 = Frame.from_transformation(T)
            >>> f1 == f2
            True
        """
        xaxis, yaxis = transformation.basis_vectors
        point = transformation.translation
        return cls(point, xaxis, yaxis)

    @classmethod
    def from_matrix(cls, matrix):
        """Calculates a frame from a matrix.

        Args:
            matrix (:obj:`list` of :obj:`list` of :obj:`float`): The 4x4
                transformation matrix in row-major order.

        Example:
            >>> ea1 = [0.5, 0.4, 0.8]
            >>> M = matrix_from_euler_angles(ea1)
            >>> f = Frame.from_matrix(M)
            >>> ea2 = f.euler_angles()
            >>> allclose(ea1, ea2)
            True
        """
        sc, sh, a, point, p = decompose_matrix(matrix)
        R = matrix_from_euler_angles(a, static=True, axes='xyz')
        xaxis, yaxis = basis_vectors_from_matrix(R)
        return cls(point, xaxis, yaxis)

    @classmethod
    def from_list(cls, values):
        """Construct a frame from a list of 12 or 16 :obj:`float` values.

        Args:
            values (:obj:`list` of :obj:`float`): The list of 12 or 16 values 
                representing a 4x4 matrix.
        
        Note:
            Since the transformation matrix follows the row-major order, the
            translational components must be at the list's indices 3, 7, 11.
        
        Raises:
            ValueError: If the length of the list is neither 12 nor 16.
        
        Example:
            >>> f = Frame.from_list([-1.0, 0.0, 0.0, 8110, 
                                    0.0, 0.0, -1.0, 7020,
                                    0.0, -1.0, 0.0, 1810])
        """

        if len(values) == 12:
            values.extend([0., 0., 0., 1.])
        if len(values) != 16:
            raise ValueError('Expected 12 or 16 floats but got %d' % len(values))

        matrix = [[0. for i in range(4)] for j in range(4)]
        for i in range(4):
            for j in range(4):
                matrix[i][j] = float(values[i * 4 + j])

        return cls.from_matrix(matrix)

    @classmethod
    def from_quaternion(cls, quaternion, point=[0, 0, 0]):
        """Calculates a frame from a rotation represented by quaternion \
            coefficients.

        Args:
            quaternion (:obj:`list` of :obj:`float`): Four numbers that
                represent the four coefficient values of a quaternion.
            point (:obj:`list` of :obj:`float`, optional): The point of the
                frame. Defaults to [0, 0, 0].

        Example:
            >>> q1 = [0.945, -0.021, -0.125, 0.303]
            >>> f = Frame.from_quaternion(q1, point = [1., 1., 1.])
            >>> q2 = f.quaternion
            >>> allclose(q1, q2, tol=1e-03)
            True
        """
        R = matrix_from_quaternion(quaternion)
        xaxis, yaxis = basis_vectors_from_matrix(R)
        return cls(point, xaxis, yaxis)

    @classmethod
    def from_axis_angle_vector(cls, axis_angle_vector, point=[0, 0, 0]):
        """Calculates a frame from an axis-angle vector representing the \
            rotation.

        Args:
            axis_angle_vector (:obj:`list` of :obj:`float`): Three numbers that
                represent the axis of rotation and angle of rotation by its
                magnitude.
            point (:obj:`list` of :obj:`float`, optional): The point of the
                frame. Defaults to [0, 0, 0].

        Example:
            >>> aav1 = [-0.043, -0.254, 0.617]
            >>> f = Frame.from_axis_angle_vector(aav1, point = [0, 0, 0])
            >>> aav2 = f.axis_angle_vector
            >>> allclose(aav1, aav2)
            True
        """
        R = matrix_from_axis_angle_vector(axis_angle_vector)
        xaxis, yaxis = basis_vectors_from_matrix(R)
        return cls(point, xaxis, yaxis)

    @classmethod
    def from_euler_angles(cls, euler_angles, static=True,
                          axes='xyz', point=[0, 0, 0]):
        """Calculates a frame from a rotation represented by Euler angles.

        Args:
            euler_angles(:obj:`list` of :obj:`float`): Three numbers that
                represent the angles of rotations about the defined axes.
            static(:obj:`bool`, optional): If true the rotations are applied to
                a static frame. If not, to a rotational. Defaults to true.
            axes(:obj:`str`, optional): A 3 character string specifying the
                order of the axes. Defaults to 'xyz'.
            point (:obj:`list` of :obj:`float`, optional): The point of the
                frame. Defaults to [0, 0, 0].

        Example:
            >>> ea1 = 1.4, 0.5, 2.3
            >>> f = Frame.from_euler_angles(ea1, static = True, axes = 'xyz')
            >>> ea2 = f.euler_angles(static = True, axes = 'xyz')
            >>> allclose(ea1, ea2)
            True
        """
        R = matrix_from_euler_angles(euler_angles, static, axes)
        xaxis, yaxis = basis_vectors_from_matrix(R)
        return cls(point, xaxis, yaxis)

    @property
    def normal(self):
        """Returns the frame's normal (z-axis).
        """
        return cross_vectors(self.xaxis, self.yaxis)

    @property
    def zaxis(self):
        """Returns the frame's z-axis (normal).
        """
        return self.normal

    @property
    def quaternion(self):
        """Returns the 4 quaternion coefficients from the rotation given by the
            frame.
        """
        rotation = matrix_from_basis_vectors(self.xaxis, self.yaxis)
        return quaternion_from_matrix(rotation)

    @property
    def axis_angle_vector(self):
        """Returns the axis-angle vector from the rotation given by the frame.
        """
        R = matrix_from_basis_vectors(self.xaxis, self.yaxis)
        return axis_angle_vector_from_matrix(R)

    def euler_angles(self, static=True, axes='xyz'):
        """Returns the Euler angles from the rotation given by the frame.

        Args:
            static(:obj:`bool`, optional): If true the rotations are applied
                to a static frame. If not, to a rotational. Defaults to True.

            axes(:obj:`str`, optional): A 3 character string specifying the
                order of the axes. Defaults to 'xyz'.

        Returns:
            (:obj:`list` of :obj:`float`): Three numbers that represent the
                angles of rotations about the defined axes.

        Example:
            >>> ea1 = 1.4, 0.5, 2.3
            >>> f = Frame.from_euler_angles(ea1, static = True, axes = 'xyz')
            >>> ea2 = f.euler_angles(static = True, axes = 'xyz')
            >>> allclose(ea1, ea2)
            True
        """
        R = matrix_from_basis_vectors(self.xaxis, self.yaxis)
        return euler_angles_from_matrix(R, static, axes)

    def transform(self, transformation, copy=False):
        """Transforms the frame with the ``Transformation``.

        Args:
            transformation (:class:`Transformation`): The transformation used
                to transform the Frame.
            copy (:obj:`bool`, optional): If true, a copy of the frame will be
                made. Defaults to false.

        Returns:
            (:class:`Frame`): The transformed frame.

        Example:
            >>> f1 = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
            >>> T = Transformation.from_frame(f1)
            >>> f2 = Frame.worldXY()
            >>> f1 == f2.transform(T)
            True
        """

        T = transformation * Transformation.from_frame(self)
        point = T.translation
        xaxis, yaxis = T.basis_vectors

        if copy:
            return Frame(point, xaxis, yaxis)
        else:
            self.point = point
            self.xaxis = xaxis
            self.yaxis = yaxis
            return self
    
    @classmethod
    def from_data(cls, data):
        """Construct a frame from its data representation.

        Args:
            data (`dict`): The data dictionary.

        Returns:
            (:class:`Frame`)
        """
        frame = cls()
        frame.data = data
        return frame
    
    def to_data(self):
        return self.data
    
    @property
    def data(self):
        """Returns the data dictionary that represents the frame."""
        return {'point': self.point, 'xaxis': self.xaxis, 'yaxis': self.yaxis}
        
    @data.setter
    def data(self, data):
        self.point = data.get('point', [0, 0, 0])
        self.xaxis = data.get('xaxis', [1, 0, 0])
        self.yaxis = data.get('yaxis', [0, 1, 0])

    def __repr__(self):
        s = "[[%.4f, %.4f, %.4f], " % tuple(self.point)
        s += "[%.4f, %.4f, %.4f], " % tuple(self.xaxis)
        s += "[%.4f, %.4f, %.4f]]" % tuple(self.yaxis)
        return s

    def __iter__(self):
        return iter([self.point, self.xaxis, self.yaxis])

    def __eq__(self, other, tol=1e-05):
        for v1, v2 in zip(self, other):
            for a, b in zip(v1, v2):
                if math.fabs(a - b) > tol:
                    return False
        return True


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    f1 = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
    R = Rotation.from_frame(f1)
    f2 = Frame.from_rotation(R, point=f1.point)
    print(f1 == f2)

    f1 = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
    T = Transformation.from_frame(f1)
    f2 = Frame.from_transformation(T)
    print(f1 == f2)

    ea1 = [0.5, 0.4, 0.8]
    M = matrix_from_euler_angles(ea1)
    f = Frame.from_matrix(M)
    ea2 = f.euler_angles()
    print(allclose(ea1, ea2))

    q1 = [0.945, -0.021, -0.125, 0.303]
    f = Frame.from_quaternion(q1, point=[1., 1., 1.])
    q2 = f.quaternion
    print(allclose(q1, q2, tol=1e-03))

    aav1 = [-0.043, -0.254, 0.617]
    f = Frame.from_axis_angle_vector(aav1, point=[0, 0, 0])
    aav2 = f.axis_angle_vector
    print(allclose(aav1, aav2))

    ea1 = 1.4, 0.5, 2.3
    f = Frame.from_euler_angles(ea1, static=True, axes='xyz')
    ea2 = f.euler_angles(static=True, axes='xyz')
    print(allclose(ea1, ea2))

    f1 = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
    T = Transformation.from_frame(f1)
    f2 = Frame.worldXY()
    f2.transform(T)
    print(f1 == f2)
