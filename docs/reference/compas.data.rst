********************************************************************************
compas.data
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
    is_item_iterable


Exceptions
==========

.. autosummary::
    :toctree: generated/
    :nosignatures:

    DecoderError

