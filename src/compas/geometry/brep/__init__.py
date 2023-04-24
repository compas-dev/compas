from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from .brep import Brep  # noqa: F401
from .brep import BrepOrientation  # noqa: F401
from .brep import BrepType  # noqa: F401
from .edge import BrepEdge  # noqa: F401
from .loop import BrepLoop  # noqa: F401
from .face import BrepFace  # noqa: F401
from .vertex import BrepVertex  # noqa: F401
from .trim import BrepTrim  # noqa: F401
from .trim import BrepTrimIsoStatus  # noqa: F401


class BrepError(Exception):
    """Represents a generic error in the Brep context"""

    pass


class BrepInvalidError(BrepError):
    """Raised when the process of re-constructing a Brep has resulted in an invalid Brep"""

    pass


class BrepTrimmingError(BrepError):
    """Raised when a trimming operation has failed or had not result"""

    pass
