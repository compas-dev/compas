"""
********************************************************************************
base
********************************************************************************

.. currentmodule:: compas.base

Classes
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Base

"""
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import json
from uuid import uuid4

from compas.utilities import DataEncoder
from compas.utilities import DataDecoder


__all__ = [
    'Base',
]

# ==============================================================================
# If you ever feel tempted to use ABCMeta in your code: don't, just DON'T.
# Assigning __metaclass__ = ABCMeta to a class causes a severe memory leak/performance
# degradation on IronPython 2.7.

# See these issues for more details:
# - https://github.com/compas-dev/compas/issues/562
# - https://github.com/compas-dev/compas/issues/649

# ==============================================================================

# import abc
# ABC = abc.ABCMeta('ABC', (object,), {'__slots__': ()})


class Base(object):
    """Abstract base class for all COMPAS objects.

    Attributes
    ----------
    DATASCHEMA : :class:`schema.Schema`
        The schema of the data dict.
    JSONSCHEMA : dict
        The schema of the serialised data dict.
    data : dict
        The fundamental data describing the object.
        The structure of the data dict is defined by the implementing classes.
    """

    def __init__(self):
        self._guid = None
        self._name = None

    @property
    def DATASCHEMA(self):
        """:class:`schema.Schema` : The schema of the data of this object."""
        raise NotImplementedError

    @property
    def JSONSCHEMA(self):
        """dict : The schema of the JSON representation of the data of this object."""
        raise NotImplementedError

    @property
    def guid(self):
        """str : The globally unique identifier of the object."""
        if not self._guid:
            self._guid = uuid4()
        return self._guid

    @property
    def name(self):
        """str : The name of the object.

        This name is not necessarily unique and can be set by the user.
        """
        if not self._name:
            self._name = self.__class__.__name__
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def dtype(self):
        """str : The type of the object in the form of a "2-level" import and a class name."""
        return "{}/{}".format(".".join(self.__class__.__module__.split(".")[:2]), self.__class__.__name__)

    @property
    def data(self):
        """dict : The representation of the object as native Python data.

        The structure of the data is described by the data schema.
        """
        raise NotImplementedError

    @data.setter
    def data(self, data):
        pass

    @classmethod
    def from_data(cls, data):
        """Construct an object of this type from the provided data."""
        raise NotImplementedError

    def to_data(self):
        """Convert an object to its native data representation.

        Returns
        -------
        dict
            The data representation of the object as described by the schema.
        """
        raise NotImplementedError

    @classmethod
    def from_json(cls, filepath):
        """Construct an object from serialised data contained in a JSON file.

        Parameters
        ----------
        filepath : str
            The path to the file for serialisation.
        """
        raise NotImplementedError

    def to_json(self, filepath):
        """Serialize the data representation of an object to a JSON file.

        Parameters
        ----------
        filepath : str
            The path to the file containing the data.
        """
        raise NotImplementedError

    def __getstate__(self):
        """Return the object data for state state serialisation with older pickle protocols."""
        return {'__dict__': self.__dict__.copy(), 'dtype': self.dtype, 'data': self.data}

    def __setstate__(self, state):
        """Assign an unserialised state to the object data to support older pickle protocols."""
        self.__dict__.update(state['__dict__'])
        self.data = state['data']

    def validate_data(self):
        """Validate the data of this object against its data schema (`self.DATASCHEMA`).

        Returns
        -------
        dict
            The validated data.

        Raises
        ------
        SchemaError
        """
        return self.DATASCHEMA.validate(self.data)

    def validate_json(self):
        """Validate the data loaded from a JSON representation of the data of this object against its data schema (`self.DATASCHEMA`).

        Returns
        -------
        None

        Raises
        ------
        SchemaError
        """
        import jsonschema
        jsondata = json.dumps(self.data, cls=DataEncoder)
        data = json.loads(jsondata, cls=DataDecoder)
        jsonschema.validate(data, schema=self.JSONSCHEMA)
        self.data = data
        return self.DATASCHEMA.validate(self.data)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
