import pytest

from compas.files import OFFDocument


def test_off_document_rejects_invalid_coordinate_dimensions():
    document = OFFDocument(vertices=[[0.0, 0.0]])

    with pytest.raises(ValueError, match="three coordinates"):
        document.validate()


def test_off_document_rejects_invalid_vertex_indices():
    document = OFFDocument(vertices=[[0.0, 0.0, 0.0]], faces=[[0, 1, 0]])

    with pytest.raises(ValueError, match="invalid vertex index"):
        document.validate()
