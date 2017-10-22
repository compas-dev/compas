"""
.. _compas.utilities:

********************************************************************************
utilities
********************************************************************************

.. module:: compas.utilities


.. combine all decorators
.. combine xscript and xfunc into xrun


animation
=========

.. autosummary::
    :toctree: generated/

    gif_from_images


colors
======

.. autosummary::
    :toctree: generated/

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

    timestamp


itertools
=========

.. autosummary::
    :toctree: generated/

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

    geometric_key
    geometric_key2


mixing
======

.. autosummary::
    :toctree: generated/

    mix_in_functions
    mix_in_class_attributes


names
=====

.. autosummary::
    :toctree: generated/

    random_name


profiling
=========

.. autosummary::
    :toctree: generated/

    print_profile


scripts
=======

.. autosummary::
    :toctree: generated/

    ScriptServer


xfunc
=====

.. autosummary::
    :toctree: generated/

    XFunc


"""


def is_list_of_int():
    pass


def is_list_of_float():
    pass


def is_list_of_str():
    pass


def is_list_of_list():
    pass


def is_list_of_dict():
    pass


def to_valuedict(keys, value, default):
    value = value or default

    if isinstance(value, dict):
        valuedict = {key: default for key in keys}
        valuedict.update(value)
    else:
        valuedict = {key: value for key in keys}

    return valuedict


from .animation import *
from .datetime_ import *
from .itertools_ import *
from .colors import *
from .maps import *
from .mixing import *
from .names import *
from .profiling import *
from .sorting import *
from .xfunc import *
from .xscript import *

from .animation import __all__ as a
from .datetime_ import __all__ as b
from .itertools_ import __all__ as c
from .colors import __all__ as d
from .maps import __all__ as e
from .mixing import __all__ as f
from .names import __all__ as g
from .profiling import __all__ as h
from .sorting import __all__ as i
from .xfunc import __all__ as j
from .xscript import __all__ as k

__all__ = a + b + c + d + e + f + g + h + i + j + k
