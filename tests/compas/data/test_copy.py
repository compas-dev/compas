from compas.data import Data


class TestData(Data):
    @property
    def __data__(self):
        return {}


def test_copy():
    data = TestData()

    assert data.name == data.copy().name
    assert data.__dtype__ == data.copy().__dtype__

    assert data.guid != data.copy().guid
    assert data.__jsondump__() != data.copy().__jsondump__()
    assert data.to_jsonstring() != data.copy().to_jsonstring()

    assert data.__jsondump__(minimal=True) == data.copy().__jsondump__(minimal=True)
    assert data.to_jsonstring(minimal=True) == data.copy().to_jsonstring(minimal=True)
