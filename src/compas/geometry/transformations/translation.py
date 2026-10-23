from typing import TYPE_CHECKING
from typing import Self

from compas._typing import CoordinateType
from compas.itertools import flatten
from compas.linalg.transformations import matrix_from_translation
from compas.linalg.transformations import translation_from_matrix
from compas.tolerance import TOL

from .transformation import Matrix
from .transformation import Transformation

if TYPE_CHECKING:
    from compas.geometry import Vector


class Translation(Transformation):
    """Class representing a translation transformation.

    Parameters
    ----------
    matrix
        A 4x4 matrix (or similar) representing a translation.
    check
        If `True`, the provided matrix will be checked for validity.
    name
        The name of the transformation.

    Raises
    ------
    ValueError
        If `check` is `True` and the provided transformation matrix is not a translation.

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

    # ==========================================================================
    # Dunder methods
    # ==========================================================================

    def __init__(self, matrix: Matrix | None = None, check: bool = False, name: str | None = None) -> None:
        if matrix and check:
            translation = translation_from_matrix(matrix)
            if not TOL.is_allclose(flatten(matrix), flatten(matrix_from_translation(translation))):
                raise ValueError("This is not a proper translation matrix.")
        super().__init__(matrix=matrix, name=name)

    # ==========================================================================
    # Properties
    # ==========================================================================

    @property
    def translation_vector(self) -> "Vector":
        """The translation component as a vector."""
        from compas.geometry import Vector

        x = self.matrix[0][3]
        y = self.matrix[1][3]
        z = self.matrix[2][3]
        return Vector(x, y, z)

    # ==========================================================================
    # Constructors
    # ==========================================================================

    @classmethod
    def from_vector(cls, vector: CoordinateType) -> Self:
        """Construct a translation transformation from a vector.

        Parameters
        ----------
        vector
            The translation vector.

        Returns
        -------
        Self
            The constructed translation.

        Examples
        --------
        >>> translation = Translation.from_vector([1.0, 2.0, 3.0])
        >>> translation.translation_vector
        Vector(x=1.000, y=2.000, z=3.000)

        """
        matrix = matrix_from_translation(vector)
        return cls(matrix)
