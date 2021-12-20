from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os
import json

from compas.data.encoders import DataEncoder
from compas.data.encoders import DataDecoder


def is_sequence_of_int(items):
    """Verify that the sequence contains only :obj:`int`.

    Parameters
    ----------
    items : iterable
        The sequence of items.

    Returns
    -------
    bool
    """
    return all(isinstance(item, int) for item in items)


def is_int3(items):
    """Verify that the sequence contains 3 :obj:`int`.

    Parameters
    ----------
    items : iterable
        The sequence of items.

    Returns
    -------
    bool
    """
    return len(items) == 3 and all(isinstance(item, int) for item in items)


def is_sequence_of_float(items):
    """Verify that the sequence contains only :obj:`float`.

    Parameters
    ----------
    items : iterable
        The sequence of items.

    Returns
    -------
    bool
    """
    return all(isinstance(item, float) for item in items)


def is_sequence_of_uint(items):
    """Verify that the sequence contains only unsigned :obj:`int`.

    Parameters
    ----------
    items : iterable
        The sequence of items.

    Returns
    -------
    bool
    """
    return all(isinstance(item, int) and item >= 0 for item in items)


def is_float3(items):
    """Verify that the sequence contains 3 :obj:`float`.

    Parameters
    ----------
    items : iterable
        The sequence of items.

    Returns
    -------
    bool
    """
    return len(items) == 3 and all(isinstance(item, float) for item in items)


def is_float4x4(items):
    """Verify that the sequence contains 4 sequences of each 4 :obj:`float`.

    Parameters
    ----------
    items : iterable
        The sequence of items.

    Returns
    -------
    bool
    """
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
    :class:`jsonschema.exceptions.ValidationError`
    """
    from jsonschema import RefResolver, Draft7Validator
    from jsonschema.exceptions import ValidationError

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

    try:
        validator.validate(data)
    except ValidationError as e:
        print("Validation against the JSON schema of this object failed.")
        raise e

    return json.loads(json.dumps(data, cls=DataEncoder), cls=DataDecoder)
