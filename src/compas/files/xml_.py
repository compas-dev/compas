from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import xml.etree.ElementTree as ET

import compas


__all__ = [
    'XML',
    'XMLReader'
]


class XML(object):
    """Read XML files.

    This class simplifies reading XML files and strings
    across different Python implementations.

    Attributes
    ----------
    reader : :class:`XMLReader`
        Reader used to process the XML file or string.

    Examples
    --------
    >>> from compas.files import XML
    >>> xml = XML.from_string("<Main><Title>Test</Title></Main>")
    >>> xml.root.tag
    'Main'

    """

    def __init__(self, reader):
        self.reader = reader

    @property
    def root(self):
        """Root element of the XML tree."""
        return self.reader.root

    @classmethod
    def from_file(cls, source):
        """Read XML from a file path or file-like object.

        Parameters
        ----------
        source : str or file
            File path or file-like object.

        """
        return cls(XMLReader.from_file(source))

    @classmethod
    def from_string(cls, text):
        """Read XML from a string.

        Parameters
        ----------
        text : :obj:`str`
            XML string.

        """
        return cls(XMLReader.from_string(text))

    def to_string(self, encoding='utf-8'):
        """Generate a string representation of this XML instance,
        including all sub-elements.

        Parameters
        ----------
        encoding : str, optional
            Output encoding (the default is 'utf-8')

        Returns
        -------
        str
            String representation of the XML.

        """
        return ET.tostring(self.root, encoding=encoding, method='xml')


class XMLReader(object):
    """Reads XML files and strings.

    Parameters
    ----------
    root : :class:`xml.etree.ElementTree.Element`
        Root XML element

    """

    def __init__(self, root):
        self.root = root

    @classmethod
    def from_file(cls, source, tree_parser=None):
        tree_parser = tree_parser or DefaultXMLTreeParser
        tree = ET.parse(source, tree_parser())
        return cls(tree.getroot())

    @classmethod
    def from_string(cls, text, tree_parser=None):
        tree_parser = tree_parser or DefaultXMLTreeParser
        root = ET.fromstring(text, tree_parser())
        return cls(root)


if compas.is_ironpython():
    from compas.files.xml_cli import CLRXMLTreeParser as DefaultXMLTreeParser
else:
    DefaultXMLTreeParser = ET.XMLParser
