from typing import Any
from typing import List
from typing import Optional
from typing import Union

import bpy
import compas_blender
from compas.geometry import Box
from compas.artists import ShapeArtist
from compas.colors import Color
from .artist import BlenderArtist


class BoxArtist(BlenderArtist, ShapeArtist):
    """Artist for drawing box shapes in Blender.

    Parameters
    ----------
    box : :class:`~compas.geometry.Box`
        A COMPAS box.
    collection : str | :blender:`bpy.types.Collection`, optional
        The Blender scene collection the object(s) created by this artist belong to.
    **kwargs : dict, optional
        Additional keyword arguments.
        For more info,
        see :class:`~compas_blender.artists.BlenderArtist` and :class:`~compas.artists.ShapeArtist`.

    Examples
    --------
    Use the Blender artist explicitly.

    .. code-block:: python

        from compas.geometry import Box
        from compas_blender.artists import BoxArtist

        box = Box.from_width_height_depth(1, 1, 1)

        artist = BoxArtist(box)
        artist.draw()

    Or, use the artist through the plugin mechanism.

    .. code-block:: python

        from compas.geometry import Box
        from compas.artists import Artist

        box = Box.from_width_height_depth(1, 1, 1)

        artist = Artist(box)
        artist.draw()

    """

    def __init__(self, box: Box, collection: Optional[Union[str, bpy.types.Collection]] = None, **kwargs: Any):

        super().__init__(shape=box, collection=collection or box.name, **kwargs)

    def draw(self, color: Optional[Color] = None) -> List[bpy.types.Object]:
        """Draw the box associated with the artist.

        Parameters
        ----------
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`~compas.colors.Color`, optional
            The RGB color of the box.
            The default color is :attr:`compas.artists.ShapeArtist.color`.

        Returns
        -------
        list[:blender:`bpy.types.Object`]
            The object(s) created in Blender to represent the box.

        """
        color = Color.coerce(color) or self.color
        vertices, faces = self.shape.to_vertices_and_faces()
        obj = compas_blender.draw_mesh(
            vertices,
            faces,
            name=self.shape.name,
            color=color,
            collection=self.collection,
        )
        return [obj]
