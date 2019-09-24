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
from compas.geometry.transformations import matrix_from_shear_entries
from compas.geometry.transformations import matrix_from_shear

from compas.geometry.xforms import Transformation


__all__ = ['Shear']


class Shear(Transformation):
    """Constructs a ``Shear`` transformation by an angle along the
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


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    from compas.geometry import Frame
    from compas.geometry import Shear

    shear1 = [-0.41, -0.14, -0.35]
    Sh1 = Shear.from_entries(shear1)
    S2, Sh, R2, T2, P = Sh1.decompose()

    print(Sh)
