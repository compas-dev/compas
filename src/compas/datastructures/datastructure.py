from typing import Any
from typing import Mapping
from typing import Optional
from typing import Sequence

from typing_extensions import Self

from compas.data import Data
from compas.geometry import Box
from compas.geometry import Transformation


class Datastructure(Data):
    """Base class for all data structures."""

    def __init__(
        self,
        attributes: Optional[Mapping[str, Any]] = None,
        name: Optional[str] = None,
    ) -> None:
        super().__init__(name=name)
        self.attributes = dict(attributes or {})
        self._aabb: Optional[Box] = None
        self._obb: Optional[Box] = None

    @property
    def __inheritance__(self) -> list[str]:
        """Get the inheritance chain of the datastructure.
        Until one level above the Datastructure class (eg. Mesh, Graph, ...).

        Returns
        -------
        list[str]
            The inheritance chain of the datastructure.

        """
        inheritance = []
        for cls in self.__class__.__mro__:
            if cls == self.__class__:
                continue
            if cls == Datastructure:
                break
            inheritance.append(cls.__clstype__())
        return inheritance

    def __jsondump__(self, minimal: bool = False) -> dict[str, Any]:
        """Return the required information for serialization with the COMPAS JSON serializer.

        Parameters
        ----------
        minimal
            If True, exclude the GUID from the dump dict.

        Returns
        -------
        dict

        """
        state = {
            "dtype": self.__dtype__,
            "data": self.__data__,
            "inheritance": self.__inheritance__,
        }
        if minimal:
            return state
        if self._name is not None:
            state["name"] = self._name
        state["guid"] = str(self.guid)
        return state

    @property
    def aabb(self) -> Box:
        if self._aabb is None:
            self._aabb = self.compute_aabb()
        return self._aabb

    @property
    def obb(self) -> Box:
        if self._obb is None:
            self._obb = self.compute_obb()
        return self._obb

    def to_points(self) -> list[list[float]]:
        """Return the points of the datastructure.

        Returns
        -------
        list[list[float]]
            The point coordinates.

        Raises
        ------
        NotImplementedError
            If the subclass does not implement this method.

        """
        raise NotImplementedError

    def compute_aabb(self) -> Box:
        """Compute the axis-aligned bounding box of the datastructure.

        Returns
        -------
        Box

        """
        from compas.geometry import Box
        from compas.geometry.bbox import bounding_box

        return Box.from_bounding_box(bounding_box(self.to_points()))

    def compute_obb(self) -> Box:
        """Compute the oriented bounding box of the datastructure.

        Returns
        -------
        Box

        """
        from compas.geometry import Box
        from compas.geometry.bbox_numpy import oriented_bounding_box_numpy

        return Box.from_bounding_box(oriented_bounding_box_numpy(self.to_points()))

    def transform(self, transformation: Transformation) -> None:
        """Transforms the data structure.

        Parameters
        ----------
        transformation
            The transformation used to transform the data structure.

        Returns
        -------
        None

        Raises
        ------
        NotImplementedError
            If the subclass does not implement this method.

        """
        raise NotImplementedError

    def transformed(self, transformation: Transformation) -> Self:
        """Returns a transformed copy of this data structure.

        Parameters
        ----------
        transformation
            The transformation used to transform the copy.

        Returns
        -------
        Datastructure
            The transformed copy.

        """
        datastructure = self.copy()
        datastructure.transform(transformation)
        return datastructure

    def transform_numpy(self, transformation: Any) -> None:
        """Transforms the data structure.

        Parameters
        ----------
        transformation
            The transformation used to transform the data structure.

        Returns
        -------
        None

        Raises
        ------
        NotImplementedError
            If the subclass does not implement this method.

        """
        raise NotImplementedError

    def transformed_numpy(self, transformation: Any) -> Self:
        """Returns a transformed copy of this data structure.

        Parameters
        ----------
        transformation
            The transformation used to transform the copy.

        Returns
        -------
        Datastructure
            The transformed copy.

        """
        datastructure = self.copy()
        datastructure.transform_numpy(transformation)
        return datastructure

    def scale(self, x: float, y: Optional[float] = None, z: Optional[float] = None) -> None:
        """Scale the datastructure.

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

    def scaled(self, x: float, y: Optional[float] = None, z: Optional[float] = None) -> Self:
        """Returns a scaled copy of this datastructure.

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
        Datastructure
            The scaled datastructure.

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

    def translate(self, vector: Sequence[float]) -> None:
        """Translate the datastructure.

        Parameters
        ----------
        vector
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

    def translated(self, vector: Sequence[float]) -> Self:
        """Returns a translated copy of this datastructure.

        Parameters
        ----------
        vector
            The vector used to translate the datastructure.

        Returns
        -------
        Datastructure
            The translated datastructure.

        See Also
        --------
        translate
        rotated
        scaled
        transformed

        """
        from compas.geometry import Translation

        return self.transformed(Translation.from_vector(vector))

    def rotate(
        self,
        angle: float,
        axis: Optional[Sequence[float]] = None,
        point: Optional[Sequence[float]] = None,
    ) -> None:
        """Rotate the datastructure.

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

    def rotated(
        self,
        angle: float,
        axis: Optional[Sequence[float]] = None,
        point: Optional[Sequence[float]] = None,
    ) -> Self:
        """Returns a rotated copy of this datastructure.

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
        Datastructure
            The rotated datastructure.

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
