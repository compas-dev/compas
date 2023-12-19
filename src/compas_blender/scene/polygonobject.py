from typing import Any
from typing import Optional

import bpy  # type: ignore

from compas.geometry import Polygon
from compas.colors import Color

from compas_blender import conversions

from compas.scene import GeometryObject
from .sceneobject import BlenderSceneObject


class PolygonObject(BlenderSceneObject, GeometryObject):
    """Scene object for drawing polygons in Blender.

    Parameters
    ----------
    polygon : :class:`compas.geometry.Polygon`
        A COMPAS polygon.
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, polygon: Polygon, **kwargs: Any):
        super().__init__(geometry=polygon, **kwargs)

    def draw(
        self,
        color: Optional[Color] = None,
        collection: Optional[str] = None,
    ) -> list[bpy.types.Object]:
        """Draw the polygon.

        Parameters
        ----------
        color : tuple[float, float, float] | tuple[int, int, int] | :class:`compas.colors.Color`, optional
            The RGB color of the polygon.
        collection : str, optional
            The name of the Blender scene collection containing the created object(s).

        Returns
        -------
        list[:blender:`bpy.types.Object`]

        """
        name = self.geometry.name
        color = Color.coerce(color) or self.color

        vertices, faces = self.geometry.to_vertices_and_faces()
        mesh = conversions.vertices_and_faces_to_blender_mesh(vertices, faces, name=self.geometry.name)
        obj = self.create_object(mesh, name=name)
        self.update_object(obj, color=color, collection=collection)

        self._guids = [obj]
        return self.guids
