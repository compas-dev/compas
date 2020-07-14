from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import abc
import json
import jsonschema
import schema

from compas.utilities import DataEncoder
from compas.utilities import DataDecoder
from compas.utilities import abstractclassmethod

ABC = abc.ABCMeta('ABC', (object,), {'__slots__': ()})
# https://stackoverflow.com/questions/35673474/using-abc-abcmeta-in-a-way-it-is-compatible-both-with-python-2-7-and-python-3-5


__all__ = ['Base']


class Base(ABC):
    """Abstract base class for all COMPAS objects.

    Attributes
    ----------
    data : dict
        The fundamental data describing the object.
        The structure of the data dict is defined by the implementing classes.

    Class Attributes
    ----------------
    SCHEMA : dict
        The JSON schema

    """

    DATASCHEMA = schema.Schema({})
    JSONSCHEMA = {}

    def validate_data(self):
        self.DATASCHEMA.validate(self.data)

    def validate_data_to_json(self):
        jsondata = json.dump(self.data, cls=DataEncoder)
        jsonschema.validate(jsondata, schema=self.JSONSCHEMA)

    def validate_json_to_data(self):
        jsondata = json.dump(self.data, cls=DataEncoder)
        data = json.load(jsondata, cls=DataDecoder)
        return self.DATASCHEMA.validate(data)

    @abc.abstractproperty
    def data(self):
        pass

    @data.setter
    def data(self, data):
        pass

    @abstractclassmethod
    def from_data(cls, data):
        pass

    @abc.abstractmethod
    def to_data(self):
        pass

    @abstractclassmethod
    def from_json(cls, filepath):
        pass

    @abc.abstractmethod
    def to_json(self, filepath):
        pass


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
