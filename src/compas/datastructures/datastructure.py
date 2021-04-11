from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
from copy import deepcopy

import compas
from compas.base import Base

__all__ = ['Datastructure']


class Datastructure(Base):

    def __init__(self):
        super(Datastructure, self).__init__()

    def __str__(self):
        """Generate a readable representation of the data of the datastructure."""
        return json.dumps(self.data, sort_keys=True, indent=4)

    @classmethod
    def from_data(cls, data):
        """Construct a datastructure from structured data.

        Parameters
        ----------
        data : dict
            The data dictionary.

        Returns
        -------
        :class:`compas.datastructures.Datastructure`
            An object of the type of ``cls``.

        Notes
        -----
        This constructor method is meant to be used in conjunction with the
        corresponding *to_data* method.

        """
        datastructure = cls()
        datastructure.data = data
        return datastructure

    def to_data(self):
        """Returns a dictionary of structured data representing the data structure.

        Returns
        -------
        dict
            The structured data.

        Notes
        ----
        This method produces the data that can be used in conjunction with the
        corresponding *from_data* class method.
        """
        return self.data

    @classmethod
    def from_json(cls, filepath):
        """Construct a datastructure from structured data contained in a json file.

        Parameters
        ----------
        filepath : path string, file-like object or URL string
            A path, a file-like object or a URL pointing to a file.

        Returns
        -------
        :class:`compas.datastructures.Datastructure`
            An object of the type of ``cls``.

        Notes
        -----
        This constructor method is meant to be used in conjunction with the
        corresponding *to_json* method.
        """
        data = compas.json_load(filepath)
        datastructure = cls()
        datastructure.data = data
        return datastructure

    def to_json(self, filepath, pretty=False):
        """Serialize the structured data representing the datastructure to json.

        Parameters
        ----------
        filepath : path string or file-like object
            A path, a file-like object or a URL pointing to a file.
        """
        compas.json_dump(self.data, filepath, pretty)

    def copy(self, cls=None):
        """Make an independent copy of the datastructure object.

        Parameters
        ----------
        cls : :class:`compas.datastructure.Datastructure`, optional
            The type of datastructure to return.
            Defaults to the type of the current datastructure.

        Returns
        -------
        :class:`compas.datastructure.Datastructure`
            A separate, but identical datastructure object.
        """
        if not cls:
            cls = type(self)
        return cls.from_data(deepcopy(self.data))


# ==============================================================================
#
# ==============================================================================

if __name__ == '__main__':
    pass
