from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import xml.etree.ElementTree as ET

import compas

__all__ = [
    'prettify',
    'XML',
    'XMLReader',
]


class XML(object):
    """Read XML files.

    This class simplifies reading XML files and strings
    across different Python implementations.

    Attributes
    ----------
    reader : :class:`XMLReader`
        Reader used to process the XML file or string.
    writer : :class:`XMLWriter`
        Writer used to process the XML object to a file or string.
    filepath : str

    Examples
    --------
    >>> from compas.files import XML
    >>> xml = XML.from_string("<Main><Title>Test</Title></Main>")
    >>> xml.root.tag
    'Main'

    """

    def __init__(self, filepath=None):
        self.filepath = filepath
        self._is_parsed = False
        self._reader = None
        self._writer = None

    @property
    def reader(self):
        if not self._reader:
            self.read()
        return self._reader

    @property
    def writer(self):
        if not self._writer:
            self._writer = XMLWriter(self)
        return self._writer

    def read(self):
        """Read XML from a file path or file-like object,
        stored in the attribute ``filepath``.

        """
        self._reader = XMLReader.from_file(self.filepath)

    def write(self, pretty=True):
        """Writes the string representation of this XML instance,
        including all sub-elements, to the file path in the
        associated XML object.

        Parameters
        ----------
        pretty : bool, optional
            Whether the string should include whitespace for legibility.
            Defaults to ``False``.

        Returns
        -------
        ``None``

        """
        self.writer.write(pretty)

    def to_file(self, pretty=True):
        """Writes the string representation of this XML instance,
        including all sub-elements, to the file path in the
        associated XML object.

        Parameters
        ----------
        pretty : bool, optional
            Whether the string should include whitespace for legibility.
            Defaults to ``False``.

        Returns
        -------
        ``None``

        """
        self.write(pretty)

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
        xml = cls()
        xml._reader = XMLReader.from_file(source)
        return xml

    @classmethod
    def from_string(cls, text):
        """Read XML from a string.

        Parameters
        ----------
        text : :obj:`str`
            XML string.

        """
        xml = cls()
        xml._reader = XMLReader.from_string(text)
        return xml

    def to_string(self, encoding='utf-8', pretty=False):
        """Generate a string representation of this XML instance,
        including all sub-elements.

        Parameters
        ----------
        encoding : str, optional
            Output encoding (the default is 'utf-8')
        pretty : bool, optional
            Whether the string should include whitespace for legibility.
            Defaults to ``False``.

        Returns
        -------
        str
            String representation of the XML.

        """
        return self.writer.to_string(encoding=encoding, pretty=pretty)


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


class XMLWriter(object):
    """Writes an XML file from XML object.

    Parameters
    ----------
    xml : :class:`compas.files.XML`

    """
    def __init__(self, xml):
        self.xml = xml

    def write(self, pretty=True):
        string = self.to_string(pretty=pretty)
        with open(self.xml.filepath, 'wb') as f:
            f.write(string)

    def to_string(self, encoding='utf-8', pretty=False):
        rough_string = ET.tostring(self.xml.root, encoding=encoding, method='xml')
        if not pretty:
            return rough_string
        return prettify(rough_string)


if compas.is_ironpython():
    from compas.files.xml_cli import CLRXMLTreeParser as DefaultXMLTreeParser
    from compas.files.xml_cli import prettify
else:
    from xml.dom import minidom

    DefaultXMLTreeParser = ET.XMLParser

    def prettify(rough_string):
        """Return an XML string with added whitespace for legibility.

        Parameters
        ----------
        rough_string : str
            XML string
        """
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ", encoding='utf-8')
