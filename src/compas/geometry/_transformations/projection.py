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
from compas.utilities import flatten
from compas.geometry import allclose
from compas.geometry._transformations import decompose_matrix
from compas.geometry._transformations import matrix_from_orthogonal_projection
from compas.geometry._transformations import matrix_from_parallel_projection
from compas.geometry._transformations import matrix_from_perspective_projection
from compas.geometry._transformations import matrix_from_perspective_entries
from compas.geometry._transformations import Transformation


__all__ = ['Projection']


class Projection(Transformation):
    """Create a projection transformation.

    Parameters
    ----------
    matrix : 4x4 matrix-like, optional
        A 4x4 matrix (or similar) representing a projection transformation.

    Raises
    ------
    ValueError
        If the default constructor is used,
        and the provided transformation matrix is not a shear matrix.

    Examples
    --------
    >>>
    """

    __module__ = 'compas.geometry'

    def __init__(self, matrix=None):
        if matrix:
            _, _, _, _, perspective = decompose_matrix(matrix)
            check = matrix_from_perspective_entries(perspective)
            if not allclose(flatten(matrix), flatten(check)):
                raise ValueError('This is not a proper projection matrix.')
        super(Projection, self).__init__(matrix=matrix)

    # rename
    @classmethod
    def orthogonal(cls, point, normal):
        """Returns an orthogonal ``Projection`` to project onto a plane
        defined by point and normal.

        Parameters
        ----------
        point : list of float
        normal : list of float

        Returns
        -------
        Projection
            An orthogonal projection transformation.

        Examples
        --------
        >>> point = [0, 0, 0]
        >>> normal = [0, 0, 1]
        >>> P = Projection.orthogonal(point, normal)
        """
        P = cls()
        P.matrix = matrix_from_orthogonal_projection(point, normal)
        return P

    # rename
    @classmethod
    def parallel(cls, point, normal, direction):
        """Returns a parallel ``Projection`` to project onto a plane defined
        by point, normal and direction.

        Parameters
        ----------
        point : list of float
        normal : list of float
        direction : list of float

        Returns
        -------
        Projection
            A parallel projection transformation.

        Examples
        --------
        >>> point = [0, 0, 0]
        >>> normal = [0, 0, 1]
        >>> direction = [1, 1, 1]
        >>> P = Projection.parallel(point, normal, direction)
        """
        P = cls()
        P.matrix = matrix_from_parallel_projection(point, normal, direction)
        return P

    # rename
    # what does perspective represent?
    @classmethod
    def perspective(cls, point, normal, perspective):
        """Returns a perspective ``Projection`` to project onto a plane
        defined by point, normal and perspective.

        Parameters
        ----------
        point : list of float
        normal : list of float
        perspective : list of float

        Returns
        -------
        Projection
            A perspective projection transformation.

        Examples
        --------
        >>> point = [0, 0, 0]
        >>> normal = [0, 0, 1]
        >>> perspective = [1, 1, 0]
        >>> P = Projection.perspective(point, normal, perspective)
        """
        P = cls()
        P.matrix = matrix_from_perspective_projection(point, normal, perspective)
        return P

    @classmethod
    def from_entries(cls, perspective_entries):
        """Constructs a perspective transformation by the perspective entries
        of a matrix.

        Parameters
        ----------
        perspective_entries : list of float
            The 4 perspective entries of a matrix.

        Returns
        -------
        Projection
            A projection transformation.
        """
        P = cls()
        P.matrix = matrix_from_perspective_entries(perspective_entries)
        return P


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import doctest

    doctest.testmod(globs=globals())
