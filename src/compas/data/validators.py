from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os
import json

from compas.data.encoders import DataEncoder
from compas.data.encoders import DataDecoder


def is_int3(items):
    return len(items) == 3 and all(isinstance(item, int) for item in items)


def is_float3(items):
    return len(items) == 3 and all(isinstance(item, float) for item in items)


def is_float4x4(items):
    return (
        len(items) == 4 and
        all(
            len(item) == 4 and
            all(isinstance(i, float) for i in item) for item in items
        )
    )


def validate_data(data, cls):
    """Validate data against the data and json schemas of an object class.

    Parameters
    ----------
    data : dict
        The data representation of an object.
    cls : :class:`compas.data.Data`
        The class of a data object.

    Returns
    -------
    dict
        The validated data.

    Raises
    ------
    SchemaError
    """
    from jsonschema import RefResolver, Draft7Validator

    here = os.path.dirname(__file__)

    schema_name = '{}.json'.format(cls.__name__.lower())
    schema_path = os.path.join(here, 'schemas', schema_name)
    with open(schema_path, 'r') as fp:
        schema = json.load(fp)

    definitions_path = os.path.join(here, 'schemas', 'compas.json')
    with open(definitions_path, 'r') as fp:
        definitions = json.load(fp)

    resolver = RefResolver.from_schema(definitions)
    validator = Draft7Validator(schema, resolver=resolver)
    validator.validate(data)

    return json.loads(json.dumps(data, cls=DataEncoder), cls=DataDecoder)
