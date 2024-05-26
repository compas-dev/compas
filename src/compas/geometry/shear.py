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
from compas.geometry import matrix_from_shear
from compas.geometry import matrix_from_shear_entries
from compas.itertools import flatten
from compas.tolerance import TOL


class Shear(Transformation):
    """Class representing a shear transformation.

    A point P is transformed by the shear matrix into P" such that
    the vector P-P" is parallel to the direction vector and its extent is
    given by the angle of P-P'-P", where P' is the orthogonal projection
    of P onto the shear plane.

    Parameters
    ----------
    matrix : list[list[float]], optional
        A 4x4 matrix (or similar) representing a shear transformation.
    check : bool, optional
        If ``True``, the provided matrix will be checked for validity.
    name : str, optional
        The name of the transformation.

    Raises
    ------
    ValueError
        If ``check`` is ``True`` and the provided transformation matrix is not a shear matrix.

    Examples
    --------
    >>>

    """

    def __init__(self, matrix=None, check=False, name=None):
        if matrix and check:
            _, shear, _, _, _ = decompose_matrix(matrix)
            if not TOL.is_allclose(flatten(matrix), flatten(matrix_from_shear_entries(shear))):
                raise ValueError("This is not a proper shear matrix.")
        super(Shear, self).__init__(matrix=matrix, name=name)

    @classmethod
    def from_angle_direction_plane(cls, angle, direction, plane):
        """Construct a shear transformation from an angle, direction and plane.

        Parameters
        ----------
        angle : float
            The angle in radians.
        direction : [float, float, float] | :class:`compas.geometry.Vector`
            The direction vector as list of 3 numbers.
            It must be orthogonal to the normal vector (i.e. it must lie in the shear plane).
        plane : [point, vector] | :class:`compas.geometry.Plane`
            The shear plane defined by a point and normal.

        Returns
        -------
        :class:`compas.geometry.Shear`
            The shear transformation object.

        Raises
        ------
        ValueError
            If the shear direction does not lie in the shear plane.

        Examples
        --------
        >>> from compas.geometry import cross_vectors
        >>> angle = 0.1
        >>> direction = [0.1, 0.2, 0.3]
        >>> point = [4, 3, 1]
        >>> normal = cross_vectors(direction, [1, 0.3, -0.1])
        >>> S = Shear.from_angle_direction_plane(angle, direction, (point, normal))

        """
        point, normal = plane
        matrix = matrix_from_shear(angle, direction, point, normal)
        return cls(matrix)

    @classmethod
    def from_entries(cls, shear_entries):
        """Construct a shear transformation from the 3 factors for x-y, x-z, and y-z axes.

        Parameters
        ----------
        shear_factors : [float, float, float]
            The 3 shear factors for x-y, x-z, and y-z axes.

        Returns
        -------
        :class:`compas.geometry.Shear`
            The shear transformation object.

        Examples
        --------
        >>> S = Shear.from_entries([1, 2, 3])

        """
        matrix = matrix_from_shear_entries(shear_entries)
        return cls(matrix)
