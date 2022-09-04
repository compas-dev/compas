"""
********************************************************************************
data
********************************************************************************

.. currentmodule:: compas.data

.. rst-class:: lead

This package provides a base data class for all COMPAS data objects such as geometry objects, robots, and data structures,
and the infrastructure for data validation, conversion, coercion, and JSON serialisation.


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

    is_sequence_of_int
    is_sequence_of_uint
    is_sequence_of_float
    is_int3
    is_float3
    is_float4x4
    validate_data


Exceptions
==========

.. autosummary::
    :toctree: generated/
    :nosignatures:

    DecoderError

"""
from __future__ import absolute_import

from .exceptions import DecoderError
from .validators import is_sequence_of_int
from .validators import is_sequence_of_uint
from .validators import is_sequence_of_float
from .validators import is_int3
from .validators import is_float3
from .validators import is_float4x4
from .validators import validate_data
from .encoders import DataEncoder
from .encoders import DataDecoder
from .data import Data

from .json import json_load, json_loads, json_dump, json_dumps

__all__ = [
    "Data",
    "DataEncoder",
    "DataDecoder",
    "DecoderError",
    "is_sequence_of_int",
    "is_sequence_of_uint",
    "is_sequence_of_float",
    "is_int3",
    "is_float3",
    "is_float4x4",
    "json_load",
    "json_loads",
    "json_dump",
    "json_dumps",
    "validate_data",
]
