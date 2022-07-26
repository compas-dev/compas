from .brep import Brep
from .edge import BrepEdge
from .loop import BrepLoop
from .face import BrepFace
from .vertex import BrepVertex


class BrepError(Exception):
    """Represents a generic error in the Brep context"""
    pass


class BrepInvalidError(BrepError):
    """Raised when the process of re-constructing a Brep has resulted in an invalid Brep"""
    pass


class BrepTrimmingError(BrepError):
    """Raised when a trimming operation has failed or had not result"""
    pass


__all__ = [
    "Brep",
    "BrepEdge",
    "BrepLoop",
    "BrepFace",
    "BrepVertex",

    "BrepError",
    "BrepInvalidError",
    "BrepTrimmingError",
]
