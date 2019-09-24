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
from compas.geometry.transformations import matrix_from_translation

from compas.geometry.xforms import Transformation


__all__ = ['Translation']


class Translation(Transformation):
    """Creates a translation transformation.

    Args:
        translation (:obj:`list` of :obj:`float`): a list of 3 numbers
            defining the translation in x, y, and z.

    Example:
        >>> T = Translation([1, 2, 3])
    """

    def __init__(self, translation):
        self.matrix = matrix_from_translation(translation)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
