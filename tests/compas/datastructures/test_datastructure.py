import pytest
from compas.datastructures import Datastructure
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


def test_mro_fallback(level2):
    assert level2.__jsondump__()["dtype"] == "test_datastructure/Level2"
    # Level2 should serialize Level1 into the mro
    assert level2.__jsondump__()["mro"] == ["test_datastructure/Level1"]

    dumped = json_dumps(level2)
    loaded = json_loads(dumped)

    # The loaded object should be deserialized as the closes available class: Level1
    assert loaded.__class__ == Level1
    assert loaded.__jsondump__()["dtype"] == "test_datastructure/Level1"
    assert loaded.__jsondump__()["mro"] == []

    # level1 attributes should still be available
    assert loaded.level1_attr == "level1"
    # Meanwhile, level2 attributes will be discarded
    assert not hasattr(loaded, "level2_attr")


def test_mro_fallback_multi_level(level3):
    assert level3.__jsondump__()["dtype"] == "test_datastructure/Level3"
    # Level3 should serialize Level2 and Level1 into the mro
    assert level3.__jsondump__()["mro"] == ["test_datastructure/Level2", "test_datastructure/Level1"]

    dumped = json_dumps(level3)
    loaded = json_loads(dumped)

    # The loaded object should be deserialized as the closes available class: Level1
    assert loaded.__class__ == Level1
    assert loaded.__jsondump__()["dtype"] == "test_datastructure/Level1"
    assert loaded.__jsondump__()["mro"] == []

    # level1 attributes should still be available
    assert loaded.level1_attr == "level1"

    # level2 and 3 attributes will be discarded
    assert not hasattr(loaded, "level2_attr")
    assert not hasattr(loaded, "level3_attr")
