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


@pytest.fixture
def sample_with_nested_default_ns():
    return os.path.join(BASE_FOLDER, 'fixtures', 'sample_with_nested_default_ns.xml')


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
    assert b"\n  " in prettyxml


def test_namespaces_to_string():
    xml = XML.from_string(
        """<?xml version="1.0" encoding="UTF-8"?><robot xmlns:xacro="http://www.ros.org/wiki/xacro" name="panda"><xacro:bamboo/></robot>""")
    xml_string = xml.to_string(prettify=True)
    assert b'xmlns:xacro="http://www.ros.org/wiki/xacro"' in xml_string
    assert b'<xacro:bamboo' in xml_string or b'<ns0:bamboo' in xml_string
    # Note: Minidom does some funny things to namespaces.  First, if a namespace isn't used, it will be stripped out.
    # Second, it will include the original namespace declaration, but also repeat that declaration with another name,
    # and replace all references to the original with the new.


def test_default_namespace_to_string():
    xml = XML.from_string(
        """<?xml version="1.0" encoding="UTF-8"?><robot xmlns="https://default.org/namespace" xmlns:xacro="http://www.ros.org/wiki/xacro" name="panda"><xacro:bamboo/></robot>"""
    )
    xml_string = xml.to_string(prettify=True)
    assert b'xmlns="https://default.org/namespace"' in xml_string
    assert b'<xacro:bamboo' in xml_string or b'<ns1:bamboo' in xml_string
    assert b'<robot' in xml_string or b'<ns0:robot' in xml_string


def test_nested_default_namespaces():
    xml = XML.from_string(
        """<?xml version="1.0"?>
        <main xmlns="https://ita.arch.ethz.ch/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" name="test-xml">
            <item name="item1"><subitem /></item>
            <item xmlns="https://ethz.ch" name="item2"><subitem /></item>
        </main>"""
    )

    assert xml.root.attrib['xmlns'] == 'https://ita.arch.ethz.ch/'
    assert xml.root.attrib['xmlns:xsi'] == 'http://www.w3.org/2001/XMLSchema-instance'

    # first element redefines default namespace
    assert list(xml.root)[1].attrib['xmlns'] == 'https://ethz.ch'
    assert list(xml.root)[1].attrib['name'] == 'item2'


# This is the same test as above, but the code paths of loading from file vs from string are different on pre-3.8 cpython
def test_nested_default_namespaces_from_file(sample_with_nested_default_ns):
    xml = XML.from_file(sample_with_nested_default_ns)

    assert xml.root.attrib['xmlns'] == 'https://ita.arch.ethz.ch/'
    assert xml.root.attrib['xmlns:xsi'] == 'http://www.w3.org/2001/XMLSchema-instance'

    # first element redefines default namespace
    assert list(xml.root)[1].attrib['xmlns'] == 'https://ethz.ch'
    assert list(xml.root)[1].attrib['name'] == 'item2'


def test_no_root_default_namespace():
    xml = XML.from_string(
        """<?xml version="1.0"?>
        <main name="test-xml">
            <item name="item1"><subitem /></item>
            <item xmlns="https://ethz.ch" name="item2"><subitem /></item>
        </main>"""
    )

    assert not xml.root.attrib.get('xmlns')
    assert list(xml.root)[1].attrib['xmlns'] == 'https://ethz.ch'
    assert list(xml.root)[1].attrib['name'] == 'item2'


def test_no_default_namespace():
    xml = XML.from_string(
        """<?xml version="1.0"?><main name="test-xml"></main>"""
    )

    assert not xml.root.attrib.get('xmlns')
    assert xml.root.attrib['name'] == 'test-xml'


def test_namespace_expansion():
    xml = XML.from_string(
        """<?xml version="1.0"?>
        <main xmlns="https://ethz.ch" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" name="test-xml">
            <item>
                <subitem xmlns:magic="https://sub.ethz.ch">
                    <magic:cat />
                </subitem>
            </item>
        </main>"""
    )

    assert xml.root.tag == '{https://ethz.ch}main'
    assert list(xml.root)[0].tag == '{https://ethz.ch}item'
    assert list(list(xml.root)[0])[0].tag == '{https://ethz.ch}subitem'
    assert list(list(list(xml.root)[0])[0])[0].tag == '{https://sub.ethz.ch}cat'
