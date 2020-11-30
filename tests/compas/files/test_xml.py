import os

import pytest

import compas
from compas.files import XML

BASE_FOLDER = os.path.dirname(__file__)


@pytest.fixture
def sample_file():
    return os.path.join(BASE_FOLDER, 'fixtures', 'sample.xml')


@pytest.fixture
def sample_xml():
    return "<Tests><Test id=\"1\"></Test></Tests>"


def test_xml_from_file(sample_file):
    xml = XML.from_file(sample_file)
    assert xml.root.tag == 'Tests'


def test_xml_from_string(sample_xml):
    xml = XML.from_string(sample_xml)
    assert xml.root.tag == 'Tests'


def test_xml_to_string(sample_xml):
    xml = XML.from_string(sample_xml)
    strxml = xml.to_string('utf-8')
    assert strxml.startswith(b'<Tests>')


def test_xml_to_pretty_string(sample_xml):
    xml = XML.from_string(sample_xml)
    prettyxml = xml.to_string(prettify=True)
    print(b"\n  " in prettyxml)


def test_namespaces_to_string():
    xml = XML.from_string(
        """<?xml version="1.0" encoding="UTF-8"?><robot xmlns:xacro="http://www.ros.org/wiki/xacro" name="panda"><xacro:bamboo/></robot>""")
    xml_string = xml.to_string(prettify=True)
    assert b'xmlns:xacro="http://www.ros.org/wiki/xacro"' in xml_string
    assert b'<xacro:bamboo' in xml_string or b'<ns0:bamboo' in xml_string
    # Note: Minidom does some funny things to namespaces.  First, if a namespace isn't used, it will be stripped out.
    # Second, it will include the original namespace declaration, but also repeat that declaration with another name,
    # and replace all references to the original with the new.
