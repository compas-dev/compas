from .brep import Brep
from .edge import BrepEdge
from .loop import BrepLoop
from .face import BrepFace
from .vertex import BrepVertex


class BrepError(Exception):
    pass


class BrepInvalidError(BrepError):
    pass


__all__ = [
    "Brep",
    "BrepEdge",
    "BrepLoop",
    "BrepFace",
    "BrepVertex",
    "BrepError",
    "BrepInvalidError",
]
