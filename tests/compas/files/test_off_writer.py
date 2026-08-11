from io import BytesIO
from io import StringIO

from compas.files import OFFDocument
from compas.files import OFFWriter
from compas.files import read_off


def make_document():
    return OFFDocument(
        vertices=[[0.0, 0.0, 0.0], [1.23456, 0.0, 0.0], [0.0, 1.0, 0.0]],
        faces=[[0, 1, 2]],
        edge_count=3,
        comments=["example"],
    )


def test_off_writer_writes_text_stream_with_precision():
    stream = StringIO()

    OFFWriter(stream, precision=3).write(make_document())

    assert stream.getvalue() == "OFF\n# example\n3 1 3\n0 0 0\n1.235 0 0\n0 1 0\n3 0 1 2\n"


def test_off_writer_supports_binary_streams():
    stream = BytesIO()

    OFFWriter(stream).write(OFFDocument())

    assert stream.getvalue() == b"OFF\n0 0 0\n"


def test_off_document_roundtrip_preserves_semantics():
    original = make_document()
    stream = StringIO()

    OFFWriter(stream).write(original)
    stream.seek(0)

    assert read_off(stream) == original
