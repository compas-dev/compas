from io import BytesIO
from io import StringIO

from compas.files import STLReader


def test_stl_reader_reads_text_stream_as_bytes():
    source = "solid Grüezi\nendsolid Grüezi\n"

    assert STLReader(StringIO(source)).read() == source.encode("utf-8")


def test_stl_reader_reads_binary_stream():
    source = b"binary data"

    assert STLReader(BytesIO(source)).read() == source


def test_stl_reader_uses_configured_encoding():
    source = "solid Grüezi\nendsolid Grüezi\n"

    assert STLReader(StringIO(source), encoding="latin-1").read() == source.encode("latin-1")
