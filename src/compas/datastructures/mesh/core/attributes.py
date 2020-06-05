from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

try:
    from collections.abc import MutableMapping  # python > 3.3
except ImportError:
    from collections import MutableMapping      # python 2.7


__all__ = ['VertexAttributeView', 'FaceAttributeView', 'EdgeAttributeView']


class AttributeView(object):
    """Mixin for attribute dict views."""

    def __init__(self, defaults, attr, key, custom_only=False):
        self.defaults = defaults
        self.attr = attr
        self.key = key
        self.custom_only = custom_only

    def __str__(self):
        s = []
        for k, v in self.items():
            s.append("{}: {}".format(repr(k), repr(v)))
        return "{" + ", ".join(s) + "}"

    def __len__(self):
        return len(self.defaults)

    def __getitem__(self, name):
        return self.attr[self.key].get(name) or self.defaults[name]

    def __setitem__(self, name, value):
        self.attr[self.key][name] = value

    def __delitem__(self, name):
        del self.attr[self.key][name]

    def __iter__(self):
        if self.custom_only:
            for name in self.attr[self.key]:
                yield name
        else:
            for name in self.defaults:
                yield name


class VertexAttributeView(AttributeView, MutableMapping):
    """Mutable Mapping that provides a read/write view of the custom attributes of a vertex
    combined with the default attributes of all vertices."""

    def __init__(self, defaults, attr, key, custom_only=False):
        super(VertexAttributeView, self).__init__(defaults, attr, key, custom_only)


class EdgeAttributeView(AttributeView, MutableMapping):
    """Mutable Mapping that provides a read/write view of the custom attributes of an edge
    combined with the default attributes of all edges."""

    def __init__(self, defaults, attr, key, custom_only=False):
        super(EdgeAttributeView, self).__init__(defaults, attr, key, custom_only)
        self.attr.setdefault(self.key, {})


class FaceAttributeView(AttributeView, MutableMapping):
    """Mutable Mapping that provides a read/write view of the custom attributes of a face
    combined with the default attributes of all faces."""

    def __init__(self, defaults, attr, key, custom_only=False):
        super(FaceAttributeView, self).__init__(defaults, attr, key, custom_only)
        self.attr.setdefault(self.key, {})


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    import doctest
    doctest.testmod(globs=globals())
