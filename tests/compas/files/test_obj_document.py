import pytest

from compas.files import OBJDocument
from compas.files import OBJElementReference
from compas.files import OBJFace
from compas.files import OBJGroup
from compas.files import OBJVertexReference


def test_obj_document_defaults_are_independent():
    first = OBJDocument()
    second = OBJDocument()

    first.vertices.append([0.0, 0.0, 0.0])

    assert second.vertices == []


def test_obj_document_validates_structured_references():
    document = OBJDocument(
        vertices=[[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]],
        texture_vertices=[[0.0, 0.0], [1.0, 0.0], [0.0, 1.0]],
        normals=[[0.0, 0.0, 1.0]],
        faces=[
            OBJFace(
                vertices=[
                    OBJVertexReference(0, 0, 0),
                    OBJVertexReference(1, 1, 0),
                    OBJVertexReference(2, 2, 0),
                ],
                material="material",
                smoothing="1",
            )
        ],
        groups={
            "group": OBJGroup(
                name="group",
                elements=[OBJElementReference("face", 0)],
            )
        },
    )

    document.validate()


@pytest.mark.parametrize(
    "document",
    [
        OBJDocument(vertices=[[0.0, 0.0]]),
        OBJDocument(vertices=[[0.0, 0.0, 0.0]], vertex_weights=[1.0, 1.0]),
        OBJDocument(vertices=[[0.0, 0.0, 0.0]], faces=[OBJFace([OBJVertexReference(1)])]),
        OBJDocument(vertices=[[0.0, 0.0, 0.0]], groups={"g": OBJGroup("g", [OBJElementReference("face", 0)])}),
    ],
)
def test_obj_document_rejects_invalid_data(document):
    with pytest.raises(ValueError):
        document.validate()
