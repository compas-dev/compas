"""
********************************************************************************
interop
********************************************************************************

.. currentmodule:: compas_rhino.interop

.. rst-class:: lead

Conversions between Rhino geometry objects (:mod:`Rhino.Geometry`) and COMPAS geometry objects (:mod:`compas.geometry`).

Primitives
==========

.. autosummary::
    :toctree: generated/
    :nosignatures:

    compas_to_rhino_point
    compas_to_rhino_vector
    compas_to_rhino_line
    compas_to_rhino_plane
    compas_frame_to_rhino_vector
    compas_to_rhino_circle
    rhino_to_compas_point
    rhino_to_compas_vector
    rhino_to_compas_line
    rhino_to_compas_plane
    rhino_frame_to_compas_plane
    rhino_to_compas_circle

"""
from __future__ import absolute_import

from .primitives import (
    compas_to_rhino_point,
    compas_to_rhino_vector,
    compas_to_rhino_line,
    compas_to_rhino_plane,
    compas_frame_to_rhino_vector,
    compas_to_rhino_circle,
    rhino_to_compas_point,
    rhino_to_compas_vector,
    rhino_to_compas_line,
    rhino_to_compas_plane,
    rhino_frame_to_compas_plane,
    rhino_to_compas_circle,
)

# geometry to geometry conversions
# Rhino object to geometry conversions
# wrapper functions should be move to base classes in compas and receive an implementation via the plugin mechanism

__all__ = [
    'compas_to_rhino_point',
    'compas_to_rhino_vector',
    'compas_to_rhino_line',
    'compas_to_rhino_plane',
    'compas_frame_to_rhino_vector',
    'compas_to_rhino_circle',
    'rhino_to_compas_point',
    'rhino_to_compas_vector',
    'rhino_to_compas_line',
    'rhino_to_compas_plane',
    'rhino_frame_to_compas_plane',
    'rhino_to_compas_circle',
]
