from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys
import xml.etree.ElementTree as ET

import compas

if not compas.IPY:
    if sys.version_info[0] >= 3 and sys.version_info[1] >= 8:
        from compas.files._xml import xml_cpython as xml_impl
    else:
        from compas.files._xml import xml_pre_38 as xml_impl
else:
    from compas.files._xml import xml_cli as xml_impl

prettify_string = xml_impl.prettify_string


class XML(object):
    """Class for working with XML files.

    This class simplifies reading XML files and strings
    across different Python implementations.

    Attributes
    ----------
    reader : :class:`compas.files.XMLReader`, read-only
        Reader used to process the XML file or string.
    writer : :class:`XMLWriter`, read-only
        Writer used to process the XML object to a file or string.
    filepath : str
        The path to the XML file.
    root : :class:`xml.etree.ElementTree.Element`
        Root element of the XML tree.

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

    @property
    def root(self):
        if self._root is None:
            self._root = self.reader.root
        return self._root

    @root.setter
    def root(self, value):
        self._root = value

    def read(self):
        """Read XML from a file path or file-like object,
        stored in the attribute ``filepath``.

        Returns
        -------
        None

        """
        self._reader = XMLReader.from_file(self.filepath)

    def write(self, prettify=False):
        """Writes the string representation of this XML instance,
        including all sub-elements, to the file path in the
        associated XML object.

        Parameters
        ----------
        prettify : bool, optional
            If True, prettify the string representation by adding whitespace and indentation.

        Returns
        -------
        None

        """
        self.writer.write(prettify)

    def to_file(self, prettify=False):
        """Writes the string representation of this XML instance,
        including all sub-elements, to the file path in the
        associated XML object.

        Parameters
        ----------
        prettify : bool, optional
            If True, prettify the string representation by adding whitespace and indentation.

        Returns
        -------
        None

        """
        self.write(prettify)

    @classmethod
    def from_file(cls, source):
        """Read XML from a file path or file-like object.

        Parameters
        ----------
        source : str | file
            File path or file-like object.

        Returns
        -------
        :class:`compas.files.XML`

        """
        xml = cls(source)
        xml._reader = XMLReader.from_file(source)
        return xml

    @classmethod
    def from_string(cls, text):
        """Read XML from a string.

        Parameters
        ----------
        text : str
            XML string.

        Returns
        -------
        :class:`compas.files.XML`

        """
        xml = cls()
        xml._reader = XMLReader.from_string(text)
        return xml

    def to_string(self, encoding="utf-8", prettify=False):
        """Generate a string representation of this XML instance,
        including all sub-elements.

        Parameters
        ----------
        encoding : str, optional
            Output encoding.
        prettify : bool, optional
            If True, prettify the string representation by adding whitespace and indentation.

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
        """Construct a reader from a source file.

        Parameters
        ----------
        source : path string | file-like object | URL string
            A path, a file-like object or a URL pointing to a file.
        tree_parser : :class:`ET.XMLParser`, optional
            A custom tree parser.

        Returns
        -------
        :class:`compas.files.XMLReader`

        """
        return cls(xml_impl.xml_from_file(source, tree_parser))

    @classmethod
    def from_string(cls, text, tree_parser=None):
        """Construct a reader from a source text.

        Parameters
        ----------
        text : str
            A string of text containing the XML source code.
        tree_parser : :class:`ET.XMLParser`, optional
            A custom tree parser.

        Returns
        -------
        :class:`compas.files.XMLReader`

        """
        return cls(xml_impl.xml_from_string(text, tree_parser))


class XMLWriter(object):
    """Writes an XML file from XML object.

    Parameters
    ----------
    xml : :class:`compas.files.XML`
        The XML tree to write.

    """

    def __init__(self, xml):
        self.xml = xml

    def write(self, prettify=False):
        """Write the meshes to the file.

        Parameters
        ----------
        prettify : bool, optional
            Prettify the xml text format.

        Returns
        -------
        None

        """
        string = self.to_string(prettify=prettify)
        with open(self.xml.filepath, "wb") as f:
            f.write(string)

    def to_string(self, encoding="utf-8", prettify=False):
        """Convert the XML element tree to a string.

        Parameters
        ----------
        encoding : str, optional
            The encoding to use for the conversion.
        prettify : bool, optional
            If True, prettify the string representation by adding whitespace and indentation.

        Returns
        -------
        str

        """
        rough_string = ET.tostring(self.xml.root, encoding=encoding, method="xml")
        if not prettify:
            return rough_string
        return xml_impl.prettify_string(rough_string)


class XMLElement(object):
    """Class representing an XML element in the tree.

    Parameters
    ----------
    tag : str
        The type of XML tag.
    attributes : dict[str, Any], optional
        The attributes of the tag as name-value pairs.
    elements : list[:class:`compas.files.XMLElement`], optional
        A list of elements contained by the current element.
    text : str, optional
        The text contained by the element.

    """

    def __init__(self, tag, attributes=None, elements=None, text=None):
        self.tag = tag
        self.attributes = attributes or {}
        self.elements = elements or []
        self.text = text

    def get_root(self):
        """Get the root element.

        Returns
        -------
        :class:`ET.Element`

        """
        root = ET.Element(self.tag, self.attributes)
        root.text = self.text
        return root

    def add_children(self, element):
        """Add children to an element.

        Parameters
        ----------
        element : :class:`ET.Element`
            The parent element.

        Returns
        -------
        None

        """
        for child in self.elements:
            subelement = ET.SubElement(element, child.tag, child.attributes)
            subelement.text = child.text
            child.add_children(subelement)
