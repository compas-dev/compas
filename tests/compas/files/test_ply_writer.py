from io import BytesIO
from io import StringIO

from compas.files import PLYDocument
from compas.files import PLYElement
from compas.files import PLYProperty
from compas.files import PLYWriter
from compas.files import ply_data
from compas.files import read_ply


def make_document(format="ascii"):
    return PLYDocument(
        format=format,
        comments=["example"],
        elements=[
            PLYElement(
                "vertex",
                [PLYProperty("x", "float"), PLYProperty("y", "float"), PLYProperty("z", "float")],
                [
                    {"x": 0.0, "y": 0.0, "z": 0.0},
                    {"x": 1.0, "y": 0.0, "z": 0.0},
                    {"x": 1.0, "y": 1.0, "z": 0.0},
                    {"x": 0.0, "y": 1.0, "z": 0.0},
                ],
            ),
            PLYElement(
                "face",
                [PLYProperty("vertex_indices", "int", "uchar")],
                [{"vertex_indices": [0, 1, 2, 3]}],
            ),
        ],
    )


def test_ply_writer_writes_ascii_to_text_stream():
    stream = StringIO()

    PLYWriter(stream).write(make_document())

    result = stream.getvalue()
    assert result.startswith("ply\nformat ascii 1.0\ncomment example\n")
    assert result.endswith("4 0 1 2 3\n")


def test_ply_writer_applies_precision_without_mutating_document():
    document = make_document()
    document.elements[0].data[1]["x"] = 1.23456
    stream = StringIO()

    PLYWriter(stream, precision=3).write(document)

    assert "1.235 0 0\n" in stream.getvalue()
    assert document.elements[0].data[1]["x"] == 1.23456


def test_ply_writer_ascii_document_roundtrip():
    original = make_document()
    stream = StringIO()

    PLYWriter(stream).write(original)
    stream.seek(0)

    assert read_ply(stream) == original


def test_ply_writer_binary_document_roundtrip_with_variable_face_size():
    stream = BytesIO()

    PLYWriter(stream).write(make_document("binary_big_endian"))
    stream.seek(0)
    restored = read_ply(stream)

    assert restored.format == "binary_big_endian"
    assert ply_data(restored).faces == [[0, 1, 2, 3]]
