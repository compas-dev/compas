"""
********************************************************************************
colors
********************************************************************************

.. currentmodule:: compas.colors

.. rst-class:: lead

This package provides a class for working with colors in different color spaces,
and color maps for various color palettes.


Classes
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Color
    ColorMap

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from .color import Color
from .colormap import ColorMap

__all__ = ["Color", "ColorMap"]
