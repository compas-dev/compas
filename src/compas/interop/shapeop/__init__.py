from __future__ import print_function

__all__ = []

try:
    from compas.interop.shapeop._shapeop import *
    from compas.interop.shapeop._shapeop import __all__
except ImportError:
    try:
        from compas.interop.shapeop._shapeop_windows import *
        from compas.interop.shapeop._shapeop_windows import __all__
    except ImportError:
        raise
