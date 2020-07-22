from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.base import DataBaseClass

__all__ = ['Primitive']


class Primitive(DataBaseClass):
    """Base class for geometric primitives."""

    __slots__ = []

    def __init__(self):
        super(Primitive, self).__init__()

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
