
********************************************************************************
compas.data
********************************************************************************

.. currentmodule:: compas.data

.. rst-class:: lead

This package defines the core infrastructure for data serialisation in the COMPAS framework.
It provides a base class for data objects, a JSON encoder and decoder, serialisers and deserialisers, and schema validation.


Classes
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Data
    DataDecoder
    DataEncoder
    DecoderError


Functions
=========

.. autosummary::
    :toctree: generated/
    :nosignatures:

    compas_dataclasses
    dataclass_dataschema
    dataclass_jsonschema
    dataclass_typeschema
    json_dump
    json_dumps
    json_load
    json_loads
