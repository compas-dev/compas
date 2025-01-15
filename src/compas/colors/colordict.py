from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.data import Data

from .color import Color


class ColorDict(Data):
    """Class representing a dictionary of colors.

    Parameters
    ----------
    default : :class:`compas.colors.Color`
        The default color to use if the requested key is not in the dictionary.
    name : str, optional
        The name of the color dictionary.

    Attributes
    ----------
    default : :class:`compas.colors.Color`
        The default color to use if the requested key is not in the dictionary.

    """

    KEYMAP = {
        int: lambda x: str(x),
        tuple: lambda x: ",".join(map(str, sorted(x))),
        list: lambda x: ",".join(map(str, sorted(x))),
    }

    @property
    def __data__(self):
        return {
            "default": self.default,
            "dict": self._dict,
        }

    @classmethod
    def __from_data__(cls, data):
        colordict = cls(data["default"])
        colordict.update(data["dict"])
        return colordict

    def __init__(self, default, name=None):
        super(ColorDict, self).__init__(name=name)
        self._default = None
        self.default = default
        self._dict = {}

    @property
    def default(self):
        if not self._default:
            self._default = Color(0, 0, 0)
        return self._default

    @default.setter
    def default(self, default):
        if default and not isinstance(default, Color):
            default = Color.coerce(default)
        self._default = default

    def keymapper(self, key):
        if key.__class__ in self.KEYMAP:
            return self.KEYMAP[key.__class__](key)
        return key

    def __getitem__(self, key):
        return self._dict.get(self.keymapper(key), self.default)

    def __setitem__(self, key, value):
        self._dict[self.keymapper(key)] = Color.coerce(value)

    def __delitem__(self, key):
        del self._dict[self.keymapper(key)]

    def __iter__(self):
        return iter(self._dict)

    def __len__(self):
        return len(self._dict)

    def __contains__(self, key):
        return self.keymapper(key) in self._dict

    def items(self):
        return self._dict.items()

    def keys(self):
        return self._dict.keys()

    def values(self):
        return self._dict.values()

    def get(self, key, default=None):
        return self._dict.get(self.keymapper(key), default or self.default)

    def clear(self):
        """Clear the previously stored items.

        Returns
        -------
        None

        """
        self._dict = {}

    def update(self, other):
        """Update the dictionary with the items from another dictionary.

        Parameters
        ----------
        other : dict or :class:`compas.scene.ColorDict`
            The other dictionary.

        Returns
        -------
        None

        """
        for key, value in other.items():
            self[self.keymapper(key)] = value
