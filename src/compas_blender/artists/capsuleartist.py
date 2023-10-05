from typing import Any
from typing import Optional

import bpy  # type: ignore

from compas.geometry import Capsule
from compas.colors import Color

from compas_blender import conversions

from compas.artists import GeometryArtist
from .artist import BlenderArtist


class CapsuleArtist(BlenderArtist, GeometryArtist):
    """Artist for drawing capsule shapes in Blender.

    Parameters
    ----------
    capsule : :class:`~compas.geometry.Capsule`
        A COMPAS capsule.
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, capsule: Capsule, **kwargs: Any):
        super().__init__(geometry=capsule, **kwargs)

    def draw(
        self,
        color: Optional[Color] = None,
        collection: Optional[str] = None,
        u: int = 16,
        v: int = 16,
        show_wire: bool = False,
        shade_smooth: bool = True,
    ) -> bpy.types.Object:
        """Draw the capsule associated with the artist.

        Parameters
        ----------
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`~compas.colors.Color`, optional
            The RGB color of the capsule.
        collection : str, optional
            The name of the Blender scene collection containing the created object(s).
        u : int, optional
            Number of faces in the "u" direction.
        v : int, optional
            Number of faces in the "v" direction.
        show_wire : bool, optional
            Display the wireframe of the capsule.
        shade_smooth : bool, optional
            Display smooth shading on the capsule.

        Returns
        -------
        :blender:`bpy.types.Object`
            The objects created in Blender.

        """
        name = self.geometry.name
        color = Color.coerce(color) or self.color

        vertices, faces = self.geometry.to_vertices_and_faces(u=u, v=v)
        mesh = conversions.vertices_and_faces_to_blender_mesh(vertices, faces, name=self.geometry.name)
        if shade_smooth:
            mesh.shade_smooth()

        obj = self.create_object(mesh, name=name)
        self.update_object(obj, color=color, collection=collection, show_wire=show_wire)

        return obj
