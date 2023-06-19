import pickle
from compas.geometry import Frame


def test_pickling():
    f1 = Frame.worldXY()
    s = pickle.dumps(f1, protocol=pickle.HIGHEST_PROTOCOL)
    f2 = pickle.loads(s)
    assert all(a == b for a, b in zip(f1.point, f2.point))
    assert all(a == b for a, b in zip(f1.xaxis, f2.xaxis))
    assert all(a == b for a, b in zip(f1.yaxis, f2.yaxis))
    assert all(a == b for a, b in zip(f1.zaxis, f2.zaxis))
    assert f1.guid == f2.guid
