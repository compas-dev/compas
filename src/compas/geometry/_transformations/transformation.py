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

from compas.geometry import multiply_matrices
from compas.geometry import transpose_matrix

from compas.geometry._transformations import matrix_inverse
from compas.geometry._transformations import matrix_determinant
from compas.geometry._transformations import identity_matrix
from compas.geometry._transformations import matrix_from_frame
from compas.geometry._transformations import matrix_from_euler_angles
from compas.geometry._transformations import basis_vectors_from_matrix
from compas.geometry._transformations import translation_from_matrix
from compas.geometry._transformations import decompose_matrix


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

    Attributes
    ----------
    matrix : :obj:`list` of :obj:`list` of :obj:`float`
        Square matrix.

    Examples
    --------
    >>> from compas.geometry import Frame
    >>> T = Transformation()
    >>> f1 = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
    >>> T = Transformation.from_frame(f1)
    >>> Sc, Sh, R, Tl, P = T.decomposed()
    >>> Tinv = T.inverse()

    """

    def __init__(self, matrix=None):
        if not matrix:
            matrix = identity_matrix(4)
        self.matrix = matrix

    def __mul__(self, other):
        return self.concatenated(other)

    def __imul__(self, other):
        return self.concatenated(other)

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
            A = self.matrix
            B = other.matrix
            for i in range(4):
                for j in range(4):
                    if math.fabs(A[i][j] - B[i][j]) > tol:
                        return False
            return True
        except BaseException:
            return False

    def copy(self):
        """Returns a copy of the transformation.
        """
        cls = type(self)
        return cls.from_matrix(self.matrix)

    def __repr__(self):
        s = "[[%s],\n" % ",".join([("%.4f" % n).rjust(10) for n in self.matrix[0]])
        s += " [%s],\n" % ",".join([("%.4f" % n).rjust(10) for n in self.matrix[1]])
        s += " [%s],\n" % ",".join([("%.4f" % n).rjust(10) for n in self.matrix[2]])
        s += " [%s]]\n" % ",".join([("%.4f" % n).rjust(10) for n in self.matrix[3]])
        return s

    def __len__(self):
        return len(self.matrix)

    @classmethod
    def from_matrix(cls, matrix):
        """Creates a ``Transformation`` from a 4x4 two-dimensional list of numbers.

        Parameters
        ----------
        matrix : :obj:`list` of :obj:`list` of `float`
            The 4x4 transformation matrix.

        Returns
        -------
        Transformation
            A transformation object.

        """
        T = cls()
        for i in range(4):
            for j in range(4):
                T.matrix[i][j] = float(matrix[i][j])
        return T

    @classmethod
    def from_list(cls, numbers):
        """Creates a ``Transformation`` from a list of 16 numbers.

        Parameters
        ----------
        numbers : :obj:`list` of :obj:`float`
            A list of 16 numbers

        Examples
        --------
        >>> numbers = [1, 0, 0, 3, 0, 1, 0, 4, 0, 0, 1, 5, 0, 0, 0, 1]
        >>> T = Transformation.from_list(numbers)

        Notes
        -----
        Since the transformation matrix follows the row-major order, the
        translational components must be at the list's indices 3, 7, 11.

        """
        T = cls()
        for i in range(4):
            for j in range(4):
                T.matrix[i][j] = float(numbers[i * 4 + j])
        return T

    @classmethod
    def from_frame(cls, frame):
        """Computes a transformation from world XY to frame.

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

        Notes
        -----
        It is the same as from_frame_to_frame(Frame.worldXY(), frame).

        """
        T = cls()
        T.matrix = matrix_from_frame(frame)
        return T

    @classmethod
    def from_frame_to_frame(cls, frame_from, frame_to):
        """Computes a transformation between two frames.

        This transformation allows to transform geometry from one Cartesian
        coordinate system defined by "frame_from" to another Cartesian
        coordinate system defined by "frame_to".

        Parameters
        ----------
        frame_from : :class:`Frame`
            A frame defining the original Cartesian coordinate system.
        frame_to : :class:`Frame`
            A frame defining the targeted Cartesian coordinate system.

        Returns
        -------
        Transformation
            The transformation representing a change of basis.

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
    def change_basis(cls, frame_from, frame_to):
        """Computes a change of basis transformation between two frames.

        A basis change is essentially a remapping of geometry from one
        coordinate system to another.

        Args:
            frame_from (:class:`Frame`): a frame defining the original
                Cartesian coordinate system
            frame_to (:class:`Frame`): a frame defining the targeted
                Cartesian coordinate system

        Example:
            >>> from compas.geometry import Point, Frame
            >>> f1 = Frame([2, 2, 2], [0.12, 0.58, 0.81], [-0.80, 0.53, -0.26])
            >>> f2 = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
            >>> T = Transformation.change_basis(f1, f2)
            >>> p_f1 = Point(1, 1, 1) # point in f1
            >>> p_f1.transformed(T) # point represented in f2
            Point(1.395, 0.955, 1.934)
            >>> Frame.local_to_local_coords(f1, f2, p_f1)
            Point(1.395, 0.955, 1.934)
        """

        T1 = cls.from_frame(frame_from)
        T2 = cls.from_frame(frame_to)

        return cls(multiply_matrices(matrix_inverse(T2.matrix), T1.matrix))

    @property
    def rotation(self):
        """Returns the ``Rotation`` component from the ``Transformation``.
        """
        Sc, Sh, R, T, P = self.decomposed()
        return R

    @property
    def translation(self):
        """Returns the 3 values of translation from the ``Transformation``.
        """
        return translation_from_matrix(self.matrix)

    @property
    def basis_vectors(self):
        """Returns the basis vectors from the ``Rotation`` component of the ``Transformation``.
        """
        from compas.geometry import Vector
        sc, sh, a, t, p = decompose_matrix(self.matrix)
        R = matrix_from_euler_angles(a, static=True, axes='xyz')
        xv, yv = basis_vectors_from_matrix(R)
        return Vector(*xv), Vector(*yv)

    @property
    def list(self):
        """Flattens the ``Transformation`` into a list of numbers.
        """
        return [a for c in self.matrix for a in c]

    def transpose(self):
        """Transpose the matrix of this transformation.

        Returns
        -------
        None
            The transformation is transposed in-place.
        """
        self.matrix = transpose_matrix(self.matrix)

    def transposed(self):
        """Create a transposed copy of this transformation.

        Returns
        -------
        T: :class:`compas.geometry.Transformation`
            The transposed transformation object.
        """
        T = self.copy()
        T.transpose()
        return T

    def invert(self):
        """Invert this transformation."""
        self.matrix = matrix_inverse(self.matrix)

    def inverse(self):
        """Returns the inverse transformation.

        Returns
        -------
        Transformation
            The inverse transformation.

        Examples
        --------
        >>> from compas.geometry import Frame
        >>> f = Frame([1, 1, 1], [0.68, 0.68, 0.27], [-0.67, 0.73, -0.15])
        >>> T = Transformation.from_frame(f)
        >>> I = Transformation()
        >>> I == T * T.inverse()
        True

        """
        # cls = type(self)
        # return cls(matrix_inverse(self.matrix))
        T = self.copy()
        T.invert()
        return T

    inverted = inverse

    def determinant(self):
        """The determinant of the matrix of the transformation.

        Returns
        -------
        float
            The determinant of the matrix of this transformation.
        """
        return matrix_determinant(self.matrix)

    def decomposed(self):
        """Decompose the ``Transformation`` into its ``Scale``, ``Shear``,
        ``Rotation``, ``Translation`` and ``Perspective`` components.

        Returns
        -------
        5-tuple of Transformation
            The scale, shear, rotation, tranlation, and projection components
            of the current transformation.

        Examples
        --------
        >>> trans1 = [1, 2, 3]
        >>> angle1 = [-2.142, 1.141, -0.142]
        >>> scale1 = [0.123, 2, 0.5]
        >>> T1 = Translation(trans1)
        >>> R1 = Rotation.from_euler_angles(angle1)
        >>> S1 = Scale(scale1)
        >>> M = (T1 * R1) * S1
        >>> Sc, Sh, R, T, P = M.decomposed()
        >>> S1 == Sc
        True
        >>> R1 == R
        True
        >>> T1 == T
        True

        """
        from compas.geometry import Scale  # noqa: F811
        from compas.geometry import Shear
        from compas.geometry import Rotation  # noqa: F811
        from compas.geometry import Translation  # noqa: F811
        from compas.geometry import Projection

        sc, sh, a, t, p = decompose_matrix(self.matrix)
        Sc = Scale(sc)
        Sh = Shear.from_entries(sh)
        R = Rotation.from_euler_angles(a, static=True, axes='xyz')
        T = Translation(t)
        P = Projection.from_entries(p)
        return Sc, Sh, R, T, P

    def concatenate(self, other):
        """Concatenate another transformation to this transformation.

        Parameters
        ----------
        other: :class:`compas.geometry.Transformation`
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

    def concatenated(self, other):
        """Concatenate two transformations into one ``Transformation``.

        Parameters
        ----------
        other: :class:`compas.geometry.Transformation`
            The transformation object to concatenate.

        Returns
        -------
        T: :class:`compas.geometry.Transformation`
            The new transformation that is the concatenation of this one and the other.

        Notes
        -----
        Rz * Ry * Rx means that Rx is first transformation, Ry second, and Rz third.
        """
        # T = self.copy()
        # T.concatenate(other)
        # return T
        cls = type(self)
        if isinstance(other, cls):
            return cls(multiply_matrices(self.matrix, other.matrix))
        return Transformation(multiply_matrices(self.matrix, other.matrix))


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    from compas.geometry import Translation  # noqa: F401
    from compas.geometry import Rotation  # noqa: F401
    from compas.geometry import Scale  # noqa: F401
    from compas.geometry import Frame  # noqa: F401

    import doctest
    doctest.testmod(globs=globals())
