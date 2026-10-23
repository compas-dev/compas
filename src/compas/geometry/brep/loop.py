from collections.abc import Sequence
from typing import TYPE_CHECKING
from typing import Any
from typing import Self

from compas.data import Data

if TYPE_CHECKING:
    from compas.geometry import BrepEdge
    from compas.geometry import BrepVertex
    from compas.geometry import Polygon
    from compas.geometry import Polyline


class BrepLoop(Data):
    """Interface for a closed sequence of Brep edges."""

    # ==========================================================================
    # Properties
    # ==========================================================================

    @property
    def is_valid(self) -> bool:
        """Whether the loop is valid.

        Raises
        ------
        NotImplementedError
            If the active Brep backend does not implement loop validation.

        """
        raise NotImplementedError

    @property
    def vertices(self) -> list["BrepVertex"]:
        """The ordered vertices of the loop."""
        raise NotImplementedError

    @property
    def edges(self) -> list["BrepEdge"]:
        """The ordered edges of the loop."""
        raise NotImplementedError

    @property
    def native_loop(self) -> Any:
        """The backend-specific loop object."""
        raise NotImplementedError

    # ==========================================================================
    # Constructors
    # ==========================================================================

    @classmethod
    def from_edges(cls, edges: Sequence["BrepEdge"]) -> Self:
        """Construct a loop from ordered edges.

        Parameters
        ----------
        edges
            The ordered edges of the loop.

        Returns
        -------
        Self
            The constructed loop.

        """
        raise NotImplementedError

    @classmethod
    def from_polyline(cls, polyline: "Polyline") -> Self:
        """Construct a loop from a closed polyline.

        Parameters
        ----------
        polyline
            The closed polyline.

        Returns
        -------
        Self
            The constructed loop.

        """
        raise NotImplementedError

    @classmethod
    def from_polygon(cls, polygon: "Polygon") -> Self:
        """Construct a loop from a polygon.

        Parameters
        ----------
        polygon
            The polygon.

        Returns
        -------
        Self
            The constructed loop.

        """
        raise NotImplementedError
