from __future__ import print_function
from __future__ import division
from __future__ import absolute_import


class GLTFChildren(object):
    def __init__(self, context, values):
        self._values = list(values)
        self._context = context
        for v in values:
            self.check_node_context(v)

    def __repr__(self):
        return repr(self._values)

    def __iter__(self):
        return iter(self._values)

    def __len__(self):
        return len(self._values)

    def __bool__(self):
        return bool(self._values)

    def check_node_context(self, v):
        if v not in self._context.nodes:
            raise Exception('Cannot find Node {}.'.format(v))

    def append(self, value):
        self.check_node_context(value)
        self._values.append(value)

    def extend(self, values):
        for value in values:
            self.check_node_context(value)
        self._values.extend(values)

    def insert(self, index, value):
        self.check_node_context(value)
        self._values.insert(index, value)

    def remove(self, value):
        self._values.remove(value)

    def pop(self, index=None):
        self._values.pop(index or (len(self._values) - 1))

    def clear(self):
        self._values.clear()

    def index(self, value, start=None, end=None):
        self._values.index(value, start or 0, end or (len(self._values) - 1))

    def count(self, value):
        self._values.count(value)

    def sort(self, key=None, reverse=False):
        self._values.sort(key=key, reverse=reverse)

    def reverse(self):
        self._values.reverse()

    def copy(self):
        return self._values.copy()
