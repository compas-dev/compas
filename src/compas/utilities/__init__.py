"""
********************************************************************************
utilities
********************************************************************************

.. currentmodule:: compas.utilities


async
=====

.. autosummary::
    :toctree: generated/
    :nosignatures:

    await_callback


colors
======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    i_to_rgb
    i_to_red
    i_to_green
    i_to_blue
    i_to_white
    i_to_black
    rgb_to_hex
    color_to_colordict
    color_to_rgb


encoders
========

.. autosummary::
    :toctree: generated/
    :nosignatures:

    DataEncoder
    DataDecoder


itertools
=========

.. autosummary::
    :toctree: generated/
    :nosignatures:

    flatten
    linspace
    meshgrid
    pairwise
    window
    iterable_like
    normalize_values
    remap_values


maps
====

.. autosummary::
    :toctree: generated/
    :nosignatures:

    geometric_key
    reverse_geometric_key
    geometric_key_xy


"""
from __future__ import absolute_import

from .azync import await_callback
from .coercing import (
    coerce_sequence_of_list,
    coerce_sequence_of_tuple,
    is_item_iterable,
    is_sequence_of_dict,
    is_sequence_of_float,
    is_sequence_of_int,
    is_sequence_of_iterable,
    is_sequence_of_list,
    is_sequence_of_str,
    is_sequence_of_tuple
)
from .colors import (
    Colormap,
    black,
    blue,
    color_to_colordict,
    color_to_rgb,
    cyan,
    green,
    hex_to_rgb,
    i_to_black,
    i_to_blue,
    i_to_green,
    i_to_red,
    i_to_rgb,
    i_to_white,
    is_color_hex,
    is_color_light,
    is_color_rgb,
    red,
    rgb_to_hex,
    rgb_to_rgb,
    white,
    yellow
)
from .datetime import (
    now,
    timestamp
)
from .decorators import (
    abstractclassmethod,
    abstractstaticmethod,
    memoize,
    print_profile
)
from .descriptors import (
    Float,
    RGBColour
)
from .encoders import (
    DataDecoder,
    DataEncoder
)
from .images import gif_from_images
from .itertools import (
    flatten,
    grouper,
    iterable_like,
    linspace,
    meshgrid,
    normalize_values,
    pairwise,
    remap_values,
    window
)
from .maps import (
    geometric_key,
    geometric_key_xy,
    reverse_geometric_key
)
from .remote import download_file_from_remote
from .ssh import SSH
from .xfunc import XFunc

__all__ = [
    'await_callback',
    'is_sequence_of_str',
    'is_sequence_of_int',
    'is_sequence_of_float',
    'is_sequence_of_tuple',
    'is_sequence_of_list',
    'is_sequence_of_dict',
    'is_sequence_of_iterable',
    'is_item_iterable',
    'coerce_sequence_of_tuple',
    'coerce_sequence_of_list',
    'i_to_rgb',
    'i_to_red',
    'i_to_green',
    'i_to_blue',
    'i_to_white',
    'i_to_black',
    'is_color_rgb',
    'is_color_hex',
    'is_color_light',
    'rgb_to_hex',
    'rgb_to_rgb',
    'hex_to_rgb',
    'color_to_colordict',
    'color_to_rgb',
    'Colormap',
    'red',
    'green',
    'blue',
    'yellow',
    'cyan',
    'white',
    'black',
    'timestamp',
    'now',
    'abstractstaticmethod',
    'abstractclassmethod',
    'memoize',
    'print_profile',
    'Float',
    'RGBColour',
    'DataDecoder',
    'DataEncoder',
    'gif_from_images',
    'normalize_values',
    'remap_values',
    'meshgrid',
    'linspace',
    'flatten',
    'pairwise',
    'window',
    'iterable_like',
    'grouper',
    'geometric_key',
    'reverse_geometric_key',
    'geometric_key_xy',
    'download_file_from_remote',
    'SSH',
    'XFunc'
]
