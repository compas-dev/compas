from typing import TYPE_CHECKING
from typing import Optional
from typing import Sequence

from typing_extensions import Self

from compas.data import Data

if TYPE_CHECKING:
    from compas.geometry import Box
    from compas.geometry import Transformation


class Geometry(Data):
    """Base class for all geometric objects."""

    def __init__(self, name: Optional[str] = None) -> None:
        super(Geometry, self).__init__(name=name)
        self._aabb: Optional["Box"] = None
        self._obb: Optional["Box"] = None

    def __eq__(self, other: object) -> bool:
        raise NotImplementedError

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    @property
    def aabb(self) -> "Box":
        if self._aabb is None:
            self._aabb = self.compute_aabb()
        return self._aabb

    @property
    def obb(self) -> "Box":
        if self._obb is None:
            self._obb = self.compute_obb()
        return self._obb

    def compute_aabb(self) -> "Box":
        """Compute the axis-aligned bounding box of the geometry.

        Returns
        -------
        Box

        """
        raise NotImplementedError

    def compute_obb(self) -> "Box":
        """Compute the oriented bounding box of the geometry.

        Returns
        -------
        Box

        """
        raise NotImplementedError

    def transform(self, transformation: "Transformation") -> None:
        """Transform the geometry.

        Parameters
        ----------
        transformation
            The transformation used to transform the geometry.

        See Also
        --------
        [`Geometry.transformed`][compas.geometry.Geometry.transformed]
        [`Geometry.translate`][compas.geometry.Geometry.translate]
        [`Geometry.rotate`][compas.geometry.Geometry.rotate]
        [`Geometry.scale`][compas.geometry.Geometry.scale]

        """
        raise NotImplementedError

    def transformed(self, transformation: "Transformation") -> Self:
        """Returns a transformed copy of this geometry.

        Parameters
        ----------
        transformation
            The transformation used to transform the geometry.

        Returns
        -------
        Self
            The transformed geometry.

        See Also
        --------
        [`Geometry.transform`][compas.geometry.Geometry.transform]
        [`Geometry.translated`][compas.geometry.Geometry.translated]
        [`Geometry.rotated`][compas.geometry.Geometry.rotated]
        [`Geometry.scaled`][compas.geometry.Geometry.scaled]

        """
        geometry = self.copy()
        geometry.transform(transformation)
        return geometry

    def scale(self, x: float, y: Optional[float] = None, z: Optional[float] = None) -> None:
        """Scale the geometry.

        Parameters
        ----------
        x
            The scaling factor in the x-direction.
        y
            The scaling factor in the y-direction.
            Defaults to `x`.
        z
            The scaling factor in the z-direction.
            Defaults to `x`.

        See Also
        --------
        [`Geometry.scaled`][compas.geometry.Geometry.scaled]
        [`Geometry.translate`][compas.geometry.Geometry.translate]
        [`Geometry.rotate`][compas.geometry.Geometry.rotate]
        [`Geometry.transform`][compas.geometry.Geometry.transform]

        """
        from compas.geometry import Scale

        if y is None:
            y = x

        if z is None:
            z = x

        self.transform(Scale.from_factors([x, y, z]))

    def scaled(self, x: float, y: Optional[float] = None, z: Optional[float] = None) -> Self:
        """Returns a scaled copy of this geometry.

        Parameters
        ----------
        x
            The scaling factor in the x-direction.
        y
            The scaling factor in the y-direction.
            Defaults to `x`.
        z
            The scaling factor in the z-direction.
            Defaults to `x`.

        Returns
        -------
        Self
            The scaled geometry.

        See Also
        --------
        [`Geometry.scale`][compas.geometry.Geometry.scale]
        [`Geometry.translated`][compas.geometry.Geometry.translated]
        [`Geometry.rotated`][compas.geometry.Geometry.rotated]
        [`Geometry.transformed`][compas.geometry.Geometry.transformed]

        """
        geometry = self.copy()
        geometry.scale(x=x, y=y, z=z)
        return geometry

    def translate(self, vector: Sequence[float]) -> None:
        """Translate the geometry.

        Parameters
        ----------
        vector
            The vector used to translate the geometry.

        See Also
        --------
        [`Geometry.translated`][compas.geometry.Geometry.translated]
        [`Geometry.rotate`][compas.geometry.Geometry.rotate]
        [`Geometry.scale`][compas.geometry.Geometry.scale]
        [`Geometry.transform`][compas.geometry.Geometry.transform]

        """
        from compas.geometry import Translation

        self.transform(Translation.from_vector(vector))

    def translated(self, vector: Sequence[float]) -> Self:
        """Returns a translated copy of this geometry.

        Parameters
        ----------
        vector
            The vector used to translate the geometry.

        Returns
        -------
        Self
            The translated geometry.

        See Also
        --------
        [`Geometry.translate`][compas.geometry.Geometry.translate]
        [`Geometry.rotated`][compas.geometry.Geometry.rotated]
        [`Geometry.scaled`][compas.geometry.Geometry.scaled]
        [`Geometry.transformed`][compas.geometry.Geometry.transformed]

        """
        geometry = self.copy()
        geometry.translate(vector)
        return geometry

    def rotate(self, angle: float, axis: Optional[Sequence[float]] = None, point: Optional[Sequence[float]] = None) -> None:
        """Rotate the geometry.

        Parameters
        ----------
        angle
            The angle of rotation in radians.
        axis
            The axis of rotation.
            Defaults to the z-axis.
        point
            The base point of the rotation axis.
            Defaults to the origin.

        See Also
        --------
        [`Geometry.rotated`][compas.geometry.Geometry.rotated]
        [`Geometry.translate`][compas.geometry.Geometry.translate]
        [`Geometry.scale`][compas.geometry.Geometry.scale]
        [`Geometry.transform`][compas.geometry.Geometry.transform]

        """
        from compas.geometry import Rotation

        if axis is None:
            axis = [0.0, 0.0, 1.0]

        self.transform(Rotation.from_axis_and_angle(axis, angle, point))

    def rotated(self, angle: float, axis: Optional[Sequence[float]] = None, point: Optional[Sequence[float]] = None) -> Self:
        """Returns a rotated copy of this geometry.

        Parameters
        ----------
        angle
            The angle of rotation in radians.
        axis
            The axis of rotation.
            Defaults to the z-axis.
        point
            The base point of the rotation axis.
            Defaults to the origin.

        Returns
        -------
        Self
            The rotated geometry.

        See Also
        --------
        [`Geometry.rotate`][compas.geometry.Geometry.rotate]
        [`Geometry.translated`][compas.geometry.Geometry.translated]
        [`Geometry.scaled`][compas.geometry.Geometry.scaled]
        [`Geometry.transformed`][compas.geometry.Geometry.transformed]

        """
        geometry = self.copy()
        geometry.rotate(angle=angle, axis=axis, point=point)
        return geometry
