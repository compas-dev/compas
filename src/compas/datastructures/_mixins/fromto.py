from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import json

try:
    basestring
except NameError:
    basestring = str


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = [
    'FromToData',
    'FromToJson'
]


class FromToData(object):

    @classmethod
    def from_data(cls, data):
        """Construct a datastructure from structured data.

        Parameters
        ----------
        data : dict
            The data dictionary.

        Returns
        -------
        object
            An object of the type of ``cls``.

        Note
        ----
        This constructor method is meant to be used in conjuction with the
        corresponding *to_data* method.

        See Also
        --------
        * :meth:`to_data`

        """
        graph = cls()
        graph.data = data
        return graph

    def to_data(self):
        """Returns a dictionary of structured data representing the data structure.

        Returns
        -------
        dict
            The structured data.

        Note
        ----
        This method produces the data that can be used in conjuction with the
        corresponding *from_data* class method.

        See Also
        --------
        * :meth:`from_data`

        """
        return self.data


class FromToJson(object):

    @classmethod
    def from_json(cls, filepath):
        """Construct a datastructure from structured data contained in a json file.

        Parameters
        ----------
        filepath : str
            The path to the json file.

        Returns
        -------
        object
            An object of the type of ``cls``.

        Note
        ----
        This constructor method is meant to be used in conjuction with the
        corresponding *to_json* method.

        See Also
        --------
        * :meth:`to_json`

        """
        with open(filepath, 'r') as fp:
            data = json.load(fp)
        graph = cls()
        graph.data = data
        return graph

    def to_json(self, filepath):
        """Serialise the structured data representing the data structure to json.

        Parameters
        ----------
        filepath : str
            The path to the json file.

        See Also
        --------
        * :meth:`from_json`

        """
        with open(filepath, 'w+') as fp:
            json.dump(self.data, fp)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
