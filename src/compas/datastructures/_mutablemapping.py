"""
The module contains vendored copies of a couple of classes from collections.abc
(python standard library) with one fundamental change:

 * The Mapping class does not have a __metaclass__ = ABCMeta set
   because this causes performance issues on IronPython 2.7.x

See these issues for more details:
 - https://github.com/compas-dev/compas/issues/562
 - https://github.com/compas-dev/compas/issues/649

Notes
-----
The decision to avoid abstract base classes and metaclasses should be revisited.
It was made to work around performance and compatibility problems in IronPython
2.7, but those constraints no longer apply as support for Python 2.7-era
environments is phased out.
"""

import collections.abc as stdlib_collections
from typing import Any
from typing import Generic
from typing import Iterator
from typing import Optional
from typing import TypeVar
from typing import Union
from typing import overload

K = TypeVar("K")
V = TypeVar("V")
T = TypeVar("T")


class Mapping(Generic[K, V]):
    """A Mapping is a generic container for associating key/value
    pairs.
    This class provides concrete generic implementations of all
    methods except for __getitem__, __iter__, and __len__.
    """

    __slots__ = ()

    def __getitem__(self, key: K) -> V:
        raise NotImplementedError

    def __iter__(self) -> Iterator[K]:
        raise NotImplementedError

    def __len__(self) -> int:
        raise NotImplementedError

    @overload
    def get(self, key: K) -> Optional[V]: ...

    @overload
    def get(self, key: K, default: T) -> Union[V, T]: ...

    def get(self, key: K, default: Any = None) -> Any:
        """D.get(k[,d]) => D[k] if k in D, else d.  d defaults to None."""
        try:
            return self[key]
        except KeyError:
            return default

    def __contains__(self, key: Any) -> bool:
        try:
            self[key]
        except KeyError:
            return False
        else:
            return True

    def keys(self) -> stdlib_collections.KeysView[K]:
        """D.keys() => a set-like object providing a view on D's keys"""
        return stdlib_collections.KeysView(self)

    def items(self) -> stdlib_collections.ItemsView[K, V]:
        """D.items() => a set-like object providing a view on D's items"""
        return stdlib_collections.ItemsView(self)

    def values(self) -> stdlib_collections.ValuesView[V]:
        """D.values() => an object providing a view on D's values"""
        return stdlib_collections.ValuesView(self)

    def __eq__(self, other: object) -> Any:
        if not isinstance(other, (Mapping, stdlib_collections.Mapping)):
            return NotImplemented
        return dict(self.items()) == dict(other.items())

    __reversed__ = None


class MutableMapping(Mapping[K, V]):
    """A MutableMapping is a generic container for associating
    key/value pairs.
    This class provides concrete generic implementations of all
    methods except for __getitem__, __setitem__, __delitem__,
    __iter__, and __len__.
    """

    __slots__ = ()

    __marker = object()

    def __setitem__(self, key: K, value: V) -> None:
        raise NotImplementedError

    def __delitem__(self, key: K) -> None:
        raise NotImplementedError

    @overload
    def pop(self, key: K) -> V: ...

    @overload
    def pop(self, key: K, default: T) -> Union[V, T]: ...

    def pop(self, key: K, default: Any = __marker) -> Any:
        """D.pop(k[,d]) => v, remove specified key and return the corresponding value.
        If key is not found, d is returned if given, otherwise KeyError is raised.
        """
        try:
            value = self[key]
        except KeyError:
            if default is self.__marker:
                raise
            return default
        else:
            del self[key]
            return value

    def popitem(self) -> tuple[K, V]:
        """D.popitem() => (k, v), remove and return some (key, value) pair
        as a 2-tuple; but raise KeyError if D is empty.
        """
        try:
            key = next(iter(self))
        except StopIteration:
            raise KeyError
        value = self[key]
        del self[key]
        return key, value

    def clear(self) -> None:
        """D.clear() => None.  Remove all items from D."""
        try:
            while True:
                self.popitem()
        except KeyError:
            pass

    def update(*args: Any, **kwargs: V) -> None:
        """D.update([E, ]**F) => None.  Update D from mapping/iterable E and F.

        If E present and has a .keys() method, does: for k in E: D[k] = E[k]
        If E present and lacks .keys() method, does: for (k, v) in E: D[k] = v
        In either case, this is followed by: for k, v in F.items(): D[k] = v
        """
        if not args:
            raise TypeError("'update' of 'MutableMapping' object needs an argument")
        self = args[0]
        args = args[1:]
        if len(args) > 1:
            raise TypeError("update expected at most 1 arguments, got %d" % len(args))
        if args:
            other = args[0]
            if isinstance(other, (Mapping, stdlib_collections.Mapping)):
                for key in other:
                    self[key] = other[key]
            elif hasattr(other, "keys"):
                for key in other.keys():
                    self[key] = other[key]
            else:
                for key, value in other:
                    self[key] = value
        for key, value in kwargs.items():
            self[key] = value

    @overload
    def setdefault(self, key: K) -> Optional[V]: ...

    @overload
    def setdefault(self, key: K, default: T) -> Union[V, T]: ...

    def setdefault(self, key: K, default: Any = None) -> Any:
        """D.setdefault(k[,d]) => D.get(k,d), also set D[k]=d if k not in D"""
        try:
            return self[key]
        except KeyError:
            self[key] = default
        return default
