from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import json

try:
    basestring
except NameError:
    basestring = str


__all__ = [
    'FromToData',
    'FromToJson',
    'FromToPickle',
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

        """
        with open(filepath, 'w+') as fp:
            json.dump(self.data, fp)


class FromToPickle(object):

    @classmethod
    def from_pickle(cls, filepath):
        """Construct a datastructure from serialised data contained in a pickle file.

        Parameters
        ----------
        filepath : str
            The path to the pickle file.

        Returns
        -------
        object
            An object of type ``cls``.

        Note
        ----
        This constructor method is meant to be used in conjuction with the
        corresponding *to_pickle* method.

        """
        o = cls()
        o.load(filepath)
        return o

    def to_pickle(self, filepath):
        """Serialised the structured data representing the data structure to a pickle file.

        Parameters
        ----------
        filepath : str
            The path to the pickle file.

        """
        self.dump(filepath)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
