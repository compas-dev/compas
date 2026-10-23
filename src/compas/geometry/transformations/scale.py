from collections.abc import Sequence
from typing import Self

from compas._typing import CoordinatesType
from compas.itertools import flatten
from compas.linalg.matrices import matrix_inverse
from compas.linalg.matrices import multiply_matrices
from compas.linalg.transformations import decompose_matrix
from compas.linalg.transformations import matrix_from_frame
from compas.linalg.transformations import matrix_from_scale_factors
from compas.tolerance import TOL

from .transformation import Matrix
from .transformation import Transformation


class Scale(Transformation):
    """Class representing a scale transformation.

    Parameters
    ----------
    matrix
        A 4x4 matrix (or similar) representing a scaling.
    check
        If `True`, the provided matrix will be checked for validity.
    name
        The name of the transformation.

    Raises
    ------
    ValueError
        If `check` is `True` and the provided transformation matrix is not a scale matrix.

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

    # ==========================================================================
    # Dunder methods
    # ==========================================================================

    def __init__(self, matrix: Matrix | None = None, check: bool = False, name: str | None = None) -> None:
        if matrix and check:
            scale, _, _, _, _ = decompose_matrix(matrix)
            if not TOL.is_allclose(flatten(matrix), flatten(matrix_from_scale_factors(scale))):
                raise ValueError("This is not a proper scale matrix.")
        super().__init__(matrix=matrix, name=name)

    # ==========================================================================
    # Constructors
    # ==========================================================================

    @classmethod
    def from_factors(cls, factors: Sequence[float], frame: CoordinatesType | None = None) -> Self:
        """Construct a scale transformation from scale factors.

        Parameters
        ----------
        factors
            The scale factors along X, Y, Z.
        frame
            The anchor frame for the scaling transformation.

        Returns
        -------
        Self
            The constructed scale.

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
