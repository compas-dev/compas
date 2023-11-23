from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

try:
    from typing import TypeVar  # noqa: F401
except ImportError:
    pass
else:
    G = TypeVar("G", bound="Geometry")

from compas.data import Data


class Geometry(Data):
    """Base class for all geometric objects."""

    def __init__(self, *args, **kwargs):
        super(Geometry, self).__init__(*args, **kwargs)

    def __eq__(self, other):
        raise NotImplementedError

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

    def transformed(self, transformation):  # type: (...) -> G
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
        geometry = self.copy()  # type: Geometry
        geometry.transform(transformation)
        return geometry  # type: ignore

    def scale(self, x, y=None, z=None):
        """Scale the geometry.

        Parameters
        ----------
        x : float
            The scaling factor in the x-direction.
        y : float, optional
            The scaling factor in the y-direction.
            Defaults to ``x``.
        z : float, optional
            The scaling factor in the z-direction.
            Defaults to ``x``.

        Returns
        -------
        None

        """
        from compas.geometry import Scale

        if y is None:
            y = x

        if z is None:
            z = x

        self.transform(Scale.from_factors([x, y, z]))

    def scaled(self, x, y=None, z=None):  # type: (...) -> G
        """Returns a scaled copy of this geometry.

        Parameters
        ----------
        x : float
            The scaling factor in the x-direction.
        y : float, optional
            The scaling factor in the y-direction.
            Defaults to ``x``.
        z : float, optional
            The scaling factor in the z-direction.
            Defaults to ``x``.

        Returns
        -------
        :class:`Geometry`
            The scaled geometry.

        """
        from compas.geometry import Scale

        if y is None:
            y = x

        if z is None:
            z = x

        return self.transformed(Scale.from_factors([x, y, z]))

    def translate(self, vector):
        """Translate the geometry.

        Parameters
        ----------
        vector : :class:`compas.geometry.Vector`
            The vector used to translate the geometry.

        Returns
        -------
        None

        """
        from compas.geometry import Translation

        self.transform(Translation.from_vector(vector))

    def translated(self, vector):  # type: (...) -> G
        """Returns a translated copy of this geometry.

        Parameters
        ----------
        vector : :class:`compas.geometry.Vector`
            The vector used to translate the geometry.

        Returns
        -------
        :class:`Geometry`
            The translated geometry.

        """
        from compas.geometry import Translation

        return self.transformed(Translation.from_vector(vector))

    def rotate(self, angle, axis=None, point=None):
        """Rotate the geometry.

        Parameters
        ----------
        angle : float
            The angle of rotation in radians.
        axis : :class:`compas.geometry.Vector`, optional
            The axis of rotation.
            Defaults to the z-axis.
        point : :class:`compas.geometry.Point`, optional
            The base point of the rotation axis.
            Defaults to the origin.

        Returns
        -------
        None

        """
        from compas.geometry import Rotation

        if axis is None:
            axis = [0.0, 0.0, 1.0]

        self.transform(Rotation.from_axis_and_angle(axis, angle, point))

    def rotated(self, angle, axis=None, point=None):  # type: (...) -> G
        """Returns a rotated copy of this geometry.

        Parameters
        ----------
        angle : float
            The angle of rotation in radians.
        axis : :class:`compas.geometry.Vector`, optional
            The axis of rotation.
            Defaults to the z-axis.
        point : :class:`compas.geometry.Point`, optional
            The base point of the rotation axis.
            Defaults to the origin.

        Returns
        -------
        :class:`Geometry`
            The rotated geometry.

        """
        from compas.geometry import Rotation

        if axis is None:
            axis = [0.0, 0.0, 1.0]

        return self.transformed(Rotation.from_axis_and_angle(axis, angle, point))
