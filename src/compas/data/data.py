from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import json
from uuid import uuid4
from copy import deepcopy

import compas

from compas.data.encoders import DataEncoder
from compas.data.encoders import DataDecoder


__all__ = [
    'Data',
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


class Data(object):
    """Abstract base class for all COMPAS data objects.

    Attributes
    ----------
    DATASCHEMA : :class:`schema.Schema`
        The schema of the data dict.
    JSONSCHEMA : dict
        The schema of the serialized data dict.
    data : dict
        The fundamental data describing the object.
        The structure of the data dict is defined by the implementing classes.
    """

    def __init__(self):
        self._guid = None
        self._name = None

    # def __str__(self):
    #     """Generate a readable representation of the data of the object."""
    #     return json.dumps(self.data, sort_keys=True, indent=4)

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
        """Construct an object of this type from the provided data.

        Parameters
        ----------
        data : dict
            The data dictionary.

        Returns
        -------
        :class:`compas.data.Data`
            An object of the type of ``cls``.

        """
        obj = cls()
        obj.data = data
        return obj

    def to_data(self):
        """Convert an object to its native data representation.

        Returns
        -------
        dict
            The data representation of the object as described by the schema.
        """
        return self.data

    @classmethod
    def from_json(cls, filepath):
        """Construct an object from serialized data contained in a JSON file.

        Parameters
        ----------
        filepath : path string, file-like object or URL string
            The path, file or URL to the file for serialization.

        Returns
        -------
        :class:`compas.data.Data`
            An object of the type of ``cls``.
        """
        data = compas.json_load(filepath)
        return cls.from_data(data)

    def to_json(self, filepath, pretty=False):
        """Serialize the data representation of an object to a JSON file.

        Parameters
        ----------
        filepath : path string or file-like object
            The path or file-like object to the file containing the data.
        pretty : bool, optional
            If ``True`` serialize a pretty representation of the data.
            Default is ``False``.
        """
        compas.json_dump(self.data, filepath, pretty)

    def copy(self, cls=None):
        """Make an independent copy of the data object.

        Parameters
        ----------
        cls : :class:`compas.data.Data`, optional
            The type of data object to return.
            Defaults to the type of the current data object.

        Returns
        -------
        :class:`compas.data.Data`
            A separate, but identical data object.
        """
        if not cls:
            cls = type(self)
        return cls.from_data(deepcopy(self.data))

    def __getstate__(self):
        """Return the object data for state serialization with older pickle protocols."""
        return {'__dict__': self.__dict__.copy(), 'dtype': self.dtype, 'data': self.data}

    def __setstate__(self, state):
        """Assign a deserialized state to the object data to support older pickle protocols."""
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
