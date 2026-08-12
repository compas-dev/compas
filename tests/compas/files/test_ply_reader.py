from io import BytesIO
from io import StringIO

from compas.files import PLYReader


def test_ply_reader_reads_text_stream_as_bytes():
    source = "ply\nformat ascii 1.0\nend_header\n"

    assert PLYReader(StringIO(source)).read() == source.encode("utf-8")


def test_ply_reader_reads_binary_stream():
    source = b"ply\nformat binary_little_endian 1.0\nend_header\n"

    assert PLYReader(BytesIO(source)).read() == source


def test_ply_reader_reads_file_path():
    source = "tests/compas/files/fixtures/triangle_binary.ply"

    assert PLYReader(source).read().startswith(b"ply")
