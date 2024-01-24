from compas.data import Data


def test_string_casting():
    class TestClass(Data):
        def __init__(self, i):
            self.i = i

        def __str__(self):
            return "TestClass {}".format(self.i)

    test = TestClass(42)
    assert str(test) == "TestClass 42"


def test___eq__():
    class SerilailableClass(Data):
        def __init__(self, int_attr, str_attr, bool_attr, float_attr, list_attr, dict_attr, data_attr):
            self.int_attr = int_attr
            self.str_attr = str_attr
            self.bool_attr = bool_attr
            self.float_attr = float_attr
            self.list_attr = list_attr
            self.dict_attr = dict_attr
            self.data_attr = data_attr

        @property
        def __data__(self):
            return {
                "int_attr": self.int_attr,
                "str_attr": self.str_attr,
                "bool_attr": self.bool_attr,
                "float_attr": self.float_attr,
                "list_attr": self.list_attr,
                "dict_attr": self.dict_attr,
                "data_attr": self.data_attr,
            }

    instanceA = SerilailableClass(1, "str", True, 1.0, [1, 2, 3], {"a": 1, "b": 2}, None)
    instanceB = SerilailableClass(2, "str", True, 1.0, [1, 2, 3], {"a": 1, "b": 2}, None)
    instanceC = SerilailableClass(3, "str", False, 0.0, [3, 2, 1], {"c": 1, "d": 2}, instanceA)
    instanceD = SerilailableClass(4, "str", False, 0.0, [3, 2, 1], {"c": 1, "d": 2}, instanceB)

    assert instanceA != instanceB
    assert instanceC != instanceD

    instanceB.int_attr = 1
    assert instanceA == instanceB
    assert instanceC != instanceD

    instanceD.int_attr = 3
    assert instanceC == instanceD
