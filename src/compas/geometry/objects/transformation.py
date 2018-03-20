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
import math
from copy import deepcopy

from compas.geometry.basic import multiply_matrix_vector
from compas.geometry.basic import multiply_matrices
from compas.geometry.basic import dot_vectors
from compas.geometry.basic import normalize_vector
from compas.geometry.basic import cross_vectors
from compas.geometry.basic import length_vector
from compas.geometry.basic import subtract_vectors
from compas.geometry.basic import scale_vector
from compas.geometry.basic import norm_vector
from compas.geometry.basic import transpose_matrix

from compas.geometry.transformations import homogenize

from compas.geometry.transformations import determinant
from compas.geometry.transformations import inverse
from compas.geometry.transformations import identity_matrix
from compas.geometry.transformations import matrix_from_frame
from compas.geometry.transformations import matrix_from_euler_angles
from compas.geometry.transformations import euler_angles_from_matrix
from compas.geometry.transformations import matrix_from_axis_and_angle
from compas.geometry.transformations import matrix_from_axis_angle_vector
from compas.geometry.transformations import axis_and_angle_from_matrix
from compas.geometry.transformations import axis_angle_vector_from_matrix
from compas.geometry.transformations import matrix_from_quaternion
from compas.geometry.transformations import quaternion_from_matrix
from compas.geometry.transformations import matrix_from_basis_vectors
from compas.geometry.transformations import basis_vectors_from_matrix
from compas.geometry.transformations import matrix_from_translation
from compas.geometry.transformations import translation_from_matrix
from compas.geometry.transformations import matrix_from_orthogonal_projection
from compas.geometry.transformations import matrix_from_parallel_projection
from compas.geometry.transformations import matrix_from_perspective_projection
from compas.geometry.transformations import matrix_from_perspective_entries
from compas.geometry.transformations import matrix_from_shear_entries
from compas.geometry.transformations import matrix_from_shear
from compas.geometry.transformations import matrix_from_scale_factors
from compas.geometry.transformations import compose_matrix
from compas.geometry.transformations import decompose_matrix
from compas.geometry.transformations import transform

from compas.geometry.transformations import allclose

__author__ = ['Romana Rust <rust@arch.ethz.ch>', ]
__license__ = 'MIT License'
__email__ = 'rust@arch.ethz.ch'

__all__ = [
    'Transformation',
    'Rotation',
    'Translation',
    'Scale',
    'Reflection',
    'Projection',
    'Shear'
]

class Transformation(object):
    """The ``Transformation`` represents a 4x4 transformation matrix.

    It is the base class for transformations like :class:`Rotation`,
    :class:`Translation`, :class:`Scale`, :class:`Reflection`,
    :class:`Projection` and :class:`Shear`.


    The class allows to concatenate Transformations by multiplication, to
    calculate the inverse transformation and to decompose a transformation into
    its components of rotation, translation, scale, shear, and perspective.
    The matrix follows the row-major order, such that translation components
    x, y, z are in the right column of the matrix, i.e. ``M[0][3], M[1][3],
    M[2][3] = x, y, z``.

    Attributes:
        matrix (:obj:`list` of :obj:`list` of :obj:`float`): Square matrix.

    Examples:
        >>> from compas.geometry import Frame
        >>> T = Transformation()
        >>> f1 = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
        >>> T = Transformation.from_frame(f1)
        >>> Sc, Sh, R, Tl, P = T.decompose()
        >>> Tinv = T.inverse()
    """

    def __init__(self, matrix=None):
        if not matrix:
            matrix = identity_matrix(4)

        self.matrix = matrix

    @classmethod
    def from_matrix(cls, matrix):
        """Creates a ``Transformation`` from a 4x4 two-dimensional list of \
            numbers.

        Args:
            matrix (:obj:`list` of :obj:`list` of `float`)
        """
        T = cls()
        for i in range(4):
            for j in range(4):
                T.matrix[i][j] = float(matrix[i][j])
        return T

    @classmethod
    def from_list(cls, numbers):
        """Creates a ``Transformation`` from a list of 16 numbers.

        Note:
            Since the transformation matrix follows the row-major order, the
            translational components must be at the list's indices 3, 7, 11.

        Args:
            numbers (:obj:`list` of :obj:`float`)

        Example:
            >>> numbers = [1, 0, 0, 3, 0, 1, 0, 4, 0, 0, 1, 5, 0, 0, 0, 1]
            >>> T = Transformation.from_list(numbers)
        """
        T = cls()
        for i in range(4):
            for j in range(4):
                T.matrix[i][j] = float(numbers[i * 4 + j])
        return T

    @classmethod
    def from_frame(cls, frame):
        """Computes a change of basis transformation from world XY to frame.

        It is the same as from_frame_to_frame(Frame.worldXY(), frame).

        Args:
            frame (:class:`Frame`): a frame describing the targeted Cartesian
                coordinate system

        Example:
            >>> from compas.geometry import Frame
            >>> f1 = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
            >>> T = Transformation.from_frame(f1)
            >>> f2 = Frame.from_transformation(T)
            >>> f1 == f2
            True
        """
        T = cls()
        T.matrix = matrix_from_frame(frame)
        return T

    @classmethod
    def from_frame_to_frame(cls, frame_from, frame_to):
        """Computes a change of basis transformation between two frames.

        This transformation maps geometry from one Cartesian coordinate system
        defined by "frame_from" to the other Cartesian coordinate system
        defined by "frame_to".

        Args:
            frame_from (:class:`Frame`): a frame defining the original
                Cartesian coordinate system
            frame_to (:class:`Frame`): a frame defining the targeted
                Cartesian coordinate system

        Example:
            >>> from compas.geometry import Frame
            >>> f1 = Frame([2, 2, 2], [0.12, 0.58, 0.81], [-0.80, 0.53, -0.26])
            >>> f2 = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
            >>> T = Transformation.from_frame_to_frame(f1, f2)
            >>> f1 == f1.transform(T)
            True
        """
        T1 = matrix_from_frame(frame_from)
        T2 = matrix_from_frame(frame_to)

        return cls(multiply_matrices(T2, inverse(T1)))

    def inverse(self):
        """Returns the inverse transformation.

        Example:
            >>> from compas.geometry import Frame
            >>> f = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
            >>> T = Transformation.from_frame(f)
            >>> I = Transformation() # identity matrix
            >>> I == T * T.inverse()
            True
        """
        cls = type(self)
        return cls(inverse(self.matrix))

    def decompose(self):
        """Decomposes the ``Transformation`` into ``Scale``, ``Shear``, \
            ``Rotation``, ``Translation`` and ``Perspective``.

        Example:
            >>> trans1 = [1, 2, 3]
            >>> angle1 = [-2.142, 1.141, -0.142]
            >>> scale1 = [0.123, 2, 0.5]
            >>> T1 = Translation(trans1)
            >>> R1 = Rotation.from_euler_angles(angle1)
            >>> S1 = Scale(scale1)
            >>> M = (T1 * R1) * S1
            >>> Sc, Sh, R, T, P = M.decompose()
            >>> S1 == Sc
            True
            >>> R1 == R
            True
            >>> T1 == T
            True
        """
        sc, sh, a, t, p = decompose_matrix(self.matrix)

        Sc = Scale(sc)
        Sh = Shear.from_entries(sh)
        R = Rotation.from_euler_angles(a, static=True, axes='xyz')
        T = Translation(t)
        P = Projection.from_entries(p)
        return Sc, Sh, R, T, P

    @property
    def rotation(self):
        """Returns the ``Rotation`` component from the ``Transformation``.
        """
        Sc, Sh, R, T, P = self.decompose()
        return R

    @property
    def translation(self):
        """Returns the 3 values of translation from the ``Transformation``.
        """
        return translation_from_matrix(self.matrix)

    @property
    def basis_vectors(self):
        """Returns the basis vectors from the ``Rotation`` component of the
            ``Transformation``.
        """
        sc, sh, a, t, p = decompose_matrix(self.matrix)
        R = matrix_from_euler_angles(a, static=True, axes='xyz')
        return basis_vectors_from_matrix(R)

    def transform_point(self, point):
        """Transforms a point.

        Args:
            point (:obj:`list` of :obj:`float`)

        Example:
            >>> from compas.geometry import Frame
            >>> f = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
            >>> T = Transformation.from_frame(f)
            >>> q = T.transform_point([0,0,0])
            >>> allclose(f.point, q)
            True

        Returns:
            (:obj:`list` of :obj:`float`): The transformed point.
        """

        ph = list(point) + [1.]  # make homogeneous coordinates
        pht = multiply_matrix_vector(self.matrix, ph)
        return pht[:3]

    def transform_points(self, points):
        """Transforms a list of points.

        Args:
            points (:obj:`list` of :obj:`list` of :obj:`float`): A list of
                points.

        Example:
            >>> from compas.geometry import Frame
            >>> f1 = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
            >>> T = Transformation.from_frame(f1)
            >>> pts = [[1.0, 1.0, 1.0], [1.68, 1.68, 1.27], [0.33, 1.73, 0.85]]
            >>> pts_ = T.transform_points(pts)

        Returns:
            (:obj:`list` of :obj:`list` of :obj:`float`): The transformed \
                points.
        """
        return transform(points, self.matrix)

    @property
    def list(self):
        """Flattens the ``Transformation`` into a list of numbers.
        """
        return [a for c in self.matrix for a in c]

    def concatenate(self, other):
        """Concatenate two transformations into one ``Transformation``.

        Note:
            Rz * Ry * Rx means that Rx is first transformation, Ry second, and
            Rz third.
        """
        cls = type(self)
        if not isinstance(other, cls):
            return Transformation(multiply_matrices(self.matrix, other.matrix))
        else:
            return cls(multiply_matrices(self.matrix, other.matrix))

    def __mul__(self, other):
        return self.concatenate(other)

    def __imul__(self, other):
        return self.concatenate(other)

    def __getitem__(self, key):
        i, j = key
        return self.matrix[i][j]

    def __setitem__(self, key, value):
        i, j = key
        self.matrix[i][j] = value

    def __iter__(self):
        return iter(self.matrix)

    def __eq__(self, other, tol=1e-05):
        try:
            M = self.matrix
            O = other.matrix
            for i in range(4):
                for j in range(4):
                    if math.fabs(M[i][j] - O[i][j]) > tol:
                        return False
            return True
        except BaseException:
            raise TypeError("Wrong input type.")

    def __repr__(self):
        s = "[[%s],\n" % ",".join([("%.4f" % n).rjust(10)
                                   for n in self.matrix[0]])
        s += " [%s],\n" % ",".join([("%.4f" % n).rjust(10)
                                    for n in self.matrix[1]])
        s += " [%s],\n" % ",".join([("%.4f" % n).rjust(10)
                                    for n in self.matrix[2]])
        s += " [%s]]" % ",".join([("%.4f" % n).rjust(10)
                                  for n in self.matrix[3]])
        s += "\n"
        return s


class Rotation(Transformation):
    """The ``Rotation`` represents a 4x4 rotation matrix and is based on \
        ``Transformation``.

    The class contains methods for converting rotation matrices to axis-angle
    representations, Euler angles, quaternion and basis vectors.

    Example:
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
        >>> f1 == f2.transform(Rx * Ry * Rz)
        True

    """

    @classmethod
    def from_basis_vectors(cls, xaxis, yaxis):
        """Creates a ``Rotation`` from basis vectors (= orthonormal vectors).

        Args:
            xaxis (:obj:`list` oof :obj:`float`): The x-axis of the frame.
            yaxis (:obj:`list` oof :obj:`float`): The y-axis of the frame.

        Example:
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
    def from_quaternion(cls, quaternion):
        """Calculates a ``Rotation`` from quaternion coefficients.

        Args:
            quaternion (:obj:`list` of :obj:`float`): Four numbers that
                represents the four coefficient values of a quaternion.

        Example:
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

        Args:
            axis_angle_vector (:obj:`list` of :obj:`float`): Three numbers
                that represent the axis of rotation and angle of rotation
                through the vector's magnitude.
            point (:obj:`list` of :obj:`float`, optional): A point to
                perform a rotation around an origin other than [0, 0, 0].

        Example:
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
        """Calculates a ``Rotation`` from a rotation axis and an angle and \
            an optional point of rotation.

        Note:
            The rotation is based on the right hand rule, i.e. anti-clockwise
            if the axis of rotation points towards the observer.

        Args:
            axis (:obj:`list` of :obj:`float`): Three numbers that represent
                the axis of rotation
            angle (:obj:`float`): The rotation angle in radians.
            point (:obj:`list` of :obj:`float`, optional): A point to
                perform a rotation around an origin other than [0, 0, 0].

        Example:
            >>> axis1 = normalize_vector([-0.043, -0.254, 0.617])
            >>> angle1 = 0.1
            >>> R = Rotation.from_axis_and_angle(axis1, angle1)
            >>> axis2, angle2 = R.axis_and_angle
            >>> allclose(axis1, axis2)
            True
            >>> allclose([angle1], [angle2])
            True
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

        Args:
            euler_angles(:obj:`list` of :obj:`float`): Three numbers that
                represent the angles of rotations about the defined axes.
            static(:obj:`bool`, optional): If true the rotations are applied to
                a static frame. If not, to a rotational. Defaults to true.
            axes(:obj:`str`, optional): A 3 character string specifying order
                of the axes. Defaults to 'xyz'.

        Example:
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
        """Returns the 4 quaternion coefficients from the ``Rotation``.

        Example:
            >>> q1 = [0.945, -0.021, -0.125, 0.303]
            >>> R = Rotation.from_quaternion(q1)
            >>> q2 = R.quaternion
            >>> allclose(q1, q2, tol=1e-3)
            True
        """
        return quaternion_from_matrix(self.matrix)

    @property
    def axis_and_angle(self):
        """Returns the axis and the angle of the ``Rotation``.

        Example:
            >>> axis1 = normalize_vector([-0.043, -0.254, 0.617])
            >>> angle1 = 0.1
            >>> R = Rotation.from_axis_and_angle(axis1, angle1)
            >>> axis2, angle2 = R.axis_and_angle
            >>> allclose(axis1, axis2)
            True
            >>> allclose([angle1], [angle2])
            True
        """
        return axis_and_angle_from_matrix(self.matrix)

    @property
    def axis_angle_vector(self):
        """Returns the axis-angle vector of the ``Rotation``.

        Returns:
            (:obj:`list` of :obj:`float`): Three numbers that represent the \
                axis of rotation and angle of rotation through the vector's \
                magnitude.

        Example:
            >>> aav1 = [-0.043, -0.254, 0.617]
            >>> R = Rotation.from_axis_angle_vector(aav1)
            >>> aav2 = R.axis_angle_vector
            >>> allclose(aav1, aav2)
            True
        """
        axis, angle = self.axis_and_angle
        return scale_vector(axis, angle)

    def euler_angles(self, static=True, axes='xyz'):
        """Returns Euler angles from the ``Rotation`` according to specified \
            axis sequence and rotation type.

        Args:
            static(:obj:`bool`, optional): If true the rotations are applied to
                a static frame. If not, to a rotational. Defaults to True.
            axes(:obj:`str`, optional): A 3 character string specifying the
                order of the axes. Defaults to 'xyz'.

        Returns:
            (:obj:`list` of :obj:`float`): The 3 Euler angles.

        Example:
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
        """
        return basis_vectors_from_matrix(self.matrix)


class Translation(Transformation):
    """Creates a translation transformation.

    Args:
        translation (:obj:`list` of :obj:`float`): a list of 3 numbers
            defining the translation in x, y, and z.

    Example:
        >>> T = Translation([1, 2, 3])
    """

    def __init__(self, translation):
        self.matrix = matrix_from_translation(translation)


class Scale(Transformation):
    """Creates a scaling transformation.

    Args:
        scale_factors (:obj:`list` of :obj:`float`): a list of 3 numbers
            defining the scaling factors in x, y, and z respectively.

    Example:
        >>> S = Scale([1, 2, 3])
    """

    def __init__(self, scale_factors):
        self.matrix = matrix_from_scale_factors(scale_factors)


class Reflection(Transformation):
    """Creates a ``Reflection`` that mirrors points at a plane, defined by
        point and normal vector.

    Args:
        point (:obj:`list` of :obj:`float`): The point of the mirror plane.
        normal (:obj:`list` of :obj:`float`): The normal of the mirror plane.

    Example:
        >>> point = [1, 1, 1]
        >>> normal = [0, 0, 1]
        >>> R1 = Reflection(point, normal)
        >>> R2 = Transformation.from_matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, -1, 2], [0, 0, 0, 1]])
        >>> R1 == R2
        True

    """

    def __init__(self, point, normal):
        super(Reflection, self).__init__()

        normal = normalize_vector((list(normal)))

        for i in range(3):
            for j in range(3):
                self.matrix[i][j] -= 2.0 * normal[i] * normal[j]

        for i in range(3):
            self.matrix[i][3] = 2 * dot_vectors(point, normal) *\
                normal[i]

    @classmethod
    def from_frame(cls, frame):
        """Creates a ``Reflection`` that mirrors at the ``Frame``.

        Args:
            frame(:class:`Frame`)
        """
        return cls(frame.point, frame.normal)


class Projection(Transformation):

    @classmethod
    def orthogonal(cls, point, normal):
        """Returns an orthogonal ``Projection`` to project onto a plane \
            defined by point and normal.

        Args:
            point(:obj:`list` of :obj:`float`)
            normal(:obj:`list` of :obj:`float`)

        Example:
            >>> point = [0, 0, 0]
            >>> normal = [0, 0, 1]
            >>> P = Projection.orthogonal(point, normal)
        """
        M = matrix_from_orthogonal_projection(point, normal)
        return cls(M)

    @classmethod
    def parallel(cls, point, normal, direction):
        """Returns an parallel ``Projection`` to project onto a plane defined \
            by point, normal and direction.

        Args:
            point(:obj:`list` of :obj:`float`)
            normal(:obj:`list` of :obj:`float`)
            direction(:obj:`list` of :obj:`float`)

        Example:
            >>> point = [0, 0, 0]
            >>> normal = [0, 0, 1]
            >>> direction = [1, 1, 1]
            >>> P = Projection.parallel(point, normal, direction)
        """
        M = matrix_from_parallel_projection(point, normal, direction)
        return cls(M)

    @classmethod
    def perspective(cls, point, normal, perspective):
        """Returns an perspective ``Projection`` to project onto a plane \
            defined by point, normal and perspective.

        Args:
            point(:obj:`list` of :obj:`float`)
            normal(:obj:`list` of :obj:`float`)
            perspective(:obj:`list` of :obj:`float`)

        Example:
            >>> point = [0, 0, 0]
            >>> normal = [0, 0, 1]
            >>> perspective = [1, 1, 0]
            >>> P = Projection.perspective(point, normal, perspective)
        """
        M = matrix_from_perspective_projection(point, normal, perspective)
        return cls(M)

    @classmethod
    def from_entries(cls, perspective_entries):
        """Constructs a perspective transformation by the perspective entries \
            of a matrix.

        Args:
            perspective_entries(:obj:`list` of :obj:`float`): The 4 perspective
                entries of a matrix.
        """
        M = matrix_from_perspective_entries(perspective_entries)
        return cls(M)


class Shear(Transformation):
    """Constructs a ``Shear`` transformation by an angle along the \
        direction vector on the shear plane (defined by point and normal).

    A point P is transformed by the shear matrix into P" such that
    the vector P-P" is parallel to the direction vector and its extent is
    given by the angle of P-P'-P", where P' is the orthogonal projection
    of P onto the shear plane (defined by point and normal).

    Args:
        angle (:obj:`float`): The angle in radians.
        direction (:obj:`list` of :obj:`float`): The direction vector as
            list of 3 numbers. It must be orthogonal to the normal vector.
        point (:obj:`list` of :obj:`float`): The point of the shear plane
            as list of 3 numbers.
        normal (:obj:`list` of :obj:`float`): The normal of the shear plane
            as list of 3 numbers.

    Raises:
        ValueError: If direction and normal are not orthogonal.

    Example:
        >>> angle = 0.1
        >>> direction = [0.1, 0.2, 0.3]
        >>> point = [4, 3, 1]
        >>> normal = cross_vectors(direction, [1, 0.3, -0.1])
        >>> S = Shear(angle, direction, point, normal)
    """

    def __init__(self, angle=0., direction=[1, 0, 0],
                 point=[1, 1, 1], normal=[0, 0, 1]):

        self.matrix = matrix_from_shear(angle, direction, point, normal)

    @classmethod
    def from_entries(cls, shear_entries):
        """Creates a ``Shear`` from the 3 factors for x-y, x-z, and y-z axes.

        Args:
            shear_factors (:obj:`list` of :obj:`float`): The 3 shear factors
                for x-y, x-z, and y-z axes.

        Example:
            >>> S = Shear.from_entries([1, 2, 3])
        """
        M = matrix_from_shear_entries(shear_entries)
        return cls.from_matrix(M)


if __name__ == "__main__":

    from compas.geometry.objects.frame import Frame
    f1 = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
    T = Transformation.from_frame(f1)
    f2 = Frame.from_transformation(T)
    print(f1 == f2)

    f = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
    T = Transformation.from_frame(f)
    Tinv = T.inverse()
    I = Transformation()
    print(I == T * Tinv)

    f1 = Frame([2, 2, 2], [0.12, 0.58, 0.81], [-0.80, 0.53, -0.26])
    f2 = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
    T = Transformation.from_frame_to_frame(f1, f2)
    f1.transform(T)
    print(f1 == f2)

    trans1 = [1, 2, 3]
    angle1 = [-2.142, 1.141, -0.142]
    scale1 = [0.123, 2, 0.5]
    T = matrix_from_translation(trans1)
    R = matrix_from_euler_angles(angle1)
    S = matrix_from_scale_factors(scale1)
    M = multiply_matrices(multiply_matrices(T, R), S)
    # M = compose_matrix(scale1, None, angle1, trans1, None)
    scale2, shear2, angle2, trans2, persp2 = decompose_matrix(M)
    print(allclose(scale1, scale2))
    print(allclose(angle1, angle2))
    print(allclose(trans1, trans2))

    T1 = Translation(trans1)
    R1 = Rotation.from_euler_angles(angle1)
    S1 = Scale(scale1)
    M = (T1 * R1) * S1
    S2, Sh, R2, T2, P = M.decompose()
    print(S1 == S2)
    print(R1 == R2)
    print(T1 == T2)

    shear1 = [-0.41, -0.14, -0.35]
    persp1 = [0.3, 0.1, 0.1, 1]
    Sh1 = Shear.from_entries(shear1)
    S2, Sh, R2, T2, P = Sh1.decompose()
    # print("Sh", Sh)

    P1 = Projection.from_entries(persp1)
    S2, Sh, R2, T2, P = P1.decompose()
    # print("P", P)

    f = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
    T = Transformation.from_frame(f)
    q = T.transform_point([0, 0, 0])
    print(allclose(f.point, q))

    f1 = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
    T = Transformation.from_frame(f1)
    pts = [[1.0, 1.0, 1.0], [1.68, 1.68, 1.27], [0.33, 1.73, 0.85]]
    pts_ = T.transform_points(pts)

    xaxis = [0.68, 0.68, 0.27]
    yaxis = [-0.67, 0.73, -0.15]
    R = Rotation.from_basis_vectors(xaxis, yaxis)

    q1 = [0.945, -0.021, -0.125, 0.303]
    R = Rotation.from_quaternion(q1)
    q2 = R.quaternion
    print(allclose(q1, q2, tol=1e-3))

    aav1 = [-0.043, -0.254, 0.617]
    R = Rotation.from_axis_angle_vector(aav1)
    aav2 = R.axis_angle_vector
    print(allclose(aav1, aav2))

    axis1 = normalize_vector([-0.043, -0.254, 0.617])
    angle1 = 0.1
    R = Rotation.from_axis_and_angle(axis1, angle1)
    axis2, angle2 = R.axis_and_angle
    print(allclose(axis1, axis2))
    print(allclose([angle1], [angle2]))

    ea1 = 1.4, 0.5, 2.3
    args = False, 'xyz'
    R1 = Rotation.from_euler_angles(ea1, *args)
    ea2 = R1.euler_angles(*args)
    print(allclose(ea1, ea2))

    alpha, beta, gamma = ea1
    origin, xaxis, yaxis, zaxis = [0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]
    Rx = Rotation.from_axis_and_angle(xaxis, alpha)
    Ry = Rotation.from_axis_and_angle(yaxis, beta)
    Rz = Rotation.from_axis_and_angle(zaxis, gamma)
    R2 = Rx * Ry * Rz
    print(R1 == R2)

    f1 = Frame([0, 0, 0], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
    R = Rotation.from_frame(f1)
    args = False, 'xyz'
    alpha, beta, gamma = R.euler_angles(*args)
    xaxis, yaxis, zaxis = [1, 0, 0], [0, 1, 0], [0, 0, 1]
    Rx = Rotation.from_axis_and_angle(xaxis, alpha)
    Ry = Rotation.from_axis_and_angle(yaxis, beta)
    Rz = Rotation.from_axis_and_angle(zaxis, gamma)
    f2 = Frame.worldXY()
    f2.transform(Rx * Ry * Rz)
    print(f1 == f2)

    angle = 0.1
    direction = [0.1, 0.2, 0.3]
    point = [4, 3, 1]
    normal = cross_vectors(direction, [1, 0.3, -0.1])
    S = Shear(angle, direction, point, normal)
    print(S)
    S = Shear.from_entries([1, 2, 3])
