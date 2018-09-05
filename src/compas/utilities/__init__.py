"""
********************************************************************************
compas.utilities
********************************************************************************

.. currentmodule:: compas.utilities


animation
=========

.. autosummary::
    :toctree: generated/
    :nosignatures:

    gif_from_images


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


datetime
========

.. autosummary::
    :toctree: generated/
    :nosignatures:


.. timestamp


decorators
==========

.. autosummary::
    :toctree: generated/
    :nosignatures:

    memoize


itertools
=========

.. autosummary::
    :toctree: generated/
    :nosignatures:

    take
    tabulate
    tail
    consume
    nth
    all_equal
    quantify
    padnone
    ncycles
    dotproduct
    flatten
    repeatfunc
    pairwise
    window
    roundrobin
    powerset
    unique_everseen
    unique_justseen
    iter_except
    first_true
    random_permutation
    random_combination
    random_combination_with_replacement


maps
====

.. autosummary::
    :toctree: generated/
    :nosignatures:

    geometric_key
    geometric_key2
    normalize_values


mixing
======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    mix_in_functions
    mix_in_class_attributes


names
=====

.. autosummary::
    :toctree: generated/
    :nosignatures:

    random_name


profiling
=========

.. autosummary::
    :toctree: generated/
    :nosignatures:

    print_profile


xfunc
=====

.. autosummary::
    :toctree: generated/
    :nosignatures:

    XFunc

"""
from __future__ import absolute_import


def valuedict(keys, value, default):
    value = value or default

    if isinstance(value, dict):
        valuedict = {key: default for key in keys}
        valuedict.update(value)
    else:
        valuedict = {key: value for key in keys}

    return valuedict


from .animation import *
from .coercing import *
from .colors import *
from .datetime_ import *
from .decorators import *
from .encoders import *
from .itertools_ import *
from .maps import *
from .mixing import *
from .names import *
from .profiling import *
from .remote import *
from .sorting import *
from .xfunc import *
from .xscript import *
from .functions import *

from . import animation
from . import coercing
from . import colors
from . import datetime_
from . import decorators
from . import encoders
from . import itertools_
from . import maps
from . import mixing
from . import names
from . import profiling
from . import remote
from . import sorting
from . import xfunc
from . import xscript
from . import functions

__all__  = []
__all__ += animation.__all__ + coercing.__all__ + colors.__all__
__all__ += datetime_.__all__ + decorators.__all__ + encoders.__all__
__all__ += itertools_.__all__ + maps.__all__ + mixing.__all__ + names.__all__
__all__ += profiling.__all__ + remote.__all__ + sorting.__all__
__all__ += xfunc.__all__ + xscript.__all__
__all__ += functions.__all__
