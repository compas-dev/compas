from io import StringIO

import pytest

from compas.files.obj_parser import OBJParseError
from compas.files.obj_parser import OBJParser
from compas.files.obj_reader import OBJReader


def parse(text):
    return OBJParser(OBJReader(StringIO(text)).read()).parse()


def test_obj_parser_handles_comments_and_continuations():
    document = parse(
        """
        # comment
        v 0 0 \\
          0 # inline comment
        f 1 1 1
        """
    )

    assert document.comments == ["comment", "inline comment"]
    assert document.vertices == [[0.0, 0.0, 0.0]]
    assert len(document.faces) == 1


def test_obj_parser_uses_configured_encoding():
    document = OBJParser("# Grüezi\n".encode("latin-1"), encoding="latin-1").parse()

    assert document.comments == ["Grüezi"]


def test_obj_parser_builds_structured_document():
    document = parse(
        """
        mtllib materials.mtl
        o Object
        g GroupA GroupB
        v 0 0 0 0.5
        v 1 0 0
        v 0 1 0
        vt 0 0
        vt 1 0
        vt 0 1
        vn 0 0 1
        usemtl red
        s 1
        f 1/1/1 2/2/1 3/3/1
        """
    )

    assert document.vertices == [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]
    assert document.vertex_weights == [0.5, 1.0, 1.0]
    assert document.faces[0].vertices[1].vertex == 1
    assert document.faces[0].vertices[1].texture == 1
    assert document.faces[0].vertices[1].normal == 0
    assert document.faces[0].material == "red"
    assert document.faces[0].smoothing == "1"
    assert document.objects["Object"].elements[0].kind == "face"
    assert document.groups["GroupA"].elements == document.groups["GroupB"].elements
    assert document.material_libraries == ["materials.mtl"]


def test_obj_parser_resolves_negative_indices_at_statement_time():
    document = parse(
        """
        v 0 0 0
        v 1 0 0
        v 0 1 0
        f -3 -2 -1
        """
    )

    assert [reference.vertex for reference in document.faces[0].vertices] == [0, 1, 2]


def test_obj_parser_converts_linear_curves_to_lines():
    document = parse(
        """
        v 0 0 0
        v 1 0 0
        cstype bspline
        deg 1
        curv 0 1 1 2
        """
    )

    assert [reference.vertex for reference in document.lines[0].vertices] == [0, 1]


@pytest.mark.parametrize(
    "statement",
    [
        "v 0 0",
        "vn 0 0",
        "f 1 2",
        "f 0 1 2",
        "f 1 2 4",
    ],
)
def test_obj_parser_reports_invalid_supported_syntax(statement):
    source = "v 0 0 0\nv 1 0 0\nv 0 1 0\n" + statement

    with pytest.raises(OBJParseError):
        parse(source)
