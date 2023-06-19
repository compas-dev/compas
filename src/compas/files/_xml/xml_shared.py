from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import xml.etree.ElementTree as ET

from compas import _iotools


def shared_xml_from_file(source, tree_parser, http_response_type):
    target = TreeBuilderWithNamespaces()
    with _iotools.open_file(source, "r") as f:
        tree = ET.parse(f, tree_parser(target=target))
    return tree.getroot()


def shared_xml_from_string(text, tree_parser):
    target = TreeBuilderWithNamespaces()
    root = ET.fromstring(text, tree_parser(target=target))
    return root


class TreeBuilderWithNamespaces(ET.TreeBuilder):
    def start(self, tag, attrs):
        if hasattr(self, "_current_namespaces") and len(self._current_namespaces):
            attrs.update(self._current_namespaces)

        element = super(TreeBuilderWithNamespaces, self).start(tag, attrs)

        # reset current namespaces
        self._current_namespaces = {}

        return element

    def start_ns(self, prefix, uri):
        if not hasattr(self, "_current_namespaces"):
            self._current_namespaces = {}

        ns_prefix = "xmlns:" + prefix if prefix else "xmlns"
        self._current_namespaces[ns_prefix] = uri
