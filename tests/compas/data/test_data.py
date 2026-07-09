import compas
from compas.data import Data
from compas.geometry import Point


def test_string_casting():
    class TestClass(Data):
        def __init__(self, i):
            self.i = i

        def __str__(self):
            return "TestClass {}".format(self.i)

    test = TestClass(42)
    assert str(test) == "TestClass 42"


def test_canonical_hash_is_guid_independent():
    a = Point(1, 2, 3)
    b = Point(1, 2, 3)
    assert a.guid != b.guid
    assert a.canonical_hash() == b.canonical_hash()
    # sha256 is coupled to the guid, so it differs for these two
    assert a.sha256() != b.sha256()


def test_canonical_hash_is_content_sensitive():
    assert Point(1, 2, 3).canonical_hash() != Point(1, 2, 4).canonical_hash()


def test_canonical_hash_is_stable_and_string_form():
    p = Point(1, 2, 3)
    assert p.canonical_hash() == p.canonical_hash()
    assert p.canonical_hash(as_string=True) == p.canonical_hash(as_string=True)
    assert isinstance(p.canonical_hash(as_string=True), str)
    assert isinstance(p.canonical_hash(), bytes)


def test_canonical_hash_survives_json_roundtrip():
    p = Point(1, 2, 3)
    q = compas.json_loads(compas.json_dumps(p))
    assert q.canonical_hash() == p.canonical_hash()
