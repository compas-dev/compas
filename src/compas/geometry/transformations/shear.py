from collections.abc import Sequence
from typing import Self

from compas._typing import CoordinatesType
from compas._typing import CoordinateType
from compas.itertools import flatten
from compas.linalg.transformations import decompose_matrix
from compas.linalg.transformations import matrix_from_shear
from compas.linalg.transformations import matrix_from_shear_entries
from compas.tolerance import TOL

from .transformation import Matrix
from .transformation import Transformation


class Shear(Transformation):
    """Class representing a shear transformation.

    A point P is transformed by the shear matrix into P" such that
    the vector P-P" is parallel to the direction vector and its extent is
    given by the angle of P-P'-P", where P' is the orthogonal projection
    of P onto the shear plane.

    Parameters
    ----------
    matrix
        A 4x4 matrix (or similar) representing a shear transformation.
    check
        If `True`, the provided matrix will be checked for validity.
    name
        The name of the transformation.

    Raises
    ------
    ValueError
        If `check` is `True` and the provided transformation matrix is not a shear matrix.

    """

    # ==========================================================================
    # Dunder methods
    # ==========================================================================

    def __init__(self, matrix: Matrix | None = None, check: bool = False, name: str | None = None) -> None:
        if matrix and check:
            _, shear, _, _, _ = decompose_matrix(matrix)
            if not TOL.is_allclose(flatten(matrix), flatten(matrix_from_shear_entries(shear))):
                raise ValueError("This is not a proper shear matrix.")
        super().__init__(matrix=matrix, name=name)

    # ==========================================================================
    # Constructors
    # ==========================================================================

    @classmethod
    def from_angle_direction_plane(cls, angle: float, direction: CoordinateType, plane: CoordinatesType) -> Self:
        """Construct a shear transformation from an angle, direction and plane.

        Parameters
        ----------
        angle
            The angle in radians.
        direction
            The shear direction.
            It must be orthogonal to the normal vector (i.e. it must lie in the shear plane).
        plane
            The shear plane defined by a point and normal.

        Returns
        -------
        Self
            The constructed shear.

        Raises
        ------
        ValueError
            If the shear direction does not lie in the shear plane.

        Examples
        --------
        >>> from compas.linalg import cross_vectors
        >>> angle = 0.1
        >>> direction = [0.1, 0.2, 0.3]
        >>> point = [4, 3, 1]
        >>> normal = cross_vectors(direction, [1, 0.3, -0.1])
        >>> S = Shear.from_angle_direction_plane(angle, direction, (point, normal))

        """
        point, normal = plane
        matrix = matrix_from_shear(angle, direction, point, normal)
        return cls(matrix)

    @classmethod
    def from_entries(cls, shear_entries: Sequence[float]) -> Self:
        """Construct a shear transformation from the 3 factors for x-y, x-z, and y-z axes.

        Parameters
        ----------
        shear_entries
            The 3 shear factors for x-y, x-z, and y-z axes.

        Returns
        -------
        Self
            The constructed shear.

        Examples
        --------
        >>> S = Shear.from_entries([1, 2, 3])

        """
        matrix = matrix_from_shear_entries(shear_entries)
        return cls(matrix)
