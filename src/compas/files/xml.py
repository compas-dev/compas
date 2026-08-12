"""Read and write XML with the standard library ElementTree API."""

import xml.etree.ElementTree as ET
from copy import deepcopy
from os import PathLike
from typing import BinaryIO
from typing import Optional
from typing import TextIO
from typing import Union

from compas import _iotools

XMLSource = Union[str, PathLike[str], TextIO, BinaryIO]
XMLTarget = Union[str, PathLike[str], TextIO, BinaryIO]


def read_xml(source: XMLSource, parser: Optional[ET.XMLParser] = None) -> ET.Element:
    """Read an XML document.

    Parameters
    ----------
    source
        Path, URL, text stream, or binary stream containing XML data.
    parser
        Custom ElementTree parser.

    Returns
    -------
    Element
        Root element of the XML document.

    """
    with _iotools.open_file(source, "rb") as stream:
        return ET.parse(stream, parser=parser).getroot()


def parse_xml(text: Union[str, bytes], parser: Optional[ET.XMLParser] = None) -> ET.Element:
    """Parse an XML string.

    Parameters
    ----------
    text
        XML text or bytes.
    parser
        Custom ElementTree parser.

    Returns
    -------
    Element
        Root element of the XML document.

    """
    return ET.fromstring(text, parser=parser)


def xml_to_string(
    root: ET.Element,
    encoding: str = "unicode",
    pretty: bool = False,
    xml_declaration: Optional[bool] = None,
) -> Union[str, bytes]:
    """Serialize an XML element tree.

    Parameters
    ----------
    root
        Root element to serialize.
    encoding
        Output encoding. Use `unicode` to return a string.
    pretty
        If True, indent the output.
    xml_declaration
        Controls inclusion of the XML declaration.

    Returns
    -------
    str | bytes
        Serialized XML data. The return type depends on `encoding`.

    """
    element = deepcopy(root) if pretty else root
    if pretty:
        ET.indent(element, space="  ")
    return ET.tostring(element, encoding=encoding, xml_declaration=xml_declaration)


def write_xml(
    target: XMLTarget,
    root: ET.Element,
    encoding: str = "utf-8",
    pretty: bool = False,
    xml_declaration: Optional[bool] = None,
) -> None:
    """Write an XML element tree.

    Parameters
    ----------
    target
        Path or writable text or binary stream.
    root
        Root element to write.
    encoding
        Output encoding.
    pretty
        If True, indent the output.
    xml_declaration
        Controls inclusion of the XML declaration.

    Returns
    -------
    None

    """
    data = xml_to_string(root, encoding=encoding, pretty=pretty, xml_declaration=xml_declaration)
    with _iotools.open_file(target, "wb") as stream:
        try:
            stream.write(data)
        except TypeError:
            if isinstance(data, bytes):
                stream.write(data.decode(encoding))
            else:
                stream.write(data.encode(encoding))
