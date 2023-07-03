from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.geometry import Transformation
from .curve import Curve


class Conic(Curve):
    """Base class for curves that are conic sections."""

    # overwriting the __new__ method is necessary
    # to avoid triggering the plugin mechanism of the base curve class
    def __new__(cls, *args, **kwargs):
        curve = object.__new__(cls)
        curve.__init__(*args, **kwargs)
        return curve

    @property
    def eccentricity(self):
        raise NotImplementedError

    def transform(self, T):
        """
        Transform the curve.

        Parameters
        ----------
        T : :class:`compas.geometry.Transformation` | list[list[float]]
            The transformation.

        Returns
        -------
        None

        """
        self.frame.transform(T)
        self._transformation = Transformation.from_frame(self.frame)
