# -*- coding: UTF-8 -*-
#
# This module has been adapted from aglyph.compat.ipyetree
#
# MIT license
# Copyright (c) 2006-2016 Matthew Zipay <mattz@ninthtest.net>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""This module defines an :class:`xml.etree.ElementTree.XMLParser` that
delegates to the .NET `System.Xml.XmlReader
<http://msdn.microsoft.com/en-us/library/system.xml.xmlreader>`_ XML
parser to parse an XML document.

`IronPython <http://ironpython.net/>`_ is not able to load CPython's
:mod:`xml.parsers.expat` module, and so the default parser used by
ElementTree does not exist is most releases.
"""

from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import xml.etree.ElementTree as ET

import compas

try:
    import clr
    clr.AddReference('System.Xml')

    from System.IO import StringReader
    from System.Text.RegularExpressions import Regex
    from System.Text.RegularExpressions import RegexOptions
    from System.Xml import DtdProcessing
    from System.Xml import ValidationType
    from System.Xml import XmlNodeType
    from System.Xml import XmlReader
    from System.Xml import XmlReaderSettings

    CRE_ENCODING = Regex("encoding=['\"](?<enc_name>.*?)['\"]",
                        RegexOptions.Compiled)
except ImportError:
    compas.raise_if_ironpython()


__all__ = ['CLRXMLTreeParser']


class CLRXMLTreeParser(ET.XMLParser):
    """Parses XML using .NET infrastructure.

    This is a sub-class of :class:`xml.etree.ElementTree.XMLParser`
    that delegates parsing to the .NET `System.Xml.XmlReader
    <http://msdn.microsoft.com/en-us/library/system.xml.xmlreader>`_
    parser.

    Parameters
    ----------
    target : :class:`xml.etree.ElementTree.TreeBuilder`
        Target object (if omitted, a standard ``TreeBuilder`` instance is used)
    validating : bool
        ``True`` to use a validating parser, otherwise ``False``
    """

    def __init__(self, target=None, validating=False):
        if not compas.is_ironpython():
            raise Exception('CLRXMLTreeParser can only be used from IronPython')

        settings = XmlReaderSettings()
        settings.IgnoreComments = True
        settings.IgnoreProcessingInstructions = True
        settings.IgnoreWhitespace = True
        if not validating:
            settings.DtdProcessing = DtdProcessing.Ignore
            settings.ValidationType = getattr(ValidationType, 'None')
        else:
            settings.DtdProcessing = DtdProcessing.Parse
            settings.ValidationType = ValidationType.DTD
        self.settings = settings
        self._target = (target if (target is not None) else ET.TreeBuilder())
        self._buffer = []
        self._document_encoding = 'UTF-8'  # default

    def feed(self, data):
        """Add more XML data to be parsed.

        Parameters
        ----------
        data : str
            raw XML read from a stream

        Note
        ----
        All *data* across calls to this method are buffered
        internally; the parser itself is not actually created
        until the :meth:`close` method is called.

        """
        self._buffer.append(data)

    def close(self):
        """Parse the XML from the internal buffer to build an
        element tree.

        Returns
        -------
        :class:`xml.etree.ElementTree.ElementTree`
            The root element of the XML document
        """
        xml_string = "".join(self._buffer)
        self._buffer = None
        reader = XmlReader.Create(StringReader(xml_string), self.settings)
        while reader.Read():
            if reader.IsStartElement():
                self._start_element(reader)
            elif reader.NodeType in [XmlNodeType.Text, XmlNodeType.CDATA]:
                self._target.data(reader.Value.decode(self._document_encoding))
            elif reader.NodeType == XmlNodeType.EndElement:
                self._target.end(reader.LocalName)
            elif reader.NodeType == XmlNodeType.XmlDeclaration:
                self._parse_xml_declaration(reader.Value)
        return self._target.close()

    def _parse_xml_declaration(self, xml_decl):
        """Parse the document encoding from XML declaration."""
        enc_name = CRE_ENCODING.Match(xml_decl).Groups['enc_name'].Value

        if enc_name:
            self._document_encoding = enc_name

    def _start_element(self, reader):
        """Notify the tree builder that a start element has been
        encountered."""
        name = reader.LocalName
        attributes = {}

        while reader.MoveToNextAttribute():
            attributes[reader.Name] = reader.Value

        reader.MoveToElement()
        self._target.start(name, attributes)

        if (reader.IsEmptyElement):
            self._target.end(name)
