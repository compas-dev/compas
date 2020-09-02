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
from compas.geometry.transformations import decompose_matrix
from compas.geometry.transformations import matrix_from_orthogonal_projection
from compas.geometry.transformations import matrix_from_parallel_projection
from compas.geometry.transformations import matrix_from_perspective_projection
from compas.geometry.transformations import matrix_from_perspective_entries
from compas.geometry.transformations import Transformation


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

    def __init__(self, matrix=None):
        if matrix:
            _, _, _, _, perspective = decompose_matrix(matrix)
            check = matrix_from_perspective_entries(perspective)
            if not allclose(flatten(matrix), flatten(check)):
                raise ValueError('This is not a proper projection matrix.')
        super(Projection, self).__init__(matrix=matrix)

    @classmethod
    def from_plane(cls, plane):
        """Returns an orthogonal ``Projection`` to project onto a plane.

        Parameters
        ----------
        plane : compas.geometry.Plane or (point, normal)
            The plane to project onto.

        Returns
        -------
        Projection
            An orthogonal projection transformation.

        Examples
        --------
        >>> point = [0, 0, 0]
        >>> normal = [0, 0, 1]
        >>> plane = Plane(point, normal)
        >>> P = Projection.from_plane(plane)
        """
        P = cls()
        P.matrix = matrix_from_orthogonal_projection(plane)
        return P

    @classmethod
    def from_plane_and_direction(cls, plane, direction):
        """Returns a parallel ``Projection`` to project onto a plane along a
        specific direction.

        Parameters
        ----------
        plane : compas.geometry.Plane or (point, normal)
            The plane to project onto.
        direction : compas.geometry.Vector or list of float
            The direction of projection direction.

        Returns
        -------
        Projection
            A parallel projection transformation.

        Examples
        --------
        >>> point = [0, 0, 0]
        >>> normal = [0, 0, 1]
        >>> plane = Plane(point, normal)
        >>> direction = [1, 1, 1]
        >>> P = Projection.from_plane_and_direction(plane, direction)
        """
        P = cls()
        P.matrix = matrix_from_parallel_projection(plane, direction)
        return P

    @classmethod
    def from_plane_and_point(cls, plane, center_of_projection):
        """Returns a perspective ``Projection`` to project onto a plane along lines that emanate from a single point, called the center of projection.

        Parameters
        ----------
        plane : compas.geometry.Plane or (point, normal)
            The plane to project onto.
        center_of_projection : compas.geometry.Point or list of float
            The camera view point.

        Returns
        -------
        Projection
            A perspective projection transformation.

        Examples
        --------
        >>> point = [0, 0, 0]
        >>> normal = [0, 0, 1]
        >>> plane = Plane(point, normal)
        >>> center_of_projection = [1, 1, 0]
        >>> P = Projection.from_plane_and_point(plane, center_of_projection)
        """
        P = cls()
        P.matrix = matrix_from_perspective_projection(plane, center_of_projection)
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
    from compas.geometry import Plane  # noqa: F401
    doctest.testmod(globs=globals())
