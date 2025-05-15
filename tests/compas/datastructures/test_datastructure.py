import pytest
import compas
from compas.datastructures import Datastructure
from compas.datastructures import Mesh
from compas.data import json_dumps, json_loads


class Level1(Datastructure):
    def __init__(self, attributes=None, name=None):
        super(Level1, self).__init__(attributes=attributes, name=name)
        self.level1_attr = "level1"

    @property
    def __data__(self):
        return {"attributes": self.attributes, "level1_attr": self.level1_attr}

    @classmethod
    def __from_data__(cls, data):
        obj = cls(attributes=data.get("attributes"))
        obj.level1_attr = data.get("level1_attr", "")
        return obj


@pytest.fixture
def level2():
    # Level2 is a custom class that is not available outside of this local scope
    class Level2(Level1):
        def __init__(self, attributes=None, name=None):
            super(Level2, self).__init__(attributes=attributes, name=name)
            self.level2_attr = "level2"

        @property
        def __data__(self):
            data = super(Level2, self).__data__
            data["level2_attr"] = self.level2_attr
            return data

        @classmethod
        def __from_data__(cls, data):
            obj = super(Level2, cls).__from_data__(data)
            obj.level2_attr = data.get("level2_attr", "")
            return obj

    # return an instance of Level2
    return Level2(name="test")


@pytest.fixture
def level3():
    # Level2 and Level3 are custom classes that are not available outside of this local scope
    class Level2(Level1):
        def __init__(self, attributes=None, name=None):
            super(Level2, self).__init__(attributes=attributes, name=name)
            self.level2_attr = "level2"

        @property
        def __data__(self):
            data = super(Level2, self).__data__
            data["level2_attr"] = self.level2_attr
            return data

        @classmethod
        def __from_data__(cls, data):
            obj = super(Level2, cls).__from_data__(data)
            obj.level2_attr = data.get("level2_attr", "")
            return obj

    class Level3(Level2):
        def __init__(self, attributes=None, name=None):
            super(Level3, self).__init__(attributes=attributes, name=name)
            self.level3_attr = "level3"

        @property
        def __data__(self):
            data = super(Level3, self).__data__
            data["level3_attr"] = self.level3_attr
            return data

        @classmethod
        def __from_data__(cls, data):
            obj = super(Level3, cls).__from_data__(data)
            obj.level3_attr = data.get("level3_attr", "")
            return obj

    # return an instance of Level3
    return Level3(name="test")


@pytest.fixture
def custom_mesh():
    class CustomMesh(Mesh):
        def __init__(self, *args, **kwargs):
            super(CustomMesh, self).__init__(*args, **kwargs)
            self.custom_mesh_attr = "custom_mesh"

        @property
        def __data__(self):
            data = super(CustomMesh, self).__data__
            data["custom_mesh_attr"] = self.custom_mesh_attr
            return data

        @classmethod
        def __from_data__(cls, data):
            obj = super(CustomMesh, cls).__from_data__(data)
            obj.custom_mesh_attr = data.get("custom_mesh_attr", "")
            return obj

    return CustomMesh(name="test")


def test_inheritance_fallback(level2):
    if compas.IPY:
        # IronPython is not able to deserialize a class that is defined in a local scope like Level1.
        # We skip this tests for IronPython.
        return

    assert level2.__jsondump__()["dtype"] == "test_datastructure/Level2"
    # Level2 should serialize Level1 into the inheritance
    assert level2.__jsondump__()["inheritance"] == ["test_datastructure/Level1"]

    dumped = json_dumps(level2)
    loaded = json_loads(dumped)

    # The loaded object should be deserialized as the closes available class: Level1
    assert loaded.__class__ == Level1
    assert loaded.__jsondump__()["dtype"] == "test_datastructure/Level1"
    assert loaded.__jsondump__()["inheritance"] == []

    # level1 attributes should still be available
    assert loaded.level1_attr == "level1"
    # Meanwhile, level2 attributes will be discarded
    assert not hasattr(loaded, "level2_attr")


def test_inheritance_fallback_multi_level(level3):
    if compas.IPY:
        # IronPython is not able to deserialize a class that is defined in a local scope like Level1.
        # We skip this tests for IronPython.
        return

    assert level3.__jsondump__()["dtype"] == "test_datastructure/Level3"
    # Level3 should serialize Level2 and Level1 into the inheritance
    assert level3.__jsondump__()["inheritance"] == ["test_datastructure/Level2", "test_datastructure/Level1"]

    dumped = json_dumps(level3)
    loaded = json_loads(dumped)

    # The loaded object should be deserialized as the closes available class: Level1
    assert loaded.__class__ == Level1
    assert loaded.__jsondump__()["dtype"] == "test_datastructure/Level1"
    assert loaded.__jsondump__()["inheritance"] == []

    # level1 attributes should still be available
    assert loaded.level1_attr == "level1"

    # level2 and 3 attributes will be discarded
    assert not hasattr(loaded, "level2_attr")
    assert not hasattr(loaded, "level3_attr")


def test_custom_mesh(custom_mesh):
    # This test should pass both Python and IronPython
    assert custom_mesh.__jsondump__()["dtype"].endswith("CustomMesh")
    assert custom_mesh.__jsondump__()["inheritance"] == ["compas.datastructures/Mesh"]
    assert custom_mesh.__jsondump__()["data"]["custom_mesh_attr"] == "custom_mesh"

    dumped = json_dumps(custom_mesh)
    loaded = json_loads(dumped)

    assert loaded.__class__ == Mesh
    assert loaded.__jsondump__()["dtype"] == "compas.datastructures/Mesh"
    assert loaded.__jsondump__()["inheritance"] == []
    assert not hasattr(loaded, "custom_mesh_attr")
