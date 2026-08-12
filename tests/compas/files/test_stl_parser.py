import struct

import pytest

from compas.files import STLParser
from compas.files.stl_parser import STLParseError


ASCII_STL = b"""solid first
facet normal 0 0 1
outer loop
vertex 0 0 0
vertex 1 0 0
vertex 0 1 0
endloop
endfacet
endsolid first
solid second
endsolid second
"""


def test_stl_parser_parses_multiple_ascii_solids():
    document = STLParser(ASCII_STL).parse()

    assert document.format == "ascii"
    assert [solid.name for solid in document.solids] == ["first", "second"]
    assert len(document.solids[0].facets) == 1


def test_stl_parser_detects_binary_with_solid_header():
    header = b"solid deceptive binary header".ljust(80, b"\0")
    facet = struct.pack("<12fH", *([0.0] * 12), 23)

    document = STLParser(header + struct.pack("<I", 1) + facet).parse()

    assert document.format == "binary"
    assert document.header == header
    assert document.solids[0].facets[0].attribute == 23


@pytest.mark.parametrize(
    "source",
    [
        b"",
        b"solid part\nfacet normal 0 0 1\n",
        b"solid part\nvertex 0 0 0\nendsolid part\n",
        b"solid part\nfacet normal 0 0 1\nouter loop\nvertex 0 0 0\nendloop\nendfacet\nendsolid part\n",
        b"solid part\nfacet normal 0 0 1\nvertex 0 0 0\nvertex 1 0 0\nvertex 0 1 0\nendfacet\nendsolid part\n",
        b"solid part\nunexpected\nendsolid part\n",
    ],
)
def test_stl_parser_rejects_invalid_ascii(source):
    with pytest.raises(STLParseError):
        STLParser(source).parse()


def test_stl_parser_rejects_truncated_binary_data():
    source = b"binary".ljust(80, b"\0") + struct.pack("<I", 1) + b"\0" * 49

    with pytest.raises(STLParseError):
        STLParser(source).parse()
