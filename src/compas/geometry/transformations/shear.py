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
# from compas.utilities import flatten
# from compas.geometry import allclose
# from compas.geometry.transformations import decompose_matrix
from compas.geometry.transformations import matrix_from_shear_entries
from compas.geometry.transformations import matrix_from_shear
from compas.geometry.transformations import Transformation


__all__ = ['Shear']


class Shear(Transformation):
    """Create a shear transformation.

    A point P is transformed by the shear matrix into P" such that
    the vector P-P" is parallel to the direction vector and its extent is
    given by the angle of P-P'-P", where P' is the orthogonal projection
    of P onto the shear plane.

    Parameters
    ----------
    matrix : 4x4 matrix-like, optional
        A 4x4 matrix (or similar) representing a shear transformation.

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
            # _, shear, _, _, _ = decompose_matrix(matrix)
            # check = matrix_from_shear_entries(shear)
            # if not allclose(flatten(matrix), flatten(check)):
            #     raise ValueError('This is not a proper shear matrix.')
            pass
        super(Shear, self).__init__(matrix=matrix)

    @classmethod
    def from_angle_direction_plane(cls, angle, direction, plane):
        """
        Parameters
        ----------
        angle : :obj:`float`
            The angle in radians.
        direction : compas.geometry.Vector or :obj:`list` of :obj:`float`
            The direction vector as list of 3 numbers.
            It must be orthogonal to the normal vector (i.e. it must lie in the shear plane).
        plane : compas.geometry.Plane or (point, normal)
            The shear plane defined by a point and normal.

        Raises
        ------
        ValueError
            If the shear direction does not lie in the shear plane.

        Returns
        -------
        Shear
            The shear transformation object.

        Examples
        --------
        >>> angle = 0.1
        >>> direction = [0.1, 0.2, 0.3]
        >>> point = [4, 3, 1]
        >>> normal = cross_vectors(direction, [1, 0.3, -0.1])
        >>> S = Shear.from_angle_direction_plane(angle, direction, (point, normal))
        """
        point, normal = plane
        return cls(matrix_from_shear(angle, direction, point, normal))

    @classmethod
    def from_entries(cls, shear_entries):
        """Creates a ``Shear`` from the 3 factors for x-y, x-z, and y-z axes.

        Parameters
        ----------
        shear_factors : :obj:`list` of :obj:`float`
            The 3 shear factors for x-y, x-z, and y-z axes.

        Examples
        --------
        >>> S = Shear.from_entries([1, 2, 3])
        """
        return cls(matrix_from_shear_entries(shear_entries))


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import doctest

    from compas.geometry import Shear  # noqa: F401 F811
    from compas.geometry import cross_vectors  # noqa: F401

    doctest.testmod(globs=globals())
