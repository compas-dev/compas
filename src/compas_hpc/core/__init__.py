
from .cuda import *
from .opencl import *

from .cuda import __all__ as a
from .opencl import __all__ as b

__all__ = a + b
