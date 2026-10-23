import pickle

from compas.geometry import Frame


def test_pickling():
    f1 = Frame.worldXY()
    f1.name = "pickled frame"
    s = pickle.dumps(f1, protocol=pickle.HIGHEST_PROTOCOL)
    f2 = pickle.loads(s)
    assert f1 is not f2
    assert f2.name == "pickled frame"
    assert all(a == b for a, b in zip(f1.point, f2.point))
    assert all(a == b for a, b in zip(f1.xaxis, f2.xaxis))
    assert all(a == b for a, b in zip(f1.yaxis, f2.yaxis))
    assert all(a == b for a, b in zip(f1.zaxis, f2.zaxis))
    assert f1.guid == f2.guid
