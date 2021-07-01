from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.data import Data


class Primitive(Data):
    """Base class for geometric primitives."""

    def __ne__(self, other):
        # this is not obvious to ironpython
        return not self.__eq__(other)

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
