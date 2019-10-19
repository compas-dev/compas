from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__all__ = ['Primitive']


class Primitive(object):
    """Base class for geometric primitives."""
    def __init__(self):
        pass

    @classmethod
    def from_data(cls, data):
        """Construct a primitive from its data representation.
        """
        raise NotImplementedError

    @property
    def data(self):
        """Returns the data dictionary that represents the primitive.

        Returns
        -------
        dict
            The primitive's data.
        """
        raise NotImplementedError

    @data.setter
    def data(self, data):
        raise NotImplementedError

    def to_data(self):
        """Returns the data dictionary that represents the primitive.

        Returns
        -------
        dict
            The primitive's data.
        """
        return self.data

    def copy(self):
        """Makes a copy of this primitive.

        Returns
        -------
        Primitive
            The copy.
        """
        raise NotImplementedError

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
