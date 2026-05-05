import json
import os
from typing import Any
from typing import Optional
from typing import Type
from typing import Union

from .data import Data

JSONFile = Union[str, os.PathLike[str]]


def dataclass_dataschema(cls: Type[Data]) -> dict[str, Any]:
    """Generate a JSON schema for a COMPAS object class.

    Parameters
    ----------
    cls
        The COMPAS object class.

    Returns
    -------
    dict
        The JSON schema.

    """
    return cls.DATASCHEMA


def dataclass_typeschema(cls: Type[Data]) -> dict[str, Any]:
    """Generate a JSON schema for the data type of a COMPAS object class.

    Parameters
    ----------
    cls
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


def dataclass_jsonschema(cls: Type[Data], filepath: Optional[JSONFile] = None, draft: Optional[str] = None) -> dict[str, Any]:
    """Generate a JSON schema for a COMPAS object class.

    Parameters
    ----------
    cls
        The COMPAS object class.
    filepath
        The path to the file where the schema should be saved.
    draft
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


def compas_jsonschema(dirname: Optional[JSONFile] = None) -> list[dict[str, Any]]:
    """Generate a JSON schema for the COMPAS data model.

    Parameters
    ----------
    dirname
        The path to the directory where the schemas should be saved.

    Returns
    -------
    list
        A list of JSON schemas.

    """
    schemas: list[dict[str, Any]] = []
    dataclasses = compas_dataclasses()
    for cls in dataclasses:
        filepath = None
        if dirname:
            filepath = os.path.join(dirname, "{}.json".format(cls.__name__))
        schema = dataclass_jsonschema(cls, filepath=filepath)
        schemas.append(schema)
    return schemas


def compas_dataclasses() -> list[Type[Data]]:
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
    dataclasses: list[Type[Data]] = []

    while tovisit:
        cls = tovisit.popleft()
        dataclasses.append(cls)
        for subcls in cls.__subclasses__():
            tovisit.append(subcls)

    return dataclasses
