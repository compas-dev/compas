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

from compas.geometry import dot_vectors
from compas.geometry import normalize_vector

from compas.geometry._transformations import identity_matrix
from compas.geometry._transformations import Transformation


__all__ = ['Reflection']


class Reflection(Transformation):
    """Creates a ``Reflection`` that mirrors points at a plane, defined by
    point and normal vector.

    Examples
    --------
    point = [1, 1, 1]
    normal = [0, 0, 1]
    R1 = Reflection.from_plane((point, normal))
    R2 = Transformation([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, -1, 2], [0, 0, 0, 1]])
    R1 == R2
    True
    """

    def __init__(self, matrix=None):
        if matrix:
            pass
        super(Reflection, self).__init__(matrix=matrix)

    @classmethod
    def from_plane(cls, plane):
        """Creates a reflection object that mirrors wrt the given plane.

        Parameters
        ----------
        plane : compas.geometry.Plane or (point, normal)
            The reflection plane.

        Returns
        -------
        Reflection
            The reflection transformation.
        """
        point, normal = plane
        normal = normalize_vector((list(normal)))
        matrix = identity_matrix(4)
        for i in range(3):
            for j in range(3):
                matrix[i][j] -= 2.0 * normal[i] * normal[j]
        for i in range(3):
            matrix[i][3] = 2 * dot_vectors(point, normal) * normal[i]
        R = cls()
        R.matrix = matrix
        return R

    @classmethod
    def from_frame(cls, frame):
        """Creates a reflection object that mirrors wrt the given frame.

        Parameters
        ----------
        frame : compas.geometry.Frame or (point, xaxis, yaxis, zaxis)

        Returns
        -------
        Reflection
            The reflection transformation.
        """
        point = frame.point
        z = frame.zaxis
        plane = point, z
        return cls.from_plane(plane)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    point = [1, 1, 1]
    normal = [0, 0, 1]
    R1 = Reflection.from_plane((point, normal))
    R2 = Transformation([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, -1, 2], [0, 0, 0, 1]])
    print(R1 == R2)
