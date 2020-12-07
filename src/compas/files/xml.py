from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import xml.etree.ElementTree as ET

import compas

if not compas.IPY:
    if sys.version_info[0] >= 3 and sys.version_info[1] >= 8:
        from ._xml import xml_cpython as xml_impl
    else:
        from ._xml import xml_pre_38 as xml_impl
else:
    from ._xml import xml_cli as xml_impl


__all__ = [
    'prettify_string',
    'XML',
    'XMLReader',
    'XMLWriter',
    'XMLElement',
]

prettify_string = xml_impl.prettify_string


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
        return cls(xml_impl.xml_from_file(source, tree_parser))

    @classmethod
    def from_string(cls, text, tree_parser=None):
        return cls(xml_impl.xml_from_string(text, tree_parser))


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
        return xml_impl.prettify_string(rough_string)


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
