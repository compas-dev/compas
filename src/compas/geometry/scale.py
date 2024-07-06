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
from compas.geometry import decompose_matrix
from compas.geometry import matrix_from_frame
from compas.geometry import matrix_from_scale_factors
from compas.geometry import matrix_inverse
from compas.geometry import multiply_matrices
from compas.itertools import flatten
from compas.tolerance import TOL


class Scale(Transformation):
    """Class representing a scale transformation.

    Parameters
    ----------
    matrix : list[list[float]], optional
        A 4x4 matrix (or similar) representing a scaling.
    check : bool, optional
        If ``True``, the provided matrix will be checked for validity.
    name : str, optional
        The name of the transformation.

    Raises
    ------
    ValueError
        If ``check`` is ``True`` and the provided transformation matrix is not a scale matrix.

    Examples
    --------
    >>> S = Scale.from_factors([1, 2, 3])
    >>> S[0, 0] == 1
    True
    >>> S[1, 1] == 2
    True
    >>> S[2, 2] == 3
    True

    >>> from compas.geometry import Point, Frame
    >>> point = Point(2, 5, 0)
    >>> frame = Frame(point, (1, 0, 0), (0, 1, 0))
    >>> points = [point, Point(2, 10, 0)]
    >>> S = Scale.from_factors([2.0] * 3, frame)
    >>> points = [p.transformed(S) for p in points]
    >>> print(points)
    [Point(x=2.000, y=5.000, z=0.000), Point(x=2.000, y=15.000, z=0.000)]

    """

    def __init__(self, matrix=None, check=False, name=None):
        if matrix and check:
            scale, _, _, _, _ = decompose_matrix(matrix)
            if not TOL.is_allclose(flatten(matrix), flatten(matrix_from_scale_factors(scale))):
                raise ValueError("This is not a proper scale matrix.")
        super(Scale, self).__init__(matrix=matrix, name=name)

    @classmethod
    def from_factors(cls, factors, frame=None):
        """Construct a scale transformation from scale factors.

        Parameters
        ----------
        factors : [float, float, float]
            The scale factors along X, Y, Z.
        frame : [point, vector, vector] | :class:`compas.geometry.Frame`, optional
            The anchor frame for the scaling transformation.

        Returns
        -------
        :class:`compas.geometry.Scale`
            A scale transformation.

        Examples
        --------
        >>> from compas.geometry import Point, Frame
        >>> point = Point(2, 5, 0)
        >>> frame = Frame(point, (1, 0, 0), (0, 1, 0))
        >>> points = [point, Point(2, 10, 0)]
        >>> S = Scale.from_factors([2.0] * 3, frame)
        >>> points = [p.transformed(S) for p in points]
        >>> print(points)
        [Point(x=2.000, y=5.000, z=0.000), Point(x=2.000, y=15.000, z=0.000)]

        """
        matrix = matrix_from_scale_factors(factors)
        if frame:
            Tw = matrix_from_frame(frame)
            Tl = matrix_inverse(Tw)
            matrix = multiply_matrices(multiply_matrices(Tw, matrix), Tl)
        return cls(matrix)
