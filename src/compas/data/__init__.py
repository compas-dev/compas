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


Validators
==========

.. autosummary::
    :toctree: generated/
    :nosignatures:

    is_int3
    is_float3
    is_float4x4

"""
from __future__ import absolute_import

from .validators import is_int3
from .validators import is_float3
from .validators import is_float4x4
from .encoders import DataEncoder
from .encoders import DataDecoder
from .data import Data

from .json import json_load, json_loads, json_dump, json_dumps

__all__ = [
    'Data',
    'DataEncoder',
    'DataDecoder',
    'is_int3',
    'is_float3',
    'is_float4x4',
    'json_load',
    'json_loads',
    'json_dump',
    'json_dumps'
]
