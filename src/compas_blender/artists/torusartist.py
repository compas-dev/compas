from typing import Optional
from typing import Any
from typing import List
from typing import Union

import bpy

import compas_blender
from compas.geometry import Torus
from compas.artists import ShapeArtist
from compas.colors import Color
from .artist import BlenderArtist


class TorusArtist(BlenderArtist, ShapeArtist):
    """Artist for drawing torus shapes in Blender.

    Parameters
    ----------
    torus : :class:`~compas.geometry.Torus`
        A COMPAS torus.
    collection: str | :blender:`bpy.types.Collection`
        The name of the collection the object belongs to.
    **kwargs : dict, optional
        Additional keyword arguments.
        For more info,
        see :class:`~compas_blender.artists.BlenderArtist` and :class:`~compas.artists.ShapeArtist`.

    Examples
    --------
    Use the Blender artist explicitly.

    .. code-block:: python

        from compas.geometry import Plane, Torus
        from compas_blender.artists import TorusArtist

        torus = Torus(Plane([0, 0, 0], [0, 0, 1]), 1.0, 0.3)

        artist = TorusArtist(torus)
        artist.draw()

    Or, use the artist through the plugin mechanism.

    .. code-block:: python

        from compas.geometry import Plane, Torus
        from compas.artists import Artist

        torus = Torus(Plane([0, 0, 0], [0, 0, 1]), 1.0, 0.3)

        artist = Artist(torus)
        artist.draw()

    """

    def __init__(self, torus: Torus, collection: Optional[Union[str, bpy.types.Collection]] = None, **kwargs: Any):

        super().__init__(shape=torus, collection=collection or torus.name, **kwargs)

    def draw(
        self,
        color: Optional[Color] = None,
        u: Optional[int] = None,
        v: Optional[int] = None,
    ) -> List[bpy.types.Object]:
        """Draw the torus associated with the artist.

        Parameters
        ----------
        color : tuple[float, float, float] | tuple[int, int, int] | :class:`~compas.colors.Color`, optional
            The RGB color of the torus.
            The default color is :attr:`compas.artists.ShapeArtist.color`.
        u : int, optional
            Number of faces in the "u" direction.
            Default is :attr:`TorusArtist.u`.
        v : int, optional
            Number of faces in the "v" direction.
            Default is :attr:`TorusArtist.v`.

        Returns
        -------
        list
            The objects created in Blender.

        """
        u = u or self.u
        v = v or self.v
        color = Color.coerce(color) or self.color
        vertices, faces = self.shape.to_vertices_and_faces(u=u, v=v)
        obj = compas_blender.draw_mesh(
            vertices,
            faces,
            name=self.shape.name,
            color=color,
            collection=self.collection,
        )
        return [obj]
