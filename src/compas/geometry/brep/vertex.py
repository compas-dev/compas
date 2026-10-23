from typing import TYPE_CHECKING
from typing import Any
from typing import Self

from compas.data import Data

if TYPE_CHECKING:
    from compas.geometry import Point


class BrepVertex(Data):
    """Interface for a topological vertex of a boundary representation."""

    # ==========================================================================
    # Properties
    # ==========================================================================

    @property
    def point(self) -> "Point":
        """The geometric point of the vertex."""
        raise NotImplementedError

    @property
    def native_vertex(self) -> Any:
        """The backend-specific vertex object."""
        raise NotImplementedError

    # ==========================================================================
    # Constructors
    # ==========================================================================

    @classmethod
    def from_point(cls, point: "Point") -> Self:
        """Construct a Brep vertex from a point.

        Parameters
        ----------
        point
            The geometric point.

        Returns
        -------
        Self
            The constructed vertex.

        """
        raise NotImplementedError
