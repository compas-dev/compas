from io import BytesIO
from io import StringIO

from compas.datastructures import Mesh
from compas.files import ply_data
from compas.files import read_ply
from compas.files import write_ply


ASCII_PLY = """\
ply
format ascii 1.0
comment example
obj_info source test
element vertex 3
property float x
property float y
property float z
property uchar red
element face 1
property list uchar int vertex_indices
end_header
0 0 0 255
1 0 0 128
0 1 0 64
3 0 1 2
"""

PLY_WITH_DUPLICATE_VERTICES = """\
ply
format ascii 1.0
element vertex 6
property float x
property float y
property float z
element face 2
property list uchar int vertex_indices
end_header
0 0 0
1 0 0
0 1 0
0 0 0
0 1 0
1 1 0
3 0 1 2
3 3 4 5
"""


def test_ply_data_extracts_mesh_geometry():
    data = ply_data(read_ply(StringIO(ASCII_PLY)))

    assert data.vertices == [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]
    assert data.faces == [[0, 1, 2]]


def test_write_ply_adds_metadata_without_mutating_document():
    document = read_ply(StringIO(ASCII_PLY))
    stream = StringIO()

    write_ply(stream, document, author="COMPAS")
    stream.seek(0)
    restored = read_ply(stream)

    assert document.comments == ["example"]
    assert restored.comments == ["example", "author: COMPAS"]


def test_mesh_ply_roundtrip_preserves_counts():
    mesh = Mesh.from_vertices_and_faces(
        [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0], [0.0, 1.0, 0.0]],
        [[0, 1, 2, 3]],
    )
    stream = BytesIO()

    mesh.to_ply(stream)
    stream.seek(0)
    restored = Mesh.from_ply(stream)

    assert restored.number_of_vertices() == 4
    assert restored.number_of_faces() == 1


def test_mesh_ply_roundtrip_preserves_unwelded_vertex_identity():
    mesh = Mesh.from_ply(StringIO(PLY_WITH_DUPLICATE_VERTICES))
    stream = BytesIO()

    mesh.to_ply(stream)
    stream.seek(0)
    restored = Mesh.from_ply(stream)

    assert mesh.number_of_vertices() == 6
    assert mesh.number_of_faces() == 2
    assert restored.number_of_vertices() == 6
    assert restored.number_of_faces() == 2


def test_mesh_ply_roundtrip_preserves_explicit_welding():
    mesh = Mesh.from_ply(StringIO(PLY_WITH_DUPLICATE_VERTICES))
    mesh.weld()
    stream = BytesIO()

    mesh.to_ply(stream)
    stream.seek(0)
    restored = Mesh.from_ply(stream)

    assert mesh.number_of_vertices() == 4
    assert mesh.number_of_faces() == 2
    assert restored.number_of_vertices() == 4
    assert restored.number_of_faces() == 2
