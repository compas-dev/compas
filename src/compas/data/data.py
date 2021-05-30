from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os
import json
from uuid import uuid4
from copy import deepcopy

import compas

from compas.data.encoders import DataEncoder
from compas.data.encoders import DataDecoder


__all__ = [
    'Data'
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
    dataschema : :class:`schema.Schema`
        The schema of the data dict.
    jsonschema : dict
        The schema of the serialized data dict.
    data : dict
        The fundamental data describing the object.
        The structure of the data dict is defined by the implementing classes.
    """

    def __init__(self, name=None):
        self._guid = None
        self._name = None
        self._jsondefinitions = None
        self._jsonschema = None
        self._jsonvalidator = None
        if name:
            self.name = name

    def __str__(self):
        """Generate a readable representation of the data of the object."""
        return json.dumps(self.data, sort_keys=True, indent=4)

    def __getstate__(self):
        """Return the object data for state serialization with older pickle protocols."""
        return {'__dict__': self.__dict__.copy(), 'dtype': self.dtype, 'data': self.data}

    def __setstate__(self, state):
        """Assign a deserialized state to the object data to support older pickle protocols."""
        self.__dict__.update(state['__dict__'])
        self.data = state['data']

    # def __copy__(self):
    #     pass

    # def __deepcopy__(self):
    #     pass

    @property
    def dataschema(self):
        """:class:`schema.Schema` : The schema of the data of this object."""
        raise NotImplementedError

    @property
    def jsonschema(self):
        """dict : The schema of the JSON representation of the data of this object."""
        if not self._jsonschema:
            schema_name = '{}.json'.format(self.__class__.__name__.lower())
            schema_path = os.path.join(os.path.dirname(__file__), 'schemas', schema_name)
            with open(schema_path, 'r') as fp:
                self._jsonschema = json.load(fp)
        return self._jsonschema

    @property
    def jsondefinitions(self):
        """dict : Reusable schema deinitions."""
        if not self._jsondefinitions:
            schema_path = os.path.join(os.path.dirname(__file__), 'schemas', 'compas.json')
            with open(schema_path, 'r') as fp:
                self._jsondefinitions = json.load(fp)
        return self._jsondefinitions

    @property
    def jsonvalidator(self):
        """:class:`jsonschema.Draft7Validator` : JSON schema validator for draft 7."""
        if not self._jsonvalidator:
            from jsonschema import RefResolver, Draft7Validator
            resolver = RefResolver.from_schema(self.jsondefinitions)
            self._jsonvalidator = Draft7Validator(self.jsonschema, resolver=resolver)
        return self._jsonvalidator

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
        raise NotImplementedError

    @property
    def jsonstring(self):
        """str: The representation of the object data in JSON format."""
        return compas.json_dumps(self.data)

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

    @classmethod
    def from_jsonstring(cls, string):
        """Construct an object from serialized data contained in a JSON string.

        Parameters
        ----------
        string : str
            The JSON string.

        Returns
        -------
        :class:`compas.data.Data`
            An object of the type of ``cls``.
        """
        data = compas.json_loads(string)
        return cls.from_data(data)

    def to_jsonstring(self, pretty=False):
        """Serialize the data representation of an object to a JSON string.

        Parameters
        ----------
        pretty : bool, optional
            If ``True`` serialize a pretty representation of the data.
            Default is ``False``.

        Returns
        -------
        str
            A JSON string representation of the data.
        """
        return compas.json_dumps(self.data, pretty)

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

    def validate_data(self):
        """Validate the object's data against its data schema (`self.dataschema`).

        Returns
        -------
        dict
            The validated data.

        Raises
        ------
        SchemaError
        """
        return self.dataschema.validate(self.data)

    def validate_json(self):
        """Validate the object's data against its json schema (`self.jsonschema`).

        Returns
        -------
        str
            The validated JSON representation of the data.

        Raises
        ------
        SchemaError
        """
        jsonstring = json.dumps(self.data, cls=DataEncoder)
        jsondata = json.loads(jsonstring, cls=DataDecoder)
        self.jsonvalidator.validate(jsondata)
        return jsonstring
