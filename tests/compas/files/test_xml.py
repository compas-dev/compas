from io import BytesIO
from io import StringIO
import os
import xml.etree.ElementTree as ET

import pytest

from compas.files import parse_xml
from compas.files import read_xml
from compas.files import write_xml
from compas.files import xml_to_string

BASE_FOLDER = os.path.dirname(__file__)


@pytest.fixture
def basic_xml():
    return '<Tests><Test id="1"></Test></Tests>'


@pytest.fixture
def basic_file():
    return os.path.join(BASE_FOLDER, "fixtures", "xml", "basic.xml")


@pytest.fixture
def basic_file_url():
    return "https://raw.githubusercontent.com/compas-dev/compas/main/tests/compas/files/fixtures/xml/basic.xml"


@pytest.fixture
def namespaces_file():
    return os.path.join(BASE_FOLDER, "fixtures", "xml", "namespaces.xml")


def test_read_xml_from_file(basic_file):
    root = read_xml(basic_file)

    assert root.tag == "Tests"


def test_read_xml_from_url(basic_file_url):
    root = read_xml(basic_file_url)

    assert root.tag == "Tests"


def test_read_xml_from_stream(basic_xml):
    root = read_xml(StringIO(basic_xml))

    assert root.tag == "Tests"


def test_parse_xml_from_string(basic_xml):
    root = parse_xml(basic_xml)

    assert root.tag == "Tests"


def test_xml_to_string_returns_text_by_default(basic_xml):
    root = parse_xml(basic_xml)

    result = xml_to_string(root)

    assert isinstance(result, str)
    assert result.startswith("<Tests>")


def test_xml_to_string_can_return_bytes(basic_xml):
    root = parse_xml(basic_xml)

    result = xml_to_string(root, encoding="utf-8")

    assert isinstance(result, bytes)
    assert result.startswith(b"<Tests>")


def test_xml_to_string_pretty_prints_without_mutating_root(basic_xml):
    root = parse_xml(basic_xml)

    result = xml_to_string(root, pretty=True)

    assert "\n  " in result
    assert root[0].tail is None


def test_write_xml_supports_binary_streams(basic_xml):
    stream = BytesIO()

    write_xml(stream, parse_xml(basic_xml), pretty=True)

    assert stream.getvalue().startswith(b"<Tests>")


def test_write_xml_supports_text_streams(basic_xml):
    stream = StringIO()

    write_xml(stream, parse_xml(basic_xml))

    assert stream.getvalue().startswith("<Tests>")


def test_standard_namespace_expansion():
    root = parse_xml(
        """<?xml version="1.0"?>
        <main xmlns="https://ethz.ch" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
            <item><subitem xmlns:magic="https://sub.ethz.ch"><magic:cat /></subitem></item>
        </main>"""
    )

    assert root.tag == "{https://ethz.ch}main"
    assert root[0].tag == "{https://ethz.ch}item"
    assert root[0][0].tag == "{https://ethz.ch}subitem"
    assert root[0][0][0].tag == "{https://sub.ethz.ch}cat"
    assert "xmlns" not in root.attrib


def test_namespace_semantics_survive_roundtrip(namespaces_file):
    root = read_xml(namespaces_file)
    restored = ET.fromstring(xml_to_string(root, encoding="utf-8"))

    assert restored.tag == "{https://ethz.ch}main"
    assert restored[0].tag == "{https://ethz.ch}item"
    assert restored[0][0][0].tag == "{https://sub.ethz.ch}cat"
