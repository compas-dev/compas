from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from .curve import Curve


class Conic(Curve):
    """Base class for curves that are conic sections."""

    # overwriting the __new__ method is necessary
    # to avoid triggering the plugin mechanism of the base curve class
    def __new__(cls, *args, **kwargs):
        curve = object.__new__(cls)
        curve.__init__(*args, **kwargs)
        return curve
