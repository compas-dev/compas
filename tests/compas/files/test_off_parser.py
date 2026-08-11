import pytest

from compas.files import OFFParser
from compas.files.off_parser import OFFParseError


def test_off_parser_builds_document_and_preserves_comments():
    source = b"""OFF
# example
3 1 3
0 0 0
1 0 0 # vertex
0 1 \\
0
3 0 1 2
"""

    document = OFFParser(source).parse()

    assert document.vertices == [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]
    assert document.faces == [[0, 1, 2]]
    assert document.edge_count == 3
    assert document.comments == ["example", "vertex"]


def test_off_parser_accepts_counts_on_header_line():
    document = OFFParser(b"OFF 1 0 0\n0 0 0\n").parse()

    assert len(document.vertices) == 1


@pytest.mark.parametrize(
    "source",
    [
        b"NOFF\n0 0 0\n",
        b"OFF\n",
        b"OFF\n-1 0 0\n",
        b"OFF\n1 0 0\n0 0\n",
        b"OFF\n3 1 0\n0 0 0\n1 0 0\n0 1 0\n3 0 1\n",
        b"OFF\n0 0 0\nunexpected\n",
    ],
)
def test_off_parser_rejects_invalid_documents(source):
    with pytest.raises(OFFParseError):
        OFFParser(source).parse()
