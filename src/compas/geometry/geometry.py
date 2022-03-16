from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.data import Data


class Geometry(Data):
    """Base class for all geometric objects."""

    def __ne__(self, other):
        # this is not obvious to ironpython
        return not self.__eq__(other)

    def transform(self, transformation):
        """Transform the geometry.

        Parameters
        ----------
        transformation : :class:`~compas.geometry.Transformation`
            The transformation used to transform the geometry.

        Returns
        -------
        None

        """
        raise NotImplementedError

    def transformed(self, transformation):
        """Returns a transformed copy of this geometry.

        Parameters
        ----------
        transformation : :class:`~compas.geometry.Transformation`
            The transformation used to transform the geometry.

        Returns
        -------
        :class:`Geometry`
            The transformed geometry.

        """
        geometry = self.copy()
        geometry.transform(transformation)
        return geometry
