from typing import Any
from typing import Optional

import bpy  # type: ignore

from compas.geometry import Point
from compas.colors import Color

from compas.scene import GeometryObject
from .artist import BlenderArtist

from compas_blender import conversions


class PointcloudArtist(BlenderArtist, GeometryObject):
    """Artist for drawing pointclouds in Blender.

    Parameters
    ----------
    pointcloud : :class:`compas.geometry.Pointcloud`
        A COMPAS point.
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, point: Point, **kwargs: Any):
        super().__init__(geometry=point, **kwargs)

    def draw(
        self,
        color: Optional[Color] = None,
        collection: Optional[str] = None,
        radius: float = 0.01,
        u: int = 16,
        v: int = 16,
    ) -> bpy.types.Object:
        """Draw the pointcloud.

        Parameters
        ----------
        color : tuple[float, float, float] | tuple[int, int, int] | :class:`compas.colors.Color`, optional
            Color of the point object.
        collection : str, optional
            The name of the Blender scene collection containing the created object(s).
        radius : float, optional
            The radius of the spheres representing the vertices.
        u : int, optional
            Number of faces in the "u" direction of the spheres representing the vertices.
        v : int, optional
            Number of faces in the "v" direction of the spheres representing the vertices.

        Returns
        -------
        :blender:`bpy.types.Object`

        """
        name = self.geometry.name
        color = Color.coerce(color) or self.color

        mesh = conversions.pointcloud_to_blender(self.geometry, name=name, u=u, v=v, radius=radius)

        obj = self.create_object(mesh, name=name)
        self.update_object(obj, color=color, collection=collection)

        return obj
