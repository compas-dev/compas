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
from compas.geometry.transformations import matrix_from_translation
from compas.geometry.transformations import Transformation


__all__ = ['Translation']


class Translation(Transformation):
    """Create a translation transformation.

    Parameters
    ----------
    matrix : 4x4 matrix-like, optional
        A 4x4 matrix (or similar) representing a translation.

    Raises
    ------
    ValueError
        If the default constructor is used,
        and the provided transformation matrix is not a translation.

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

    def __init__(self, matrix=None):
        if matrix:
            _, _, _, translation, _ = decompose_matrix(matrix)
            check = matrix_from_translation(translation)
            if not allclose(flatten(matrix), flatten(check)):
                raise ValueError('This is not a proper translation matrix.')
        super(Translation, self).__init__(matrix=matrix)

    @classmethod
    def from_vector(cls, vector):
        """Create a translation transformation from a translation vector.

        Parameters
        ----------
        vector : :obj:`list` or :class:`compas.geometry.Vector`
            The translation vector.

        Returns
        -------
        Translation
            The translation transformation.
        """
        return cls(matrix_from_translation(vector))

    @property
    def translation_vector(self):
        """:class:`compas.geometry.Vector` : The translation vector."""
        from compas.geometry import Vector
        x = self.matrix[0][3]
        y = self.matrix[1][3]
        z = self.matrix[2][3]
        return Vector(x, y, z)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import doctest
    doctest.testmod()
