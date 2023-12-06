"""
This package defines a color and color map class,
that can be used to work wihth colors in a consistent way across color spaces.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from .color import Color
from .colormap import ColorMap
from .colordict import ColorDict

__all__ = ["Color", "ColorMap", "ColorDict"]
