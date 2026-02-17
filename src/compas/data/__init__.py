"""
This package defines the core infrastructure for data serialisation in the COMPAS framework.
It provides a base class for data objects, a JSON encoder and decoder, serialisers and deserialisers, and schema validation.
"""
# ruff: noqa: F401

from .exceptions import DecoderError
from .encoders import DataEncoder
from .encoders import DataDecoder
from .data import Data
from .json import json_load, json_loads, json_loadz, json_dump, json_dumps, json_dumpz
from .schema import dataclass_dataschema, dataclass_typeschema, dataclass_jsonschema
from .schema import compas_dataclasses
