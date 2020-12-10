from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.datastructures._mutablemapping import MutableMapping

__all__ = [
    'NodeAttributeView',
    'VertexAttributeView',
    'FaceAttributeView',
    'EdgeAttributeView',
    'CellAttributeView',
]


class AttributeView(MutableMapping):
    """Base class for attribute dict views."""

    def __init__(self, defaults, attr, custom_only=False):
        super(AttributeView, self).__init__()
        self.defaults = defaults
        self.attr = attr
        self.custom_only = custom_only

    def __str__(self):
        s = []
        for k, v in self.items():
            s.append("{}: {}".format(repr(k), repr(v)))
        return "{" + ", ".join(s) + "}"

    def __len__(self):
        return len(set(self.defaults).union(self.attr))

    def __getitem__(self, name):
        if name not in self.attr:
            if name not in self.defaults:
                raise KeyError
        return self.attr.get(name, self.defaults.get(name))

    def __setitem__(self, name, value):
        self.attr[name] = value

    def __delitem__(self, name):
        del self.attr[name]

    def __iter__(self):
        if self.custom_only:
            for name in self.attr:
                yield name
        else:
            names = set(self.defaults).union(self.attr)
            for name in names:
                yield name


class NodeAttributeView(AttributeView):
    """Mutable Mapping that provides a read/write view of the custom attributes of a node
    combined with the default attributes of all nodes."""

    def __init__(self, defaults, attr, custom_only=False):
        super(NodeAttributeView, self).__init__(defaults, attr, custom_only)


class VertexAttributeView(AttributeView):
    """Mutable Mapping that provides a read/write view of the custom attributes of a vertex
    combined with the default attributes of all vertices."""

    def __init__(self, defaults, attr, custom_only=False):
        super(VertexAttributeView, self).__init__(defaults, attr, custom_only)


class EdgeAttributeView(AttributeView):
    """Mutable Mapping that provides a read/write view of the custom attributes of an edge
    combined with the default attributes of all edges."""

    def __init__(self, defaults, attr, custom_only=False):
        super(EdgeAttributeView, self).__init__(defaults, attr, custom_only)


class FaceAttributeView(AttributeView):
    """Mutable Mapping that provides a read/write view of the custom attributes of a face
    combined with the default attributes of all faces."""

    def __init__(self, defaults, attr, custom_only=False):
        super(FaceAttributeView, self).__init__(defaults, attr, custom_only)


class CellAttributeView(AttributeView):
    """Mutable Mapping that provides a read/write view of the custom attributes of a cell
    combined with the default attributes of all faces."""

    def __init__(self, defaults, attr, custom_only=False):
        super(CellAttributeView, self).__init__(defaults, attr, custom_only)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    import doctest
    doctest.testmod(globs=globals())
