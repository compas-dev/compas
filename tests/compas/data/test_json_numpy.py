import compas

try:
    import numpy as np

    def test_json_numpy():
        before = [
            np.array([1, 2, 3]),
            np.array([1.0, 2.0, 3.0]),
            np.float64(1.0),
            np.int32(1),
        ]
        after = compas.json_loads(compas.json_dumps(before))
        assert after == [[1, 2, 3], [1.0, 2.0, 3.0], 1.0, 1]

except ImportError:
    pass


try:
    import numpy as np

    try:
        np_float = np.float_
    except AttributeError:
        np_float = np.float64

    def test_json_numpy_float():
        before = [
            np.array([1, 2, 3], dtype=np_float),
            np.array([1.0, 2.0, 3.0]),
            np_float(1.0),
        ]
        after = compas.json_loads(compas.json_dumps(before))
        assert after == [[1, 2, 3], [1.0, 2.0, 3.0], 1.0]

except ImportError:
    pass
