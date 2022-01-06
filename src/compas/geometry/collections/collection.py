from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.data import Data
from compas.data.encoders import cls_from_dtype


class Collection(Data):
    """A collection of data is a mutable sequence of COMPAS data objects of the same type.

    Parameters
    ----------
    itype : Type[:class:`compas.geometry.Geometry`]
        The type of very item in the collection.
    items : sequence[:class:`compas.geometry.Geometry`], optional
        The items of the collection.
        These items can be instances of COMPAS geometry objects,
        or their Python built-in equivalent.

    Attributes
    ----------
    items : list[:class:`compas.geometry.Geometry`]
        The type of each item is the same as :attr:`itype`.

    Examples
    --------
    >>> from compas.geometry import Pointcloud, Line, Collection
    >>> from compas.utilities import pairwise

    Construct from list of items.

    >>> lines = []
    >>> for a, b in pairwise(Pointcloud.from_bounds(8, 5, 3, 31)):
    ...     lines.append([a, b])
    ...
    >>> collection = Collection(Line, lines)
    >>> collection
    '<Collection of 30 Line>'

    Construct with loop.

    >>> collection = Collection(Line)
    >>> for a, b in pairwise(Pointcloud.from_bounds(8, 5, 3, 31)):
    ...     collection.append([a, b])
    ...
    >>> collection
    '<Collection of 30 Line>'

    """

    __slots__ = ['_items']

    def __init__(self, itype, items=None, **kwargs):
        super(Collection, self).__init__(**kwargs)
        self._itype = itype
        self._items = []
        self.items = items

    # ==========================================================================
    # items
    # ==========================================================================

    @property
    def itype(self):
        return self._itype

    @property
    def items(self):
        return self._items

    @items.setter
    def items(self, items):
        if not items:
            return
        if not self._itype:
            raise Exception("Item type not set.")
        self._items = []
        for item in items:
            self.add(item)

    # ==========================================================================
    # data
    # ==========================================================================

    @property
    def DATASCHEMA(self):
        """schema.Schema : Schema of the data representation."""
        from schema import Schema
        return Schema({
            'itype': '.../...',
            'items': lambda item: 'validate schema?'
        })

    @property
    def JSONSCHEMANAME(self):
        """str : Name of the schema of the data representation in JSON format."""
        raise NotImplementedError

    @property
    def data(self):
        """dict : The data dictionary that represents the circle."""
        itype = '{}/{}'.format('.'.join(self.itype.__module__.split('.')[:2]), self.itype.__name__)
        return {'itype': itype, 'items': [item.data for item in self._items]}

    @data.setter
    def data(self, data):
        self._items = [self.itype.from_data(item) for item in data['items']]

    @classmethod
    def from_data(cls, data):
        """Construct a circle from its data representation.

        Parameters
        ----------
        data : dict
            The data dictionary.

        Returns
        -------
        :class:`compas.geometry.Collection[data['itype']]`
            The data collection.

        Examples
        --------
        >>> from compas.geometry import Circle
        >>> data = {'plane': {'point': [0.0, 0.0, 0.0], 'normal': [0.0, 0.0, 1.0]}, 'radius': 5.}
        >>> circle = Circle.from_data(data)

        """
        itype = cls_from_dtype(data['itype'])
        coll = cls(itype)
        coll.data = data
        return coll

    # ==========================================================================
    # properties
    # ==========================================================================

    # ==========================================================================
    # customization
    # ==========================================================================

    def __getitem__(self, key):
        if isinstance(key, slice):
            return [self._items[i] for i in range(*key.indices(len(self._items)))]
        return self._items[key]

    def __setitem__(self, key, value):
        if not isinstance(value, self._itype):
            value = self._itype(*value)
        self._items[key] = value

    def __delitem__(self, key):
        if isinstance(key, slice):
            n = len(self._items)
            start, stop, step = key.indices(n)
            indices = list(range(start, stop, step))
            if step > 0:
                indices[:] = indices[::-1]
            for i in indices:
                del self._items[i]
        else:
            del self._items[key]

    def __iter__(self):
        return iter(self._items)

    def __len__(self):
        return len(self._items)

    def __repr__(self):
        return "<Collection of {} {}>".format(len(self), self.itype.__name__)

    # ==========================================================================
    # constructors
    # ==========================================================================

    # ==========================================================================
    # methods
    # ==========================================================================

    def append(self, item):
        """Add an item at the end of the sequence of items contained by the list.

        Parameters
        ----------
        item : self.itype
            An item of the COMPAS geometry type of this Collection,
            or its Python built-in equivalent.

        Returns
        -------
        self.itype

        """
        if not isinstance(item, self._itype):
            item = self._itype(*item)
        self._items.append(item)
        return item

    def copy(self):
        """Make an independent copy of the collection and all the objects in it.

        Returns
        -------
        :class:`compas.geometry.Collection[self.itype]`

        """
        return Collection(self.itype, [item.copy() for item in self.items])

    def transform(self, X):
        """Transform all items in the collection.

        Parameters
        ----------
        X : list[list[float]] or :class:`compas.geometry.Transformation`

        Returns
        -------
        None

        """
        for item in self._items:
            item.transform(X)

    def transformed(self, X):
        """Return a transformed copy of this collection.

        Parameters
        ----------
        X : list[list[float]] or :class:`compas.geometry.Transformation`

        Returns
        -------
        :class:`compas.geometry.Collection[self.itype]`

        """
        collection = self.copy()
        collection.transform(X)
        return collection
