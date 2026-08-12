from io import BytesIO
from io import StringIO

from compas.files import OBJReader


def test_obj_reader_reads_text_stream_as_bytes():
    source = "v 0 0 0\n"

    assert OBJReader(StringIO(source)).read() == source.encode("utf-8")


def test_obj_reader_reads_binary_stream():
    source = b"v 0 0 0\n"

    assert OBJReader(BytesIO(source)).read() == source


def test_obj_reader_uses_configured_encoding_for_text_streams():
    source = "# Gr\u00fcezi\n"

    assert OBJReader(StringIO(source), encoding="latin-1").read() == source.encode("latin-1")
