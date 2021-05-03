"""
********************************************************************************
data
********************************************************************************

.. currentmodule:: compas.data

Classes
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Data
    DataEncoder
    DataDecoder


Functions
=========

.. autosummary::
    :toctree: generated/
    :nosignatures:

    json_load
    json_loads
    json_dump
    json_dumps

"""
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from .encoders import DataEncoder
from .encoders import DataDecoder
from .data import Data

from .json import json_load, json_loads, json_dump, json_dumps

__all__ = [
    'Data',
    'DataEncoder',
    'DataDecoder',
    'json_load',
    'json_loads',
    'json_dump',
    'json_dumps'
]
