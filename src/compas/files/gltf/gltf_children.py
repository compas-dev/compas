from __future__ import print_function
from __future__ import division
from __future__ import absolute_import


class GLTFChildren(object):
    def __init__(self, context, value):
        self._value = list(value)
        self._context = context
        for v in value:
            self.check(v)

    def __repr__(self):
        return repr(self._value)

    def __iter__(self):
        return iter(self._value)

    def __len__(self):
        return len(self._value)

    def __bool__(self):
        return bool(self._value)

    def check(self, v):
        if v not in self._context.nodes:
            raise Exception('Cannot find Node {}.'.format(v))

    def append(self, value):
        self.check(value)
        self._value.append(value)

    def extend(self, values):
        for value in values:
            self.check(value)
        self._value.extend(values)

    def insert(self, index, value):
        self.check(value)
        self._value.insert(index, value)

    def remove(self, value):
        self._value.remove(value)

    def pop(self, index=None):
        self._value.pop(index or (len(self._value)-1))

    def clear(self):
        self._value.clear()

    def index(self, value, start=None, end=None):
        self._value.index(value, start or 0, end or (len(self._value)-1))

    def count(self, value):
        self._value.count(value)

    def sort(self, key=None, reverse=False):
        self._value.sort(key=key, reverse=reverse)

    def reverse(self):
        self._value.reverse()

    def copy(self):
        return self._value.copy()


class Children(object):
    def __init__(self, value):
        for v in value:
            self.check(v)
        self._value = value

    def __repr__(self):
        return repr(self._value)

    def __iter__(self):
        return iter(self._value)

    def __bool__(self):
        return bool(self._value)

    def check(self, v):
        if v not in [1, 2, 3]:
            raise Exception('Nope')

    def append(self, value):
        self.check(value)
        self._value.append(value)
