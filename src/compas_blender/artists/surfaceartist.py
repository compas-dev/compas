from typing import Any
from typing import List
from typing import Optional
from typing import Union

import bpy

import compas_blender
from compas.artists import SurfaceArtist
from compas.geometry import Surface
from compas.colors import Color
from compas_blender.artists import BlenderArtist


class SurfaceArtist(BlenderArtist, SurfaceArtist):
    """Artist for drawing surfaces in Blender.

    Parameters
    ----------
    surface : :class:`~compas.geometry.Surface`
        A COMPAS surface.
    collection : str | :blender:`bpy.types.Collection`
        The Blender scene collection the object(s) created by this artist belong to.
    **kwargs : dict, optional
        Additional keyword arguments.
        For more info,
        see :class:`~compas_blender.artists.BlenderArtist` and :class:`~compas.artists.PrimitiveArtist`.

    Examples
    --------
    Use the Blender artist explicitly.

    .. code-block:: python

        from compas.geometry import NurbsSurface
        from compas_blender.artists import SurfaceArtist

        surface = NurbsSurface([[0, 0, 0], [1, 0, 0], [1, 1, 0], [1, 1, 1]])

        artist = SurfaceArtist(surface)
        artist.draw()

    Or, use the artist through the plugin mechanism.

    .. code-block:: python

        from compas.geometry import NurbsSurface
        from compas.artists import Artist

        surface = NurbsSurface([[0, 0, 0], [1, 0, 0], [1, 1, 0], [1, 1, 1]])

        artist = Artist(surface)
        artist.draw()

    """

    def __init__(self, surface: Surface, collection: Optional[Union[str, bpy.types.Collection]] = None, **kwargs: Any):

        super().__init__(surface=surface, collection=collection or surface.name, **kwargs)

    def draw(self, color: Optional[Color] = None) -> List[bpy.types.Object]:
        """Draw the surface.

        Parameters
        ----------
        color : tuple[float, float, float] | tuple[int, int, int] | :class:`~compas.colors.Color`, optional
            The RGB color of the surface.
            The default color is :attr:`compas.artists.SurfaceArtist.color`.

        Returns
        -------
        list[:blender:`bpy.types.Object`]

        """
        color = Color.coerce(color) or self.color
        surfaces = [{"surface": self.surface, "color": color, "name": self.surface.name}]
        return compas_blender.draw_surfaces(surfaces, collection=self.collection)
