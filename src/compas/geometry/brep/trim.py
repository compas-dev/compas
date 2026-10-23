from typing import TYPE_CHECKING
from typing import Any
from typing import Literal

from compas.data import Data

if TYPE_CHECKING:
    from compas.geometry import BrepVertex
    from compas.geometry import NurbsCurve


class BrepTrimIsoStatus:
    """Isoparametric direction of a trim on its surface."""

    NONE = 0
    X = 1
    Y = 2
    WEST = 3
    SOUTH = 4
    EAST = 5
    NORTH = 6


class BrepTrim(Data):
    """Interface for a parametric trimming curve of a Brep face."""

    # ==========================================================================
    # Properties
    # ==========================================================================

    @property
    def curve(self) -> "NurbsCurve":
        """The two-dimensional NURBS curve in the surface parameter space."""
        raise NotImplementedError

    @property
    def iso_status(self) -> Literal[0, 1, 2, 3, 4, 5, 6]:
        """The isoparametric direction as a `BrepTrimIsoStatus` value."""
        raise NotImplementedError

    @property
    def is_reversed(self) -> bool:
        """Whether the trim runs opposite to its associated edge curve."""
        raise NotImplementedError

    @property
    def native_trim(self) -> Any:
        """The backend-specific trim object."""
        raise NotImplementedError

    @property
    def start_vertex(self) -> "BrepVertex":
        """The start vertex of the trim."""
        raise NotImplementedError

    @property
    def end_vertex(self) -> "BrepVertex":
        """The end vertex of the trim."""
        raise NotImplementedError

    @property
    def vertices(self) -> list["BrepVertex"]:
        """The start and end vertices of the trim."""
        raise NotImplementedError
