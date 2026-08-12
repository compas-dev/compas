import pytest

from compas.files import PLYDocument
from compas.files import PLYElement
from compas.files import PLYProperty
from compas.files import ply_data


def test_ply_document_rejects_unsupported_property_types():
    document = PLYDocument(elements=[PLYElement("vertex", [PLYProperty("x", "imaginary")], [{"x": 0.0}])])

    with pytest.raises(ValueError, match="Unsupported PLY scalar type"):
        document.validate()


def test_ply_document_rejects_noninteger_list_count_types():
    document = PLYDocument(
        elements=[PLYElement("face", [PLYProperty("vertex_indices", "int", "float")], [{"vertex_indices": [0]}])]
    )

    with pytest.raises(ValueError, match="list counts"):
        document.validate()


def test_ply_document_rejects_values_outside_scalar_range():
    document = PLYDocument(elements=[PLYElement("vertex", [PLYProperty("red", "uchar")], [{"red": 256}])])

    with pytest.raises(ValueError, match="outside the range"):
        document.validate()


def test_ply_document_rejects_lists_too_long_for_count_type():
    document = PLYDocument(
        elements=[
            PLYElement(
                "face",
                [PLYProperty("vertex_indices", "int", "uchar")],
                [{"vertex_indices": list(range(256))}],
            )
        ]
    )

    with pytest.raises(ValueError, match="outside the range"):
        document.validate()


def test_ply_data_rejects_invalid_vertex_indices():
    document = PLYDocument(
        elements=[
            PLYElement(
                "vertex",
                [PLYProperty("x", "float"), PLYProperty("y", "float"), PLYProperty("z", "float")],
                [{"x": 0.0, "y": 0.0, "z": 0.0}],
            ),
            PLYElement(
                "face",
                [PLYProperty("vertex_indices", "int", "uchar")],
                [{"vertex_indices": [0, 1, 0]}],
            ),
        ]
    )

    with pytest.raises(ValueError, match="invalid vertex index"):
        ply_data(document)
