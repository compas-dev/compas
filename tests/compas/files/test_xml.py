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
