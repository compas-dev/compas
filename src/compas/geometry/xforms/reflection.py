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

from compas.geometry.basic import dot_vectors
from compas.geometry.basic import normalize_vector

from compas.geometry.xforms import Transformation


__all__ = ['Reflection']


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


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
