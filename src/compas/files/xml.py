from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


import io
import xml.etree.ElementTree as ET

import compas

if compas.is_ironpython():
    from urllib import addinfourl as ResponseType
    from compas.files.xml_cli import CLRXMLTreeParser as DefaultXMLTreeParser
    from compas.files.xml_cli import prettify_string
else:
    from http.client import HTTPResponse as ResponseType
    from xml.dom import minidom

    DefaultXMLTreeParser = ET.XMLParser

    def prettify_string(rough_string):
        """Return an XML string with added whitespace for legibility.

        Parameters
        ----------
        rough_string : str
            XML string
        """
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ", encoding='utf-8')


__all__ = [
    'prettify_string',
    'XML',
    'XMLReader',
    'XMLWriter',
    'XMLElement',
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
        self._root = None

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

    def write(self, prettify=False):
        """Writes the string representation of this XML instance,
        including all sub-elements, to the file path in the
        associated XML object.

        Parameters
        ----------
        prettify : bool, optional
            Whether the string should add whitespace for legibility.
            Defaults to ``False``.

        Returns
        -------
        ``None``

        """
        self.writer.write(prettify)

    def to_file(self, prettify=False):
        """Writes the string representation of this XML instance,
        including all sub-elements, to the file path in the
        associated XML object.

        Parameters
        ----------
        prettify : bool, optional
            Whether the string should add whitespace for legibility.
            Defaults to ``False``.

        Returns
        -------
        ``None``

        """
        self.write(prettify)

    @property
    def root(self):
        """Root element of the XML tree."""
        if self._root is None:
            self._root = self.reader.root
        return self._root

    @root.setter
    def root(self, value):
        self._root = value

    @classmethod
    def from_file(cls, source):
        """Read XML from a file path or file-like object.

        Parameters
        ----------
        source : str or file
            File path or file-like object.

        """
        xml = cls(source)
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

    def to_string(self, encoding='utf-8', prettify=False):
        """Generate a string representation of this XML instance,
        including all sub-elements.

        Parameters
        ----------
        encoding : str, optional
            Output encoding (the default is 'utf-8')
        prettify : bool, optional
            Whether the string should add whitespace for legibility.
            Defaults to ``False``.

        Returns
        -------
        str
            String representation of the XML.

        """
        return self.writer.to_string(encoding=encoding, prettify=prettify)

class TreeBuilderWithNamespaces(ET.TreeBuilder):
    def start(self, tag, attrs):
        if hasattr(self, '_current_namespaces') and len(self._current_namespaces):
            attrs.update(self._current_namespaces)

        element = super(TreeBuilderWithNamespaces, self).start(tag, attrs)

        # reset current namespaces
        self._current_namespaces = {}

        return element

    def start_ns(self, prefix, uri):
        if not hasattr(self, '_current_namespaces'):
            self._current_namespaces = {}

        ns_prefix = 'xmlns:' + prefix if prefix else 'xmlns'
        self._current_namespaces[ns_prefix] = uri

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
        target = TreeBuilderWithNamespaces()
        # If the source is an `HTTPResponse` (or `addinfourl` in ipy),
        # it cannot be read twice, so we first read the response into a byte stream.
        if isinstance(source, ResponseType):
            source = io.BytesIO(source.read())
        tree = ET.parse(source, tree_parser(target=target))
        return cls(tree.getroot())

    @classmethod
    def from_string(cls, text, tree_parser=None):
        tree_parser = tree_parser or DefaultXMLTreeParser
        target = TreeBuilderWithNamespaces()
        root = ET.fromstring(text, tree_parser(target=target))
        return cls(root)


class XMLWriter(object):
    """Writes an XML file from XML object.

    Parameters
    ----------
    xml : :class:`compas.files.XML`

    """
    def __init__(self, xml):
        self.xml = xml

    def write(self, prettify=False):
        string = self.to_string(prettify=prettify)
        with open(self.xml.filepath, 'wb') as f:
            f.write(string)

    def to_string(self, encoding='utf-8', prettify=False):
        rough_string = ET.tostring(self.xml.root, encoding=encoding, method='xml')
        if not prettify:
            return rough_string
        return prettify_string(rough_string)


class XMLElement(object):
    def __init__(self, tag, attributes=None, elements=None, text=None):
        self.tag = tag
        self.attributes = attributes or {}
        self.elements = elements or []
        self.text = text

    def get_root(self):
        root = ET.Element(self.tag, self.attributes)
        root.text = self.text
        return root

    def add_children(self, element):
        for child in self.elements:
            subelement = ET.SubElement(element, child.tag, child.attributes)
            subelement.text = child.text
            child.add_children(subelement)
