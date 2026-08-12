from compas.data import Data


class TestData(Data):
    @property
    def __data__(self):
        return {}


def test_copy_noname():
    data = TestData()

    assert data._name is None
    assert data.name == "TestData"

    assert data.copy()._name is None
    assert data.copy().name == "TestData"

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
    data = TestData(name="test")

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
