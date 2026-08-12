from compas.datastructures._mutablemapping import MutableMapping


class CustomMapping(MutableMapping[str, object]):
    def __init__(self):
        self.data = {}

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __delitem__(self, key):
        del self.data[key]

    def __iter__(self):
        return iter(self.data)

    def __len__(self):
        return len(self.data)


def test_mutablemapping_views_and_defaults():
    mapping = CustomMapping()

    assert mapping.get("missing") is None
    assert mapping.get("missing", 1) == 1
    assert mapping.setdefault("key", 1) == 1
    assert list(mapping.keys()) == ["key"]
    assert list(mapping.items()) == [("key", 1)]
    assert list(mapping.values()) == [1]


def test_mutablemapping_update():
    mapping = CustomMapping()

    mapping.update({"a": 1})
    mapping.update([("b", 2)])
    mapping.update(c=3)

    assert mapping == {"a": 1, "b": 2, "c": 3}


def test_mutablemapping_removal():
    mapping = CustomMapping()
    mapping.update(a=1, b=2)

    assert mapping.pop("a") == 1
    assert mapping.pop("missing", None) is None
    assert mapping.popitem() == ("b", 2)

    mapping.update(a=1, b=2)
    mapping.clear()
    assert not mapping
