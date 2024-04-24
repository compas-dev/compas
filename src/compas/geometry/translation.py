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
from compas.geometry import matrix_from_translation
from compas.geometry import translation_from_matrix
from compas.itertools import flatten
from compas.tolerance import TOL


class Translation(Transformation):
    """Class representing a translation transformation.

    Parameters
    ----------
    matrix : list[list[float]], optional
        A 4x4 matrix (or similar) representing a translation.
    check : bool, optional
        If ``True``, the provided matrix will be checked for validity.
    name : str, optional
        The name of the transformation.

    Attributes
    ----------
    translation_vector : :class:`compas.geometry.Vector`
        The translation vector.

    Raises
    ------
    ValueError
        If ``check`` is ``True`` and the provided transformation matrix is not a translation.

    Examples
    --------
    >>> T = Translation.from_vector([1, 2, 3])
    >>> T[0, 3] == 1
    True
    >>> T[1, 3] == 2
    True
    >>> T[2, 3] == 3
    True

    >>> from compas.geometry import Vector
    >>> T = Translation.from_vector(Vector(1, 2, 3))
    >>> T[0, 3] == 1
    True
    >>> T[1, 3] == 2
    True
    >>> T[2, 3] == 3
    True

    >>> T = Translation([[1, 0, 0, 1], [0, 1, 0, 2], [0, 0, 1, 3], [0, 0, 0, 1]])
    >>> T[0, 3] == 1
    True
    >>> T[1, 3] == 2
    True
    >>> T[2, 3] == 3
    True

    """

    def __init__(self, matrix=None, check=False, name=None):
        if matrix and check:
            translation = translation_from_matrix(matrix)
            if not TOL.is_allclose(flatten(matrix), flatten(matrix_from_translation(translation))):
                raise ValueError("This is not a proper translation matrix.")
        super(Translation, self).__init__(matrix=matrix, name=name)

    @property
    def translation_vector(self):
        from compas.geometry import Vector

        x = self.matrix[0][3]
        y = self.matrix[1][3]
        z = self.matrix[2][3]
        return Vector(x, y, z)

    @classmethod
    def from_vector(cls, vector):
        """Create a translation transformation from a translation vector.

        Parameters
        ----------
        vector : [float, float, float] | :class:`compas.geometry.Vector`
            The translation vector.

        Returns
        -------
        :class:`compas.geometry.Translation`
            The translation transformation.

        """
        matrix = matrix_from_translation(vector)
        return cls(matrix)
