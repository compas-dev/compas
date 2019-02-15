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

from compas.geometry.basic import multiply_matrices

from compas.geometry._primitives import Point
from compas.geometry._primitives import Vector

from compas.geometry.transformations import inverse
from compas.geometry.transformations import identity_matrix
from compas.geometry.transformations import matrix_from_frame
from compas.geometry.transformations import matrix_from_euler_angles
from compas.geometry.transformations import basis_vectors_from_matrix
from compas.geometry.transformations import translation_from_matrix
from compas.geometry.transformations import decompose_matrix


__all__ = ['Transformation']


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

    def copy(self):
        """Returns a copy of the transformation.
        """
        cls = type(self)
        return cls.from_matrix(self.matrix)

    def __repr__(self):
        s  = "[[%s],\n" % ",".join([("%.4f" % n).rjust(10) for n in self.matrix[0]])
        s += " [%s],\n" % ",".join([("%.4f" % n).rjust(10) for n in self.matrix[1]])
        s += " [%s],\n" % ",".join([("%.4f" % n).rjust(10) for n in self.matrix[2]])
        s += " [%s]]\n" % ",".join([("%.4f" % n).rjust(10) for n in self.matrix[3]])
        return s

    def __len__(self):
        return len(self.matrix)

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
        from compas.geometry.xforms import Scale
        from compas.geometry.xforms import Shear
        from compas.geometry.xforms import Rotation
        from compas.geometry.xforms import Translation
        from compas.geometry.xforms import Projection

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
        xv, yv = basis_vectors_from_matrix(R)
        return Vector(*xv), Vector(*yv)

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


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    from compas.geometry import Point
    from compas.geometry import Frame
    from compas.geometry import allclose
    from compas.geometry import matrix_from_translation
    from compas.geometry import matrix_from_scale_factors
    from compas.geometry import transform_points

    from numpy import asarray


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

    f = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
    T = Transformation.from_frame(f)
    p = Point(0, 0, 0)
    p.transform(T)
    print(allclose(f.point, p))

    f1 = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
    T = Transformation.from_frame(f1)
    points = [[1.0, 1.0, 1.0], [1.68, 1.68, 1.27], [0.33, 1.73, 0.85]]
    points = transform_points(points, T)

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
