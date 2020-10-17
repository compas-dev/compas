from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
from copy import deepcopy
from compas.base import Base
from compas.utilities import DataEncoder
from compas.utilities import DataDecoder


__all__ = ['Primitive']


class Primitive(Base):
    """Base class for geometric primitives."""

    def __init__(self):
        super(Primitive, self).__init__()

    @classmethod
    def from_json(cls, filepath):
        """Construct a primitive from structured data contained in a json file.

        Parameters
        ----------
        filepath : str
            The path to the json file.

        Returns
        -------
        object
            An object of the type of ``cls``.

        Notes
        -----
        This constructor method is meant to be used in conjunction with the
        corresponding *to_json* method.
        """
        with open(filepath, 'r') as fp:
            data = json.load(fp, cls=DataDecoder)
        return cls.from_data(data)

    def to_data(self):
        """Returns the data dictionary that represents the primitive.

        Returns
        -------
        dict
            The object's data.
        """
        return self.data

    def to_json(self, filepath):
        """Serialise the structured data representing the primitive to json.

        Parameters
        ----------
        filepath : str
            The path to the json file.
        """
        with open(filepath, 'w+') as f:
            json.dump(self.data, f, cls=DataEncoder)

    def copy(self):
        """Makes a copy of this primitive.

        Returns
        -------
        Primitive
            The copy.
        """
        cls = type(self)
        return cls.from_data(deepcopy(self.data))

    def transform(self, transformation):
        """Transform the primitive.

        Parameters
        ----------
        transformation : :class:`Transformation`
            The transformation used to transform the Box.

        Returns
        -------
        None

        """
        raise NotImplementedError

    def transformed(self, transformation):
        """Returns a transformed copy of this primitive.

        Parameters
        ----------
        transformation : :class:`Transformation`
            The transformation used to transform the primitive.

        Returns
        -------
        :class:`Primitive`
            The transformed primitive.
        """
        primitive = self.copy()
        primitive.transform(transformation)
        return primitive


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
