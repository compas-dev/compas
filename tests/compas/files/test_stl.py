from io import BytesIO
from io import StringIO

from compas.datastructures import Mesh
from compas.files import STLDocument
from compas.files import STLFacet
from compas.files import STLSolid
from compas.files import read_stl
from compas.files import stl_data
from compas.files import weld_stl_data
from compas.files import write_stl


STL_WITH_SHARED_COORDINATES = """\
solid square
facet normal 0 0 1
outer loop
vertex 0 0 0
vertex 1 0 0
vertex 0 1 0
endloop
endfacet
facet normal 0 0 1
outer loop
vertex 1 0 0
vertex 1 1 0
vertex 0 1 0
endloop
endfacet
endsolid square
"""


def test_stl_projection_only_welds_when_requested():
    document = read_stl(StringIO(STL_WITH_SHARED_COORDINATES))

    unwelded = stl_data(document)
    welded = weld_stl_data(document)

    assert len(unwelded.vertices) == 6
    assert len(unwelded.faces) == 2
    assert len(welded.vertices) == 4
    assert len(welded.faces) == 2


def test_mesh_ascii_stl_roundtrip_welds_facet_vertices():
    mesh = Mesh.from_stl(StringIO(STL_WITH_SHARED_COORDINATES))
    stream = StringIO()

    mesh.to_stl(stream)
    stream.seek(0)
    restored = Mesh.from_stl(stream)

    assert mesh.number_of_vertices() == 4
    assert mesh.number_of_faces() == 2
    assert restored.number_of_vertices() == 4
    assert restored.number_of_faces() == 2


def test_mesh_binary_stl_roundtrip():
    mesh = Mesh.from_stl(StringIO(STL_WITH_SHARED_COORDINATES))
    stream = BytesIO()

    mesh.to_stl(stream, binary=True)
    stream.seek(0)
    restored = Mesh.from_stl(stream)

    assert restored.number_of_vertices() == mesh.number_of_vertices()
    assert restored.number_of_faces() == mesh.number_of_faces()


def test_write_stl_retains_document_format_and_does_not_mutate_document():
    document = STLDocument(
        format="binary",
        header=b"example",
        solids=[STLSolid("part", [STLFacet([0, 0, 1], [[-1, 0, 0], [0, 0, 0], [-1, 1, 0]], 7)])],
    )
    stream = BytesIO()

    write_stl(stream, document)
    stream.seek(0)
    restored = read_stl(stream)

    assert document.header == b"example"
    assert restored.format == "binary"
    assert restored.header.startswith(b"example")
    assert restored.solids[0].facets[0].attribute == 7
    assert restored.solids[0].facets[0].vertices[0][0] == -1
