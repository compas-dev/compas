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
from compas.geometry._transformations import decompose_matrix
from compas.geometry._transformations import matrix_from_scale_factors
from compas.geometry._transformations import Transformation


__all__ = ['Scale']


class Scale(Transformation):
    """Creates a scale transformation.

    Parameters
    ----------
    matrix : 4x4 matrix-like, optional
        A 4x4 matrix (or similar) representing a scaling.

    Raises
    ------
    ValueError
        If the default constructor is used,
        and the provided transformation matrix is not a scale matrix.

    Examples
    --------
    >>> S = Scale.from_factors([1, 2, 3])
    >>> S[0, 0] == 1
    True
    >>> S[1, 1] == 2
    True
    >>> S[2, 2] == 3
    True
    """

    def __init__(self, matrix=None):
        if matrix:
            scale, _, _, _, _ = decompose_matrix(matrix)
            check = matrix_from_scale_factors(scale)
            if not allclose(flatten(matrix), flatten(check)):
                raise ValueError('This is not a proper scale matrix.')
        super(Scale, self).__init__(matrix=matrix)

    @classmethod
    def from_factors(cls, factors):
        """Construct a scale transformation from scale factors.

        Parameters
        ----------
        factors : list of float
            The scale factors along X, Y, Z.

        Returns
        -------
        Scale
            A scale transformation.
        """
        S = cls()
        S.matrix = matrix_from_scale_factors(factors)
        return S


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    import doctest
    doctest.testmod()
