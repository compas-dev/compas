from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import xml.etree.ElementTree as ET
from compas.files import _iotools
from compas.files._xml.xml_cpython import prettify_string  # doesn't need special handling for pre-3.8 so we just import

__all__ = [
    'xml_from_file',
    'xml_from_string',
    'prettify_string',
]


def xml_from_file(source, tree_parser=None):
    if tree_parser:
        raise NotImplementedError('XML parsing on CPython 3.7 and older does not support a custom tree parser')

    tree_parser = ET.XMLPullParser
    parser = tree_parser(events=('start', 'start-ns'))

    with _iotools.open_file(source) as file:
        for data in _iotools.iter_file(file):
            parser.feed(data)
        return _process_all_events(parser)


def xml_from_string(text, tree_parser=None):
    if tree_parser:
        raise NotImplementedError('XML parsing on CPython 3.7 and older does not support a custom tree parser')

    tree_parser = ET.XMLPullParser
    parser = tree_parser(events=('start', 'end', 'start-ns', 'end-ns'))
    parser.feed(text)
    return _process_all_events(parser)


def _process_all_events(parser):
    root = None
    current_namespaces = {}

    for event, event_data in parser.read_events():
        if event == 'start':
            element = event_data
            if not root:
                root = element

            if len(current_namespaces):
                element.attrib.update(current_namespaces)

            current_namespaces = {}

        if event == 'start-ns':
            prefix, uri = event_data
            ns_prefix = 'xmlns:' + prefix if prefix else 'xmlns'
            current_namespaces[ns_prefix] = uri

    parser.close()

    return root
