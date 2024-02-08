from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

try:
    from typing import TypeVar  # noqa: F401
except ImportError:
    pass
else:
    G = TypeVar("G", bound="Datastructure")

from compas.data import Data


class Datastructure(Data):
    """Base class for all data structures."""

    def __init__(self, attributes=None, name=None):
        super(Datastructure, self).__init__(name=name)
        self.attributes = attributes or {}
        self._aabb = None
        self._obb = None

    @property
    def aabb(self):
        if self._aabb is None:
            self._aabb = self.compute_aabb()
        return self._aabb

    @property
    def obb(self):
        if self._obb is None:
            self._obb = self.compute_obb()
        return self._obb

    def compute_aabb(self):
        """Compute the axis-aligned bounding box of the datastructure.

        Returns
        -------
        :class:`compas.geometry.Box`

        """
        raise NotImplementedError

    def compute_obb(self):
        """Compute the oriented bounding box of the datastructure.

        Returns
        -------
        :class:`compas.geometry.Box`

        """
        raise NotImplementedError

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

    def scale(self, x, y=None, z=None):
        """Scale the datastructure.

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

        See Also
        --------
        scaled
        translate
        rotate
        transform

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

        See Also
        --------
        scale
        translated
        rotated
        transformed

        """
        from compas.geometry import Scale

        if y is None:
            y = x

        if z is None:
            z = x

        return self.transformed(Scale.from_factors([x, y, z]))

    def translate(self, vector):
        """Translate the datastructure.

        Parameters
        ----------
        vector : :class:`compas.geometry.Vector`
            The vector used to translate the datastructure.

        Returns
        -------
        None

        See Also
        --------
        translated
        rotate
        scale
        transform

        """
        from compas.geometry import Translation

        self.transform(Translation.from_vector(vector))

    def translated(self, vector):  # type: (...) -> G
        """Returns a translated copy of this geometry.

        Parameters
        ----------
        vector : :class:`compas.geometry.Vector`
            The vector used to translate the datastructure.

        Returns
        -------
        :class:`Geometry`
            The translated geometry.

        See Also
        --------
        translate
        rotated
        scaled
        transformed

        """
        from compas.geometry import Translation

        return self.transformed(Translation.from_vector(vector))

    def rotate(self, angle, axis=None, point=None):
        """Rotate the datastructure.

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

        See Also
        --------
        rotated
        translate
        scale
        transform

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

        See Also
        --------
        rotate
        translated
        scaled
        transformed

        """
        from compas.geometry import Rotation

        if axis is None:
            axis = [0.0, 0.0, 1.0]

        return self.transformed(Rotation.from_axis_and_angle(axis, angle, point))
