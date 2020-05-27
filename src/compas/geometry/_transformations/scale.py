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

from compas.geometry._transformations import matrix_from_scale_factors
from compas.geometry._transformations import Transformation


__all__ = ['Scale']


class Scale(Transformation):
    """Creates a scaling transformation.

    Parameters
    ----------
    factors : list of float
        Scale factor in the X-direction.
        Scale factor in the Y-direction.
        Scale factor in the Z-direction.

    Examples
    --------
    >>> S = Scale(1, 2, 3)
    >>> S.matrix[0][0] == 1
    True
    >>> S.matrix[1][1] == 2
    True
    >>> S.matrix[2][2] == 3
    True
    """

    __module__ = 'compas.geometry'

    # the default behaviour of providing a transformation matrix
    # should either be checked
    # or no longer allowed
    # the default init/constructor should therefore be overwritten
    def __init__(self, factors):
        super(Scale, self).__init__(matrix_from_scale_factors(factors))

    # there should be a property factors
    # this can have an equivalent yet more expensive version on the base object


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    import doctest
    doctest.testmod()
