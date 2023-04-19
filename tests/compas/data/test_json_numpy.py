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
