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


class Projection(Transformation):
    """Class representing a projection transformation.

    Parameters
    ----------
    matrix : list[list[float]], optional
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
                raise ValueError("This is not a proper projection matrix.")
        super(Projection, self).__init__(matrix=matrix)

    def __repr__(self):
        return "Projection({0!r})".format(self.matrix)

    @classmethod
    def from_plane(cls, plane):
        """Construct an orthogonal projection transformation to project onto a plane.

        Parameters
        ----------
        plane : [point, normal] | :class:`~compas.geometry.Plane`
            The plane to project onto.

        Returns
        -------
        :class:`~compas.geometry.Projection`
            An orthogonal projection transformation.

        Examples
        --------
        >>> from compas.geometry import Plane
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
        """Construct a parallel projection transformation to project onto a plane along a specific direction.

        Parameters
        ----------
        plane : [point, normal] | :class:`~compas.geometry.Plane`
            The plane to project onto.
        direction : [float, float, float] | :class:`~compas.geometry.Vector`
            The direction of projection direction.

        Returns
        -------
        :class:`~compas.geometry.Projection`
            A parallel projection transformation.

        Examples
        --------
        >>> from compas.geometry import Plane
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
        """Construct a perspective projection transformation to project onto a plane along lines that emanate from a single point, called the center of projection.

        Parameters
        ----------
        plane : [point, normal] | :class:`~compas.geometry.Plane`
            The plane to project onto.
        center_of_projection : [float, float, float] | :class:`~compas.geometry.Point`
            The camera view point.

        Returns
        -------
        :class:`~compas.geometry.Projection`
            A perspective projection transformation.

        Examples
        --------
        >>> from compas.geometry import Plane
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
        perspective_entries : [float, float, float, float]
            The 4 perspective entries of a matrix.

        Returns
        -------
        :class:`~compas.geometry.Projection`
            A projection transformation.

        """
        P = cls()
        P.matrix = matrix_from_perspective_entries(perspective_entries)
        return P
