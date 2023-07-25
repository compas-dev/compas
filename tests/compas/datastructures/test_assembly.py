import pytest

from compas.data import json_dumps
from compas.data import json_loads
from compas.datastructures import Assembly
from compas.datastructures import AssemblyError
from compas.datastructures import Part


def test_init():
    assembly = Assembly(name="abc")
    assert assembly.name == "abc"

    assembly = Assembly(attr1="value", attr2=3.14)
    assert assembly.attributes["attr1"] == "value"
    assert assembly.attributes["attr2"] == 3.14


def test_add_parts():
    assembly = Assembly()

    for _ in range(3):
        assembly.add_part(Part())

    assert len(list(assembly.parts())) == 3


def test_add_duplicate_parts():
    assembly = Assembly()

    part = Part()
    assembly.add_part(part)

    with pytest.raises(AssemblyError):
        assembly.add_part(part)


def test_add_connections():
    assembly = Assembly()
    parts = [Part() for i in range(3)]

    for part in parts:
        assembly.add_part(part)

    assembly.add_connection(parts[0], parts[1])
    assembly.add_connection(parts[1], parts[2])
    assembly.add_connection(parts[2], parts[0])

    assert list(assembly.connections()) == [(0, 1), (1, 2), (2, 0)]


def test_find():
    assembly = Assembly()
    part = Part()
    assert assembly.find(part.guid) is None

    assembly.add_part(part)
    assert assembly.find(part.guid) == part


def test_find_by_key():
    assembly = Assembly()
    part = Part()
    assembly.add_part(part, key=2)
    assert assembly.find_by_key(2) == part

    part = Part()
    assembly.add_part(part, key="6")
    assert assembly.find_by_key("6") == part

    assert assembly.find_by_key("100") is None


def test_find_by_key_after_from_data():
    assembly = Assembly()
    part = Part()
    assembly.add_part(part, key=2)
    assembly = Assembly.from_data(assembly.to_data())
    assert assembly.find_by_key(2) == part


def test_find_by_key_after_deserialization():
    assembly = Assembly()
    part = Part(name="test_part")
    assembly.add_part(part, key=2)
    assembly = json_loads(json_dumps(assembly))

    deserialized_part = assembly.find_by_key(2)
    assert deserialized_part.name == part.name
    assert deserialized_part.key == part.key
    assert deserialized_part.guid == part.guid
    assert deserialized_part.attributes == part.attributes
