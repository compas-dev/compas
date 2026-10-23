from typing import Self

from compas._typing import CoordinatesType
from compas.itertools import flatten
from compas.linalg.transformations import decompose_matrix
from compas.linalg.transformations import identity_matrix
from compas.linalg.transformations import matrix_from_perspective_entries
from compas.linalg.vectors import cross_vectors
from compas.linalg.vectors import dot_vectors
from compas.linalg.vectors import normalize_vector
from compas.tolerance import TOL

from .transformation import Matrix
from .transformation import Transformation


class Reflection(Transformation):
    """Class representing a reflection transformation.

    A reflection transformation mirrors points at a plane.

    Parameters
    ----------
    matrix
        A 4x4 matrix (or similar) representing a reflection.
    check
        If `True`, the provided matrix will be checked for validity.
    name
        The name of the transformation.

    Raises
    ------
    ValueError
        If `check` is `True` and the provided transformation matrix is not a reflection.

    Examples
    --------
    >>> point = [1, 1, 1]
    >>> normal = [0, 0, 1]
    >>> R1 = Reflection.from_plane((point, normal))
    >>> R2 = Transformation([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, -1, 2], [0, 0, 0, 1]])
    >>> R1 == R2
    True

    """

    # ==========================================================================
    # Dunder methods
    # ==========================================================================

    def __init__(self, matrix: Matrix | None = None, check: bool = False, name: str | None = None) -> None:
        if matrix and check:
            _, _, _, _, perspective = decompose_matrix(matrix)
            if not TOL.is_allclose(flatten(matrix), flatten(matrix_from_perspective_entries(perspective))):
                raise ValueError("This is not a proper reflection matrix.")
        super().__init__(matrix=matrix, name=name)

    # ==========================================================================
    # Constructors
    # ==========================================================================

    @classmethod
    def from_plane(cls, plane: CoordinatesType) -> Self:
        """Construct a reflection transformation across a plane.

        Parameters
        ----------
        plane
            The reflection plane.

        Returns
        -------
        Self
            The constructed reflection.

        Examples
        --------
        >>> reflection = Reflection.from_plane(((0, 0, 0), (0, 0, 1)))
        >>> reflection[2, 2]
        -1.0

        """
        point, normal = plane
        normal = normalize_vector(normal)
        matrix = identity_matrix(4)
        for i in range(3):
            for j in range(3):
                matrix[i][j] -= 2.0 * normal[i] * normal[j]
        for i in range(3):
            matrix[i][3] = 2 * dot_vectors(point, normal) * normal[i]
        return cls(matrix)

    @classmethod
    def from_frame(cls, frame: CoordinatesType) -> Self:
        """Construct a reflection transformation across a frame's XY plane.

        Parameters
        ----------
        frame
            The frame defining the reflection plane.

        Returns
        -------
        Self
            The constructed reflection.

        Examples
        --------
        >>> from compas.geometry import Frame
        >>> reflection = Reflection.from_frame(Frame.worldXY())
        >>> reflection[2, 2]
        -1.0

        """
        point, xaxis, yaxis = frame
        zaxis = cross_vectors(xaxis, yaxis)
        return cls.from_plane((point, zaxis))
