from compas.datastructures import Assembly, assembly
from compas.datastructures import Part


def test_init():
    assembly = Assembly(name='abc')
    assert assembly.name == 'abc'

    assembly = Assembly(attr1='value', attr2=3.14)
    assert assembly.attributes['attr1'] == 'value'
    assert assembly.attributes['attr2'] == 3.14


def test_add_parts():
    assembly = Assembly()

    for _ in range(3):
        assembly.add_part(Part())

    assert len(list(assembly.parts())) == 3


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
