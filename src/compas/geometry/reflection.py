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
from compas.geometry import cross_vectors
from compas.geometry import decompose_matrix
from compas.geometry import dot_vectors
from compas.geometry import identity_matrix
from compas.geometry import matrix_from_perspective_entries
from compas.geometry import normalize_vector
from compas.itertools import flatten
from compas.tolerance import TOL


class Reflection(Transformation):
    """Class representing a reflection transformation.

    A reflection transformation mirrors points at a plane.

    Parameters
    ----------
    matrix : list[list[float]], optional
        A 4x4 matrix (or similar) representing a reflection.
    check : bool, optional
        If ``True``, the provided matrix will be checked for validity.
    name : str, optional
        The name of the transformation.

    Examples
    --------
    >>> point = [1, 1, 1]
    >>> normal = [0, 0, 1]
    >>> R1 = Reflection.from_plane((point, normal))
    >>> R2 = Transformation([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, -1, 2], [0, 0, 0, 1]])
    >>> R1 == R2
    True

    """

    def __init__(self, matrix=None, check=False, name=None):
        if matrix and check:
            _, _, _, _, perspective = decompose_matrix(matrix)
            if not TOL.is_allclose(flatten(matrix), flatten(matrix_from_perspective_entries(perspective))):
                raise ValueError("This is not a proper reflection matrix.")
        super(Reflection, self).__init__(matrix=matrix, name=name)

    @classmethod
    def from_plane(cls, plane):
        """Construct a reflection transformation that mirrors wrt the given plane.

        Parameters
        ----------
        plane : [point, vector] | :class:`compas.geometry.Plane`
            The reflection plane.

        Returns
        -------
        :class:`compas.geometry.Reflection`
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
        return cls(matrix)

    @classmethod
    def from_frame(cls, frame):
        """Construct a reflection transformation that mirrors wrt the given frame.

        Parameters
        ----------
        frame : [point, vector, vector] | :class:`compas.geometry.Frame`

        Returns
        -------
        :class:`compas.geometry.Reflection`
            The reflection transformation.

        """
        if isinstance(frame, (tuple, list)):
            point = frame[0]
            zaxis = cross_vectors(frame[1], frame[2])
        else:
            point = frame.point
            zaxis = frame.zaxis
        return cls.from_plane((point, zaxis))
