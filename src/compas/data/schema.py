from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
import os


def dataclass_dataschema(cls):  # type: (...) -> dict
    """Generate a JSON schema for a COMPAS object class.

    Parameters
    ----------
    cls : :class:`compas.data.Data`
        The COMPAS object class.

    Returns
    -------
    dict
        The JSON schema.

    """
    return cls.DATASCHEMA


def dataclass_typeschema(cls):  # type: (...) -> dict
    """Generate a JSON schema for the data type of a COMPAS object class.

    Parameters
    ----------
    cls : :class:`compas.data.Data`
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


def dataclass_jsonschema(cls, filepath=None, draft=None):  # type: (...) -> dict
    """Generate a JSON schema for a COMPAS object class.

    Parameters
    ----------
    cls : :class:`compas.data.Data`
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


def compas_jsonschema(dirname=None):  # type: (...) -> list
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
    dataclasses = compas_dataclasses()
    for cls in dataclasses:
        filepath = None
        if dirname:
            filepath = os.path.join(dirname, "{}.json".format(cls.__name__))
        schema = dataclass_jsonschema(cls, filepath=filepath)
        schemas.append(schema)
    return schemas


def compas_dataclasses():  # type: (...) -> list
    """Find all classes in the COMPAS data model.

    Returns
    -------
    list

    """
    from collections import deque

    import compas.colors  # noqa: F401
    import compas.datastructures  # noqa: F401
    import compas.geometry  # noqa: F401
    from compas.data import Data

    tovisit = deque([Data])
    dataclasses = []

    while tovisit:
        cls = tovisit.popleft()
        dataclasses.append(cls)
        for subcls in cls.__subclasses__():
            tovisit.append(subcls)

    return dataclasses
