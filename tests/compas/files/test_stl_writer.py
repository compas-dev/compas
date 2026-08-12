from io import BytesIO
from io import StringIO

from compas.files import STLDocument
from compas.files import STLFacet
from compas.files import STLSolid
from compas.files import STLWriter
from compas.files import read_stl


def make_document():
    return STLDocument(solids=[STLSolid("part", [STLFacet([0, 0, 1], [[-1.23456, 0, 0], [0, 0, 0], [0, 1, 0]])])])


def test_stl_writer_writes_ascii_text_stream_with_precision():
    stream = StringIO()

    STLWriter(stream, precision=3).write(make_document())

    assert "vertex -1.235 0 0" in stream.getvalue()
    assert stream.getvalue().startswith("solid part\n")


def test_stl_writer_writes_binary_stream_and_preserves_semantics():
    document = make_document()
    document.format = "binary"
    document.header = b"header"
    document.solids[0].facets[0].attribute = 11
    stream = BytesIO()

    STLWriter(stream).write(document)
    stream.seek(0)
    restored = read_stl(stream)

    assert restored.format == "binary"
    assert restored.header.startswith(b"header")
    assert restored.solids[0].facets[0].attribute == 11


def test_stl_writer_can_override_document_format():
    stream = StringIO()

    document = make_document()
    document.format = "binary"
    STLWriter(stream, format="ascii").write(document)

    assert stream.getvalue().startswith("solid part\n")
