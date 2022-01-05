from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.data import Data


class Collection(Data):

    __slots__ = ['_items']

    def __init__(self, items=None, **kwargs):
        super(Collection, self).__init__(**kwargs)
        self._items = []
        self.items = items

    # ==========================================================================
    # items
    # ==========================================================================

    @property
    def itype(self):
        raise NotImplementedError

    @property
    def items(self):
        return self._items

    @items.setter
    def items(self, items):
        raise NotImplementedError

    # ==========================================================================
    # data
    # ==========================================================================

    @property
    def DATASCHEMA(self):
        """:class:`schema.Schema` : Schema of the data representation."""
        import schema
        return schema.Schema({
            'items': None
        })

    @property
    def JSONSCHEMANAME(self):
        """str : Name of the schema of the data representation in JSON format."""
        raise NotImplementedError

    @property
    def data(self):
        """dict : The data dictionary that represents the circle."""
        return {'items': [item.data for item in self._items]}

    @data.setter
    def data(self, data):
        self._items = [self.itype.from_data(d) for d in data]

    @classmethod
    def from_data(cls, data):
        """Construct a circle from its data representation.

        Parameters
        ----------
        data : dict
            The data dictionary.

        Returns
        -------
        :class:`compas.geometry.Collection`
            The data collection.

        Examples
        --------
        >>> from compas.geometry import Circle
        >>> data = {'plane': {'point': [0.0, 0.0, 0.0], 'normal': [0.0, 0.0, 1.0]}, 'radius': 5.}
        >>> circle = Circle.from_data(data)

        """
        coll = cls()
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
        self._items[key] = value

    def __iter__(self):
        return iter(self._items)

    def __len__(self):
        return len(self._items)

    # ==========================================================================
    # constructors
    # ==========================================================================

    # ==========================================================================
    # methods
    # ==========================================================================

    def copy(self, cls=None):
        cls = cls or type(self)
        return cls(self.items)

    def transform(self, X):
        for item in self.items:
            item.transform(X)

    def transformed(self, X):
        collection = self.copy()
        collection.transform(X)
        return collection
