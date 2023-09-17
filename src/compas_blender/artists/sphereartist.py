from typing import Optional
from typing import Any
from typing import List

import bpy  # type: ignore

from compas.geometry import Sphere
from compas.colors import Color

from compas.artists import GeometryArtist
from .artist import BlenderArtist

from compas_blender import conversions


class SphereArtist(BlenderArtist, GeometryArtist):
    """Artist for drawing sphere shapes in Blender.

    Parameters
    ----------
    sphere : :class:`~compas.geometry.Sphere`
        A COMPAS sphere.
    **kwargs : dict, optional
        Additional keyword arguments.
        For more info,
        see :class:`~compas_blender.artists.BlenderArtist` and :class:`~compas.artists.GeometryArtist`.

    """

    def __init__(self, sphere: Sphere, **kwargs: Any):
        super().__init__(geometry=sphere, **kwargs)

    def draw(
        self, color: Optional[Color] = None, collection: Optional[str] = None, u: int = 16, v: int = 16
    ) -> List[bpy.types.Object]:
        """Draw the sphere associated with the artist.

        Parameters
        ----------
        color : tuple[float, float, float] | tuple[int, int, int] | :class:`~compas.colors.Color`, optional
            The RGB color of the sphere.
        collection : str, optional
            The name of the Blender scene collection containing the created object(s).
        u : int, optional
            Number of faces in the "u" direction.
        v : int, optional
            Number of faces in the "v" direction.

        Returns
        -------
        list
            The objects created in Blender.
        """
        name = self.geometry.name
        color = Color.coerce(color) or self.color

        vertices, faces = self.geometry.to_vertices_and_faces(u=u, v=v)
        mesh = conversions.vertices_and_faces_to_blender_mesh(vertices, faces, name=self.geometry.name)

        obj = self.create_object(mesh, name=name)
        self.update_object(obj, color=color, collection=collection, show_wire=True)

        return obj
