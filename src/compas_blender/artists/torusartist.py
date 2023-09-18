from typing import Optional
from typing import Any

import bpy  # type: ignore

from compas.geometry import Torus
from compas.colors import Color

from compas.artists import GeometryArtist
from .artist import BlenderArtist

from compas_blender import conversions


class TorusArtist(BlenderArtist, GeometryArtist):
    """Artist for drawing torus shapes in Blender.

    Parameters
    ----------
    torus : :class:`~compas.geometry.Torus`
        A COMPAS torus.
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, torus: Torus, **kwargs: Any):
        super().__init__(geometry=torus, **kwargs)

    def draw(
        self,
        color: Optional[Color] = None,
        collection: Optional[str] = None,
        u: Optional[int] = 16,
        v: Optional[int] = 16,
    ) -> bpy.types.Object:
        """Draw the torus associated with the artist.

        Parameters
        ----------
        color : tuple[float, float, float] | tuple[int, int, int] | :class:`~compas.colors.Color`, optional
            The RGB color of the torus.
        collection : str, optional
            The name of the Blender scene collection containing the created object(s).
        u : int, optional
            Number of faces in the "u" direction.
        v : int, optional
            Number of faces in the "v" direction.

        Returns
        -------
        :blender:`bpy.types.Curve`

        """
        name = self.geometry.name
        color = Color.coerce(color) or self.color

        vertices, faces = self.geometry.to_vertices_and_faces(u=u, v=v)
        mesh = conversions.vertices_and_faces_to_blender_mesh(vertices, faces, name=self.geometry.name)

        obj = self.create_object(mesh, name=name)
        self.update_object(obj, color=color, collection=collection, show_wire=True)

        return obj
