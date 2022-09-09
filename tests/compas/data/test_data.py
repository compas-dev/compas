from compas.data import Data


def test_string_casting():
    class TestClass(Data):
        def __init__(self, i):
            self.i = i

        def __str__(self):
            return "TestClass {}".format(self.i)

    test = TestClass(42)
    assert str(test) == "TestClass 42"
