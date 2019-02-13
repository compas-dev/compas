"""
********************************************************************************
utilities
********************************************************************************

.. currentmodule:: compas.utilities


animation
=========

.. autosummary::
    :toctree: generated/
    :nosignatures:

    gif_from_images


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

functions
==========

.. autosummary::
    :toctree: generated/
    :nosignatures:

    fibonacci
    binomial_coefficient

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
    reverse_geometric_key
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


statistics
==========

.. autosummary::
    :toctree: generated/
    :nosignatures:

    average
    variance
    standard_deviation


xfunc
=====

.. autosummary::
    :toctree: generated/
    :nosignatures:

    XFunc

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


def valuedict(keys, value, default):
    value = value or default
    if isinstance(value, dict):
        valuedict = {key: default for key in keys}
        valuedict.update(value)
    else:
        valuedict = {key: value for key in keys}
    return valuedict


from .animation import *
from .async_ import *
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
from .statistics import *

__all__ = [name for name in dir() if not name.startswith('_')]
