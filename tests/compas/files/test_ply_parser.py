from io import StringIO

import pytest

from compas.files import PLYParser
from compas.files import PLYReader
from compas.files import ply_data
from compas.files.ply_parser import PLYParseError


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


def test_ply_parser_preserves_schema_and_custom_properties():
    document = PLYParser(PLYReader(StringIO(ASCII_PLY)).read()).parse()
    vertex = document.element("vertex")

    assert document.comments == ["example"]
    assert document.object_info == ["source test"]
    assert vertex is not None
    assert [prop.name for prop in vertex.properties] == ["x", "y", "z", "red"]
    assert vertex.data[1]["red"] == 128


def test_ply_parser_reads_binary_data_and_variable_lists():
    document = PLYParser(PLYReader("tests/compas/files/fixtures/triangle_binary.ply").read()).parse()
    data = ply_data(document)

    assert document.format == "binary_little_endian"
    assert len(data.vertices) == 3
    assert data.faces == [[0, 1, 2]]


@pytest.mark.parametrize(
    "source",
    [
        b"ply\nformat ascii 1.0\n",
        b"ply\nelement vertex 0\nend_header\n",
        b"ply\nformat ascii 1.0\nelement vertex 1\nproperty imaginary x\nend_header\n0\n",
        b"ply\nformat ascii 1.0\nelement vertex 1\nproperty float x\nend_header\n",
        b"ply\nformat ascii 1.0\nelement face 1\nproperty list uchar int vertex_indices\nend_header\n-1\n",
        b"ply\nformat ascii 1.0\nelement vertex 0\nend_header\nunexpected\n",
    ],
)
def test_ply_parser_rejects_invalid_ascii_documents(source):
    with pytest.raises(PLYParseError):
        PLYParser(source).parse()


def test_ply_parser_rejects_truncated_binary_data():
    source = PLYReader("tests/compas/files/fixtures/triangle_binary.ply").read()

    with pytest.raises(PLYParseError):
        PLYParser(source[:-1]).parse()
