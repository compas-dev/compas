from io import BytesIO
from io import StringIO

from compas.files import OBJDocument
from compas.files import OBJElementReference
from compas.files import OBJFace
from compas.files import OBJGroup
from compas.files import OBJLine
from compas.files import OBJObject
from compas.files import OBJVertexReference
from compas.files.obj_parser import OBJParser
from compas.files.obj_reader import OBJReader
from compas.files.obj_writer import OBJWriter


def make_document():
    face_reference = OBJElementReference("face", 0)
    line_reference = OBJElementReference("line", 0)
    return OBJDocument(
        vertices=[[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]],
        vertex_weights=[1.0, 0.5, 1.0],
        texture_vertices=[[0.0, 0.0], [1.0, 0.0], [0.0, 1.0]],
        normals=[[0.0, 0.0, 1.0]],
        lines=[OBJLine([OBJVertexReference(0), OBJVertexReference(1)])],
        faces=[
            OBJFace(
                [
                    OBJVertexReference(0, 0, 0),
                    OBJVertexReference(1, 1, 0),
                    OBJVertexReference(2, 2, 0),
                ],
                material="red",
                smoothing="1",
            )
        ],
        elements=[line_reference, face_reference],
        objects={"Object": OBJObject("Object", [line_reference, face_reference])},
        groups={"Group": OBJGroup("Group", [face_reference])},
        material_libraries=["materials.mtl"],
    )


def test_obj_writer_writes_document_to_text_stream():
    stream = StringIO()

    OBJWriter(stream, precision=3).write(make_document())

    assert stream.getvalue() == (
        "mtllib materials.mtl\n"
        "v 0 0 0\n"
        "v 1 0 0 0.5\n"
        "v 0 1 0\n"
        "vt 0 0\n"
        "vt 1 0\n"
        "vt 0 1\n"
        "vn 0 0 1\n"
        "o Object\n"
        "l 1 2\n"
        "g Group\n"
        "usemtl red\n"
        "s 1\n"
        "f 1/1/1 2/2/1 3/3/1\n"
    )


def test_obj_writer_supports_binary_streams():
    stream = BytesIO()

    OBJWriter(stream).write(OBJDocument(vertices=[[0.0, 0.0, 0.0]]))

    assert stream.getvalue() == b"v 0.0 0.0 0.0\n"


def test_obj_document_roundtrip_preserves_semantics():
    stream = StringIO()
    original = make_document()
    original.comments.append("roundtrip metadata")

    OBJWriter(stream).write(original)
    stream.seek(0)
    restored = OBJParser(OBJReader(stream).read()).parse()

    assert restored.vertices == original.vertices
    assert restored.vertex_weights == original.vertex_weights
    assert restored.texture_vertices == original.texture_vertices
    assert restored.normals == original.normals
    assert restored.lines == original.lines
    assert restored.faces == original.faces
    assert restored.elements == original.elements
    assert restored.objects == original.objects
    assert restored.groups == original.groups
    assert restored.material_libraries == original.material_libraries
    assert restored.comments == original.comments
