import pytest

from compas.files import STLDocument
from compas.files import STLFacet
from compas.files import STLSolid


@pytest.mark.parametrize(
    "document",
    [
        STLDocument(format="invalid"),
        STLDocument(header=b"x" * 81),
        STLDocument(solids=[STLSolid(facets=[STLFacet([0, 1], [[0, 0, 0]] * 3)])]),
        STLDocument(solids=[STLSolid(facets=[STLFacet([0, 0, 1], [[0, 0, 0]] * 2)])]),
        STLDocument(solids=[STLSolid(facets=[STLFacet([0, 0, 1], [[0, 0], [0, 0, 0], [0, 0, 0]])])]),
        STLDocument(solids=[STLSolid(facets=[STLFacet([0, 0, 1], [[0, 0, 0]] * 3, -1)])]),
        STLDocument(solids=[STLSolid(facets=[STLFacet([0, 0, 1], [[0, 0, 0]] * 3, 65536)])]),
    ],
)
def test_stl_document_rejects_invalid_data(document):
    with pytest.raises(ValueError):
        document.validate()
