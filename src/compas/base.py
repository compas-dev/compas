from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import abc
import json
# from uuid import uuid4

from compas.utilities import DataEncoder
from compas.utilities import DataDecoder
from compas.utilities import abstractclassmethod

ABC = abc.ABCMeta('ABC', (object,), {'__slots__': ()})


__all__ = [
    'Base',
]


class Base(ABC):
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

    @property
    def DATASCHEMA(self):
        """:class:`schema.Schema` : The schema of the data of this object."""
        raise NotImplementedError

    @property
    def JSONSCHEMA(self):
        """dict : The schema of the JSON representation of the data of this object."""
        raise NotImplementedError

    # @property
    # def guid(self):
    #     if not self._guid:
    #         self._guid = uuid4()
    #     return self._guid

    # @property
    # def name(self):
    #     if not self._name:
    #         self._name = self.__class__.__name__
    #     return self._name

    # @name.setter
    # def name(self, name):
    #     self._name = name

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
        return self.DATASCHEMA.validate(data)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
