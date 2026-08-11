from io import BytesIO
from io import StringIO

from compas.datastructures import Mesh
from compas.files import OFFDocument
from compas.files import read_off
from compas.files import write_off


OFF_WITH_DUPLICATE_VERTICES = """\
OFF
6 2 0
0 0 0
1 0 0
0 1 0
0 0 0
0 1 0
1 1 0
3 0 1 2
3 3 4 5
"""


def test_write_off_adds_metadata_without_mutating_document():
    document = OFFDocument()
    stream = StringIO()

    write_off(stream, document, author="COMPAS")
    stream.seek(0)
    restored = read_off(stream)

    assert document.comments == []
    assert restored.comments == ["author: COMPAS"]


def test_mesh_off_roundtrip_preserves_unwelded_vertex_identity():
    mesh = Mesh.from_off(StringIO(OFF_WITH_DUPLICATE_VERTICES))
    stream = BytesIO()

    mesh.to_off(stream)
    stream.seek(0)
    restored = Mesh.from_off(stream)

    assert mesh.number_of_vertices() == 6
    assert mesh.number_of_faces() == 2
    assert restored.number_of_vertices() == 6
    assert restored.number_of_faces() == 2


def test_mesh_off_roundtrip_preserves_explicit_welding():
    mesh = Mesh.from_off(StringIO(OFF_WITH_DUPLICATE_VERTICES))
    mesh.weld()
    stream = BytesIO()

    mesh.to_off(stream)
    stream.seek(0)
    restored = Mesh.from_off(stream)

    assert mesh.number_of_vertices() == 4
    assert mesh.number_of_faces() == 2
    assert restored.number_of_vertices() == 4
    assert restored.number_of_faces() == 2
