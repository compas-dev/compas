from collections.abc import Sequence
from typing import Self

from compas._typing import CoordinatesType
from compas._typing import CoordinateType
from compas.itertools import flatten
from compas.linalg.transformations import decompose_matrix
from compas.linalg.transformations import matrix_from_orthogonal_projection
from compas.linalg.transformations import matrix_from_parallel_projection
from compas.linalg.transformations import matrix_from_perspective_entries
from compas.linalg.transformations import matrix_from_perspective_projection
from compas.tolerance import TOL

from .transformation import Matrix
from .transformation import Transformation


class Projection(Transformation):
    """Class representing a projection transformation.

    Parameters
    ----------
    matrix
        A 4x4 matrix (or similar) representing a projection transformation.
    check
        If `True`, the provided matrix will be checked for validity.
    name
        The name of the transformation.

    Raises
    ------
    ValueError
        If `check` is `True` and the provided transformation matrix is not a projection matrix.

    """

    # ==========================================================================
    # Dunder methods
    # ==========================================================================

    def __init__(self, matrix: Matrix | None = None, check: bool = False, name: str | None = None) -> None:
        if matrix and check:
            _, _, _, _, perspective = decompose_matrix(matrix)
            if not TOL.is_allclose(flatten(matrix), flatten(matrix_from_perspective_entries(perspective))):
                raise ValueError("This is not a proper projection matrix.")
        super().__init__(matrix=matrix, name=name)

    # ==========================================================================
    # Constructors
    # ==========================================================================

    @classmethod
    def from_plane(cls, plane: CoordinatesType) -> Self:
        """Construct an orthogonal projection transformation to project onto a plane.

        Parameters
        ----------
        plane
            The plane to project onto.

        Returns
        -------
        Self
            The constructed orthogonal projection.

        Examples
        --------
        >>> from compas.geometry import Plane
        >>> point = [0, 0, 0]
        >>> normal = [0, 0, 1]
        >>> plane = Plane(point, normal)
        >>> P = Projection.from_plane(plane)

        """
        matrix = matrix_from_orthogonal_projection(plane)
        return cls(matrix)

    @classmethod
    def from_plane_and_direction(cls, plane: CoordinatesType, direction: CoordinateType) -> Self:
        """Construct a parallel projection transformation to project onto a plane along a specific direction.

        Parameters
        ----------
        plane
            The plane to project onto.
        direction
            The projection direction.

        Returns
        -------
        Self
            The constructed parallel projection.

        Examples
        --------
        >>> from compas.geometry import Plane
        >>> point = [0, 0, 0]
        >>> normal = [0, 0, 1]
        >>> plane = Plane(point, normal)
        >>> direction = [1, 1, 1]
        >>> P = Projection.from_plane_and_direction(plane, direction)

        """
        matrix = matrix_from_parallel_projection(plane, direction)
        return cls(matrix)

    @classmethod
    def from_plane_and_point(cls, plane: CoordinatesType, center_of_projection: CoordinateType) -> Self:
        """Construct a perspective projection transformation to project onto a plane along lines that emanate from a single point, called the center of projection.

        Parameters
        ----------
        plane
            The plane to project onto.
        center_of_projection
            The camera view point.

        Returns
        -------
        Self
            The constructed perspective projection.

        Examples
        --------
        >>> from compas.geometry import Plane
        >>> point = [0, 0, 0]
        >>> normal = [0, 0, 1]
        >>> plane = Plane(point, normal)
        >>> center_of_projection = [1, 1, 0]
        >>> P = Projection.from_plane_and_point(plane, center_of_projection)

        """
        matrix = matrix_from_perspective_projection(plane, center_of_projection)
        return cls(matrix)

    @classmethod
    def from_entries(cls, perspective_entries: Sequence[float]) -> Self:
        """Construct a perspective transformation from matrix entries.

        Parameters
        ----------
        perspective_entries
            The 4 perspective entries of a matrix.

        Returns
        -------
        Self
            The constructed projection.

        Examples
        --------
        >>> projection = Projection.from_entries([0.3, 0.1, 0.1, 1.0])
        >>> projection[3, 0]
        0.3

        """
        matrix = matrix_from_perspective_entries(perspective_entries)
        return cls(matrix)
