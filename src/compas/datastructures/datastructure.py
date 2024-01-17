from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.data import Data


class Datastructure(Data):
    """Base class for all data structures."""

    def __init__(self, **kwargs):
        super(Datastructure, self).__init__(**kwargs)
        self.attributes = kwargs

    def transform(self, transformation):
        """Transforms the data structure.

        Parameters
        ----------
        transformation : :class:`Transformation`
            The transformation used to transform the data structure.

        Returns
        -------
        None

        """
        raise NotImplementedError

    def transformed(self, transformation):
        """Returns a transformed copy of this data structure.

        Parameters
        ----------
        transformation : :class:`Transformation`
            The transformation used to transform the copy.

        Returns
        -------
        Datastructure
            The transformed copy.

        """
        datastructure = self.copy()
        datastructure.transform(transformation)
        return datastructure

    def transform_numpy(self, transformation):
        """Transforms the data structure.

        Parameters
        ----------
        transformation : :class:`Transformation`
            The transformation used to transform the data structure.

        Returns
        -------
        None

        """
        raise NotImplementedError

    def transformed_numpy(self, transformation):
        """Returns a transformed copy of this data structure.

        Parameters
        ----------
        transformation : :class:`Transformation`
            The transformation used to transform the copy.

        Returns
        -------
        Datastructure
            The transformed copy.

        """
        datastructure = self.copy()
        datastructure.transform_numpy(transformation)
        return datastructure
