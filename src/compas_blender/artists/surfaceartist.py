from typing import Any
from typing import Optional

import bpy  # type: ignore

from compas.geometry import Surface
from compas.colors import Color

from compas.artists import GeometryArtist
from compas_blender.artists import BlenderArtist

from compas_blender import conversions


class SurfaceArtist(BlenderArtist, GeometryArtist):
    """Artist for drawing surfaces in Blender.

    Parameters
    ----------
    surface : :class:`~compas.geometry.Surface`
        A COMPAS surface.
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, surface: Surface, **kwargs: Any):
        super().__init__(geometry=surface, **kwargs)

    def draw(self, color: Optional[Color] = None, collection: Optional[str] = None) -> bpy.types.Object:
        """Draw the surface.

        Parameters
        ----------
        color : tuple[float, float, float] | tuple[int, int, int] | :class:`~compas.colors.Color`, optional
            The RGB color of the surface.
        collection : str, optional
            The name of the Blender scene collection containing the created object(s).

        Returns
        -------
        :blender:`bpy.types.Object`

        """
        name = self.geometry.name
        color = Color.coerce(color) or self.color

        surface = conversions.nurbssurface_to_blender_surface(self.geometry)

        obj = self.create_object(surface, name=name)
        self.update_object(obj, color=color, collection=collection)

        return obj
