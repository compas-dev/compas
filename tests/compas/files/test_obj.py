from io import StringIO

from compas.datastructures import Mesh
from compas.files import OBJDocument
from compas.files import OBJFace
from compas.files import OBJVertexReference
from compas.files import obj_data
from compas.files import read_obj
from compas.files import read_obj_meshes
from compas.files import weld_obj_data
from compas.files import write_obj


OBJ_TEXT = """\
v 0 0 0
v 1 0 0
v 0 1 0
f 1 2 3
"""

OBJ_WITH_DUPLICATE_VERTICES = """\
v 0 0 0
v 1 0 0
v 0 1 0
v 0 0 0
v 0 1 0
v 1 1 0
f 1 2 3
f 4 5 6
"""


def test_read_obj_returns_document():
    document = read_obj(StringIO(OBJ_TEXT))

    assert isinstance(document, OBJDocument)
    assert document.vertices == [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]
    assert len(document.faces) == 1


def test_write_obj_writes_document():
    stream = StringIO()
    document = OBJDocument(
        vertices=[[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]],
        faces=[OBJFace([OBJVertexReference(0), OBJVertexReference(1), OBJVertexReference(2)])],
    )

    write_obj(stream, document, precision=1)

    assert stream.getvalue() == OBJ_TEXT


def test_write_obj_adds_metadata_without_mutating_document():
    stream = StringIO()
    document = OBJDocument(vertices=[[0.0, 0.0, 0.0]])

    write_obj(stream, document, author="COMPAS")
    stream.seek(0)
    restored = read_obj(stream)

    assert document.comments == []
    assert restored.comments == ["author: COMPAS"]


def test_write_obj_writes_mesh_with_compatibility_header():
    stream = StringIO()
    mesh = Mesh.from_vertices_and_faces(
        [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]],
        [[0, 1, 2]],
    )

    write_obj(stream, mesh, precision=1, author="COMPAS")

    result = stream.getvalue()
    assert "# author: COMPAS\n" in result
    assert "v 0 0 0\n" in result
    assert "f 1 2 3\n" in result


def test_obj_data_preserves_document_vertices():
    stream = StringIO("v 0 0 0\nv 0 0 0\nv 1 0 0\nl 2 3\n")
    document = read_obj(stream)
    data = obj_data(document)

    assert len(document.vertices) == 3
    assert data.vertices == document.vertices
    assert data.lines == [[1, 2]]


def test_weld_obj_data_merges_coincident_vertices():
    document = read_obj(StringIO("v 0 0 0\nv 0 0 0\nv 1 0 0\nl 2 3\n"))

    data = weld_obj_data(document)

    assert data.vertices == [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]]
    assert data.lines == [[0, 1]]


def test_mesh_write_roundtrip():
    stream = StringIO()
    mesh = Mesh.from_vertices_and_faces(
        [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]],
        [[0, 1, 2]],
    )

    write_obj(stream, mesh, precision=3)
    stream.seek(0)
    restored = obj_data(read_obj(stream))

    assert restored.vertices == [mesh.vertex_coordinates(vertex) for vertex in mesh.vertices()]
    assert restored.faces == [[0, 1, 2]]


def test_write_obj_supports_multiple_meshes_and_unwelding():
    stream = StringIO()
    mesh = Mesh.from_vertices_and_faces(
        [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0], [0.0, 1.0, 0.0]],
        [[0, 1, 2], [0, 2, 3]],
    )

    write_obj(stream, [mesh, mesh], precision=1, unweld=True)
    stream.seek(0)
    document = read_obj(stream)

    assert len(document.objects) == 2
    assert len(document.vertices) == 12
    assert len(document.faces) == 4


def test_mesh_obj_roundtrip_preserves_unwelded_vertex_identity():
    mesh = Mesh.from_obj(StringIO(OBJ_WITH_DUPLICATE_VERTICES))
    stream = StringIO()

    mesh.to_obj(stream)
    stream.seek(0)
    document = read_obj(stream)

    assert mesh.number_of_vertices() == 6
    assert mesh.number_of_faces() == 2
    assert len(document.vertices) == 6
    assert len(document.faces) == 2


def test_mesh_obj_roundtrip_preserves_explicit_welding():
    document = read_obj(StringIO(OBJ_WITH_DUPLICATE_VERTICES))
    data = weld_obj_data(document)
    mesh = Mesh.from_vertices_and_faces(data.vertices, data.faces)
    stream = StringIO()

    mesh.to_obj(stream)
    stream.seek(0)
    restored = read_obj(stream)

    assert len(document.vertices) == 6
    assert mesh.number_of_vertices() == 4
    assert mesh.number_of_faces() == 2
    assert len(restored.vertices) == 4
    assert len(restored.faces) == 2


def test_read_obj_meshes_preserves_multiple_meshes():
    first = Mesh.from_vertices_and_faces(
        [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]],
        [[0, 1, 2]],
    )
    first.name = "First"
    second = Mesh.from_vertices_and_faces(
        [[2.0, 0.0, 0.0], [3.0, 0.0, 0.0], [2.0, 1.0, 0.0], [3.0, 1.0, 0.0]],
        [[0, 1, 2], [1, 3, 2]],
    )
    second.name = "Second"
    stream = StringIO()

    write_obj(stream, [first, second])
    stream.seek(0)
    meshes = read_obj_meshes(stream)

    assert [mesh.name for mesh in meshes] == ["First", "Second"]
    assert [mesh.number_of_vertices() for mesh in meshes] == [3, 4]
    assert [mesh.number_of_faces() for mesh in meshes] == [1, 2]


def test_read_obj_meshes_can_explicitly_weld():
    meshes = read_obj_meshes(StringIO(OBJ_WITH_DUPLICATE_VERTICES), weld=True)

    assert len(meshes) == 1
    assert meshes[0].number_of_vertices() == 4
    assert meshes[0].number_of_faces() == 2
