from typing import Any
from typing import Optional
from typing import Union

import bpy  # type: ignore

from compas.geometry import Cylinder
from compas.artists import GeometryArtist
from compas.colors import Color
from compas_blender.conversions import vertices_and_faces_to_blender
from .artist import BlenderArtist


class CylinderArtist(BlenderArtist, GeometryArtist):
    """Artist for drawing cylinder shapes in Blender.

    Parameters
    ----------
    cylinder : :class:`~compas.geometry.Cylinder`
        A COMPAS cylinder.
    collection : str | :blender:`bpy.types.Collection`
        The Blender scene collection the object(s) created by this artist belong to.
    **kwargs : dict, optional
        Additional keyword arguments.
        For more info,
        see :class:`~compas_blender.artists.BlenderArtist` and :class:`~compas.artists.GeometryArtist`.

    Examples
    --------
    Use the Blender artist explicitly.

    .. code-block:: python

        from compas.geometry import Plane, Circle, Cylinder
        from compas_blender.artists import CylinderArtist

        cylinder = Cylinder(Circle(Plane([0, 0, 0], [0, 0, 1]), 0.3), 1.0)

        artist = CylinderArtist(cylinder)
        artist.draw()

    Or, use the artist through the plugin mechanism.

    .. code-block:: python

        from compas.geometry import Plane, Circle, Cylinder
        from compas.artists import Artist

        cylinder = Cylinder(Circle(Plane([0, 0, 0], [0, 0, 1]), 0.3), 1.0)

        artist = Artist(cylinder)
        artist.draw()

    """

    def __init__(
        self,
        cylinder: Cylinder,
        collection: Optional[Union[str, bpy.types.Collection]] = None,
        **kwargs: Any,
    ):
        super().__init__(
            geometry=cylinder,
            collection=collection or cylinder.name,
            **kwargs,
        )

    def draw(self, color: Optional[Color] = None, u: int = 16) -> bpy.types.Object:
        """Draw the cylinder associated with the artist.

        Parameters
        ----------
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`~compas.colors.Color`, optional
            The RGB color of the cylinder.
        u : int, optional
            Number of faces in the "u" direction.

        Returns
        -------
        :blender:`bpy.types.Object`
            The objects created in Blender.

        """
        color = Color.coerce(color) or self.color

        vertices, faces = self.geometry.to_vertices_and_faces(u=u)
        mesh = vertices_and_faces_to_blender(vertices, faces, name=self.geometry.name)

        obj = bpy.data.objects.new(self.geometry.name, mesh)
        obj.show_wire = True

        self.link_object(obj)
        if color:
            self.assign_object_color(obj, color)

        return obj
