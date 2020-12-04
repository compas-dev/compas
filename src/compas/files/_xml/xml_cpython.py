from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import xml.etree.ElementTree as ET
from http.client import HTTPResponse
from xml.dom import minidom

from .xml_shared import shared_xml_from_file
from .xml_shared import shared_xml_from_string

__all__ = [
    'xml_from_file',
    'xml_from_string',
    'prettify_string',
]


def prettify_string(rough_string):
    """Return an XML string with added whitespace for legibility.

    Parameters
    ----------
    rough_string : str
        XML string
    """
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ", encoding='utf-8')


def xml_from_file(source, tree_parser=None):
    tree_parser = tree_parser or ET.XMLParser
    return shared_xml_from_file(source, tree_parser, HTTPResponse)


def xml_from_string(text, tree_parser=None):
    tree_parser = tree_parser or ET.XMLParser
    return shared_xml_from_string(text, tree_parser)
