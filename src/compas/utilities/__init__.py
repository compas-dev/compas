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
from __future__ import division
from __future__ import print_function

from .azync import *  # noqa: F401 F403
from .coercing import *  # noqa: F401 F403
from .colors import *  # noqa: F401 F403
from .datetime import *  # noqa: F401 F403
from .decorators import *  # noqa: F401 F403
from .descriptors import *  # noqa: F401 F403
from .encoders import *  # noqa: F401 F403
from .images import *  # noqa: F401 F403
from .itertools import *  # noqa: F401 F403
from .maps import *  # noqa: F401 F403
from .remote import *  # noqa: F401 F403
from .ssh import *  # noqa: F401 F403
from .xfunc import *  # noqa: F401 F403


__all__ = [name for name in dir() if not name.startswith('_')]
