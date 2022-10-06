from typing import Any
from typing import List
from typing import Optional
from typing import Union

import bpy
import compas_blender
from compas.geometry import Polyhedron
from compas.artists import ShapeArtist
from compas.colors import Color
from .artist import BlenderArtist


class PolyhedronArtist(BlenderArtist, ShapeArtist):
    """Artist for drawing polyhedron shapes in Blender.

    Parameters
    ----------
    polyhedron : :class:`~compas.geometry.Polyhedron`
        A COMPAS polyhedron.
    collection : str | :blender:`bpy.types.Collection`
        The Blender scene collection the object(s) created by this artist belong to.
    **kwargs : dict, optional
        Additional keyword arguments.
        For more info,
        see :class:`~compas_blender.artists.BlenderArtist` and :class:`~compas.artists.ShapeArtist`.

    Examples
    --------
    Use the Blender artist explicitly.

    .. code-block:: python

        from compas.geometry import Polyhedron
        from compas_blender.artists import PolyhedronArtist

        polyhedron = Polyhedron.from_platonicsolid(12)

        artist = PolyhedronArtist(polyhedron)
        artist.draw()

    Or, use the artist through the plugin mechanism.

    .. code-block:: python

        from compas.geometry import Polyhedron
        from compas.artists import Artist

        polyhedron = Polyhedron.from_platonicsolid(12)

        artist = Artist(polyhedron)
        artist.draw()

    """

    def __init__(
        self, polyhedron: Polyhedron, collection: Optional[Union[str, bpy.types.Collection]] = None, **kwargs: Any
    ):

        super().__init__(shape=polyhedron, collection=collection or polyhedron.name, **kwargs)

    def draw(self, color: Optional[Color] = None) -> List[bpy.types.Object]:
        """Draw the polyhedron associated with the artist.

        Parameters
        ----------
        color : tuple[float, float, float] | tuple[int, int, int] | :class:`~compas.colors.Color`, optional
            The RGB color of the polyhedron.
            The default color is :attr:`compas.artists.ShapeArtist.color`.

        Returns
        -------
        list[:blender:`bpy.types.Object`]
            The objects created in Blender.

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
