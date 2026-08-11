from io import BytesIO
from io import StringIO

from compas.files import GLTFReader


def test_gltf_reader_reads_binary_stream_without_parsing():
    data = b'{"asset":{"version":"2.0"}}'

    source = GLTFReader(BytesIO(data)).read()

    assert source.data == data
    assert source.resource_loader is None


def test_gltf_reader_reads_text_stream_without_parsing():
    data = '{"asset":{"version":"2.0"}}'

    source = GLTFReader(StringIO(data)).read()

    assert source.data == data.encode("utf-8")
