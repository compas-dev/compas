from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import json


def dataclass_dataschema(cls):
    """Generate a JSON schema for a COMPAS object class.

    Parameters
    ----------
    cls : :class:`~compas.data.Data`
        The COMPAS object class.

    Returns
    -------
    dict
        The JSON schema.

    """
    return cls.DATASCHEMA


def dataclass_typeschema(cls):
    """Generate a JSON schema for the data type of a COMPAS object class.

    Parameters
    ----------
    cls : :class:`~compas.data.Data`
        The COMPAS object class.

    Returns
    -------
    dict
        The JSON schema.

    """
    return {
        "type": "string",
        "const": "{}/{}".format(".".join(cls.__module__.split(".")[:2]), cls.__name__),
    }


def dataclass_jsonschema(cls, filepath=None, draft=None):
    """Generate a JSON schema for a COMPAS object class.

    Parameters
    ----------
    cls : :class:`~compas.data.Data`
        The COMPAS object class.
    filepath : str, optional
        The path to the file where the schema should be saved.
    draft : str, optional
        The JSON schema draft to use.

    Returns
    -------
    dict
        The JSON schema.

    """
    import compas

    draft = draft or "https://json-schema.org/draft/2020-12/schema"

    schema = {
        "$schema": draft,
        "$id": "{}.json".format(cls.__name__),
        "$compas": "{}".format(compas.__version__),
        "type": "object",
        "properties": {
            "dtype": dataclass_typeschema(cls),
            "data": dataclass_dataschema(cls),
            "guid": {"type": "string", "format": "uuid"},
        },
        "required": ["dtype", "data"],
    }

    if filepath:
        with open(filepath, "w") as f:
            json.dump(schema, f, indent=4)

    return schema


def compas_jsonschema(dirname=None):
    """Generate a JSON schema for the COMPAS data model.

    Parameters
    ----------
    dirname : str, optional
        The path to the directory where the schemas should be saved.

    Returns
    -------
    list
        A list of JSON schemas.

    """
    schemas = []
    dataclasses = compas_datamodel()
    for cls in dataclasses:
        filepath = None
        if dirname:
            filepath = os.path.join(dirname, "{}.json".format(cls.__name__))
        schema = dataclass_jsonschema(cls, filepath=filepath)
        schemas.append(schema)
    return schemas


def compas_datamodel():
    """Find all classes in the COMPAS data model.

    Returns
    -------
    list

    """
    from collections import deque
    from compas.data import Data
    import compas.colors  # noqa: F401
    import compas.datastructures  # noqa: F401
    import compas.geometry  # noqa: F401

    tovisit = deque([Data])
    dataclasses = []

    while tovisit:
        cls = tovisit.popleft()
        dataclasses.append(cls)
        for subcls in cls.__subclasses__():
            tovisit.append(subcls)

    return dataclasses


# def validate_json(filepath, schema):
#     """Validates a JSON document with respect to a schema and return the JSON object instance if it is valid.

#     Parameters
#     ----------
#     filepath : path string | file-like object | URL string
#         The filepath of the JSON document.
#     schema : string
#         The JSON schema.

#     Raises
#     ------
#     jsonschema.exceptions.SchemaError
#         If the schema itself is invalid.
#     jsonschema.exceptions.ValidationError
#         If the document is invalid with respect to the schema.

#     Returns
#     -------
#     object
#         The JSON object contained in the document.

#     Examples
#     --------
#     >>> import compas
#     >>> from compas.geometry import Point
#     >>> compas.json_validate("data.json", Point)
#     {'dtype': 'compas.geometry.Point', 'data': {'x': 0.0, 'y': 0.0, 'z': 0.0}, 'guid': '00000000-0000-0000-0000-000000000000'}

#     """
#     import jsonschema
#     import jsonschema.exceptions

#     data = json_load(filepath)

#     try:
#         jsonschema.validate(data, schema)
#     except jsonschema.exceptions.SchemaError as e:
#         print("The provided schema is invalid:\n\n{}\n\n".format(schema))
#         raise e
#     except jsonschema.exceptions.ValidationError as e:
#         print(
#             "The provided JSON document is invalid compared to the provided schema:\n\n{}\n\n{}\n\n".format(
#                 schema, data
#             )
#         )
#         raise e

#     return data


# def validate_jsonstring(jsonstring, schema):
#     """Validate the data contained in the JSON string against the JSON data schema.

#     Parameters
#     ----------
#     jsonstring : str
#         The JSON string for validation.
#     schema : string
#         The JSON schema.

#     Raises
#     ------
#     jsonschema.exceptions.SchemaError
#         If the schema itself is invalid.
#     jsonschema.exceptions.ValidationError
#         If the document is invalid with respect to the schema.

#     Returns
#     -------
#     object
#         The JSON object contained in the string.

#     """
#     from jsonschema import Draft202012Validator

#     validator = Draft202012Validator(schema)  # type: ignore
#     jsondata = json.loads(jsonstring)
#     validator.validate(jsondata)
#     return jsondata


# def validate_jsondata(jsondata, schema):
#     """Validate the JSON data against the JSON data schema.

#     Parameters
#     ----------
#     jsondata : Any
#         The JSON data for validation.
#     schema : string
#         The JSON schema.

#     Raises
#     ------
#     jsonschema.exceptions.SchemaError
#         If the schema itself is invalid.
#     jsonschema.exceptions.ValidationError
#         If the document is invalid with respect to the schema.

#     Returns
#     -------
#     object
#         The JSON object contained in the data.

#     """
#     from jsonschema import Draft202012Validator

#     validator = Draft202012Validator(schema)  # type: ignore
#     validator.validate(jsondata)
#     return jsondata


# def validate_data(data, cls):
#     """Validate data against the data and json schemas of an object class.

#     Parameters
#     ----------
#     data : dict
#         The data representation of an object.
#     cls : Type[:class:`~compas.data.Data`]
#         The data object class.

#     Returns
#     -------
#     dict
#         The validated data dict.

#     Raises
#     ------
#     jsonschema.exceptions.ValidationError

#     """
#     from jsonschema import RefResolver, Draft7Validator
#     from jsonschema.exceptions import ValidationError

#     here = os.path.dirname(__file__)

#     schema_name = "{}.json".format(cls.__name__.lower())
#     schema_path = os.path.join(here, "schemas", schema_name)
#     with open(schema_path, "r") as fp:
#         schema = json.load(fp)

#     definitions_path = os.path.join(here, "schemas", "compas.json")
#     with open(definitions_path, "r") as fp:
#         definitions = json.load(fp)

#     resolver = RefResolver.from_schema(definitions)
#     validator = Draft7Validator(schema, resolver=resolver)

#     try:
#         validator.validate(data)
#     except ValidationError as e:
#         print("Validation against the JSON schema of this object failed.")
#         raise e

#     return json.loads(json.dumps(data, cls=DataEncoder), cls=DataDecoder)
