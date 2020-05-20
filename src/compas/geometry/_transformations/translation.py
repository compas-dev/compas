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
from compas.geometry._transformations import matrix_from_translation
from compas.geometry._transformations import Transformation


__all__ = ['Translation']


class Translation(Transformation):
    """Creates a translation transformation.

    Parameters
    ----------
    vector : compas.geometry.Vector or list of float
        A translation vector.

    Examples
    --------
    >>> T = Translation([1, 2, 3])
    >>> T.matrix[0][3] == 1
    True
    >>> T.matrix[1][3] == 2
    True
    >>> T.matrix[2][3] == 3
    True
    """

    __module__ = 'compas.geometry'

    def __init__(self, vector):
        super(Translation, self).__init__(matrix_from_translation(vector))


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import doctest
    doctest.testmod()
