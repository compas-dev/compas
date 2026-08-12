from io import BytesIO
from io import StringIO

from compas.files import OFFReader


def test_off_reader_reads_text_stream_as_bytes():
    source = "OFF\n0 0 0\n"

    assert OFFReader(StringIO(source)).read() == source.encode("utf-8")


def test_off_reader_reads_binary_stream():
    source = b"OFF\n0 0 0\n"

    assert OFFReader(BytesIO(source)).read() == source


def test_off_reader_uses_configured_encoding():
    source = "OFF\n# Grüezi\n0 0 0\n"

    assert OFFReader(StringIO(source), encoding="latin-1").read() == source.encode("latin-1")
