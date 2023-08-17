import compas
from compas.data import Data
from compas.data import compas_dataclasses
from compas.data import dataclass_dataschema
from compas.data import dataclass_typeschema
from compas.data import dataclass_jsonschema


def test_schema_dataclasses():
    for cls in compas_dataclasses():
        assert issubclass(cls, Data)


def test_schema_dataclasses_typeschema():
    for cls in compas_dataclasses():
        dtype = dataclass_typeschema(cls)
        modname, clsname = dtype["const"].split("/")  # type: ignore
        assert cls.__name__ == clsname
        # module = __import__(modname, fromlist=[clsname])
        # assert hasattr(module, clsname)
        # assert getattr(module, clsname) == cls


def test_schema_dataclasses_dataschema():
    for cls in compas_dataclasses():
        assert dataclass_dataschema(cls) == cls.DATASCHEMA


def test_schema_dataclasses_jsonschema():
    for cls in compas_dataclasses():
        schema = dataclass_jsonschema(cls)
        assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
        assert schema["$id"] == "{}.json".format(cls.__name__)
        assert schema["$compas"] == "{}".format(compas.__version__)
        assert schema["type"] == "object"
        assert schema["properties"]["dtype"] == dataclass_typeschema(cls)
        assert schema["properties"]["data"] == dataclass_dataschema(cls)
