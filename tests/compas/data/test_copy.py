from compas.data import Data


class ExampleData(Data):
    @property
    def __data__(self):
        return {}


def test_copy_noname():
    data = ExampleData()

    assert data._name is None
    assert data.name == "ExampleData"

    assert data.copy()._name is None
    assert data.copy().name == "ExampleData"

    assert data.name == data.copy().name
    assert data.__dtype__ == data.copy().__dtype__

    assert data.guid != data.copy().guid
    assert data.guid == data.copy(copy_guid=True).guid

    assert data.__jsondump__() != data.copy().__jsondump__()
    assert data.__jsondump__() == data.copy(copy_guid=True).__jsondump__()

    assert data.to_jsonstring() != data.copy().to_jsonstring()
    assert data.to_jsonstring() == data.copy(copy_guid=True).to_jsonstring()

    assert data.__jsondump__(minimal=True) == data.copy().__jsondump__(minimal=True)
    assert data.__jsondump__(minimal=True) == data.copy(copy_guid=False).__jsondump__(minimal=True)

    assert data.to_jsonstring(minimal=True) == data.copy().to_jsonstring(minimal=True)
    assert data.to_jsonstring(minimal=True) == data.copy(copy_guid=False).to_jsonstring(minimal=True)


def test_copy():
    data = ExampleData(name="test")

    assert data._name == "test"
    assert data.name == "test"

    assert data.copy()._name == "test"
    assert data.copy().name == "test"

    assert data.name == data.copy().name
    assert data.__dtype__ == data.copy().__dtype__

    assert data.guid != data.copy().guid
    assert data.guid == data.copy(copy_guid=True).guid

    assert data.__jsondump__() != data.copy().__jsondump__()
    assert data.__jsondump__() == data.copy(copy_guid=True).__jsondump__()

    assert data.to_jsonstring() != data.copy().to_jsonstring()
    assert data.to_jsonstring() == data.copy(copy_guid=True).to_jsonstring()

    assert data.__jsondump__(minimal=True) == data.copy().__jsondump__(minimal=True)
    assert data.__jsondump__(minimal=True) == data.copy(copy_guid=False).__jsondump__(minimal=True)

    assert data.to_jsonstring(minimal=True) == data.copy().to_jsonstring(minimal=True)
    assert data.to_jsonstring(minimal=True) == data.copy(copy_guid=False).to_jsonstring(minimal=True)


def test_empty_name_is_preserved():
    data = ExampleData(name="")

    assert data.name == ""
    assert data.copy().name == ""
