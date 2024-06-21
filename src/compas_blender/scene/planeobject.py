from typing import Any
from typing import Optional

import bpy  # type: ignore

from compas.colors import Color
from compas.geometry import Frame
from compas.geometry import Line
from compas.scene import GeometryObject
from compas_blender import conversions

from .sceneobject import BlenderSceneObject


class PlaneObject(BlenderSceneObject, GeometryObject):
    """Scene object for drawing planes in Blender.

    Parameters
    ----------
    scale : float, optional
        Scale of the plane.
    **kwargs : dict, optional
        Additional keyword arguments.
        For more info,
        see :class:`compas_blender.scene.BlenderSceneObject` and :class:`compas.scene.GeometryObject`.

    Attributes
    ----------
    scale : float
        Scale of the plane.

    """

    def __init__(self, scale=1.0, **kwargs: Any):
        super().__init__(**kwargs)
        self.scale = scale

    def draw(self, color: Optional[Color] = None, collection: Optional[str] = None) -> list[bpy.types.Object]:
        """Draw the plane.

        Parameters
        ----------
        color : tuple[float, float, float] | tuple[int, int, int] | :class:`compas.colors.Color`, optional
            The RGB color of the plane.
        collection : str, optional
            The Blender scene collection containing the created objects.

        Returns
        -------
        list[:blender:`bpy.types.Object`]
            The objects created in Blender.
        """

        objects = []
        color = Color.coerce(color) or self.color

        frame = Frame.from_plane(self._item)
        normal = Line(frame.to_world_coordinates([0, 0, 0]), frame.to_world_coordinates([0, 0, self.scale]))
        curve = conversions.line_to_blender_curve(normal)
        objects = [self.create_object(curve, name=self.geometry.name + ".normal")]

        vertices = [
            frame.to_world_coordinates([-self.scale, -self.scale, 0]),
            frame.to_world_coordinates([self.scale, -self.scale, 0]),
            frame.to_world_coordinates([self.scale, self.scale, 0]),
            frame.to_world_coordinates([-self.scale, self.scale, 0]),
        ]
        faces = [[0, 1, 2, 3]]
        mesh = conversions.vertices_and_faces_to_blender_mesh(vertices, faces)

        obj = self.create_object(mesh, name=self.geometry.name)
        objects.append(obj)

        for obj in objects:
            self.update_object(obj, color=color, collection=collection, show_wire=True)

        self._guids = objects
        return self.guids
