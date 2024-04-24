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
from compas.geometry import decompose_matrix
from compas.geometry import matrix_from_orthogonal_projection
from compas.geometry import matrix_from_parallel_projection
from compas.geometry import matrix_from_perspective_entries
from compas.geometry import matrix_from_perspective_projection
from compas.itertools import flatten
from compas.tolerance import TOL


class Projection(Transformation):
    """Class representing a projection transformation.

    Parameters
    ----------
    matrix : list[list[float]], optional
        A 4x4 matrix (or similar) representing a projection transformation.
    check : bool, optional
        If ``True``, the provided matrix will be checked for validity.
    name : str, optional
        The name of the transformation.

    Raises
    ------
    ValueError
        If ``check`` is ``True`` and the provided transformation matrix is not a projection matrix.

    Examples
    --------
    >>>

    """

    def __init__(self, matrix=None, check=False, name=None):
        if matrix and check:
            _, _, _, _, perspective = decompose_matrix(matrix)
            if not TOL.is_allclose(flatten(matrix), flatten(matrix_from_perspective_entries(perspective))):
                raise ValueError("This is not a proper projection matrix.")
        super(Projection, self).__init__(matrix=matrix, name=name)

    @classmethod
    def from_plane(cls, plane):
        """Construct an orthogonal projection transformation to project onto a plane.

        Parameters
        ----------
        plane : [point, normal] | :class:`compas.geometry.Plane`
            The plane to project onto.

        Returns
        -------
        :class:`compas.geometry.Projection`
            An orthogonal projection transformation.

        Examples
        --------
        >>> from compas.geometry import Plane
        >>> point = [0, 0, 0]
        >>> normal = [0, 0, 1]
        >>> plane = Plane(point, normal)
        >>> P = Projection.from_plane(plane)

        """
        matrix = matrix_from_orthogonal_projection(plane)
        return cls(matrix)

    @classmethod
    def from_plane_and_direction(cls, plane, direction):
        """Construct a parallel projection transformation to project onto a plane along a specific direction.

        Parameters
        ----------
        plane : [point, normal] | :class:`compas.geometry.Plane`
            The plane to project onto.
        direction : [float, float, float] | :class:`compas.geometry.Vector`
            The direction of projection direction.

        Returns
        -------
        :class:`compas.geometry.Projection`
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
        matrix = matrix_from_parallel_projection(plane, direction)
        return cls(matrix)

    @classmethod
    def from_plane_and_point(cls, plane, center_of_projection):
        """Construct a perspective projection transformation to project onto a plane along lines that emanate from a single point, called the center of projection.

        Parameters
        ----------
        plane : [point, normal] | :class:`compas.geometry.Plane`
            The plane to project onto.
        center_of_projection : [float, float, float] | :class:`compas.geometry.Point`
            The camera view point.

        Returns
        -------
        :class:`compas.geometry.Projection`
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
        matrix = matrix_from_perspective_projection(plane, center_of_projection)
        return cls(matrix)

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
        :class:`compas.geometry.Projection`
            A projection transformation.

        """
        matrix = matrix_from_perspective_entries(perspective_entries)
        return cls(matrix)
