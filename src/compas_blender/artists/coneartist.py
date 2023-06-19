from typing import Any
from typing import List
from typing import Optional
from typing import Union

import bpy

import compas_blender
from compas.geometry import Cone
from compas.artists import ShapeArtist
from compas.colors import Color
from .artist import BlenderArtist


class ConeArtist(BlenderArtist, ShapeArtist):
    """Artist for drawing cone shapes in Blender.

    Parameters
    ----------
    cone : :class:`~compas.geometry.Cone`
        A COMPAS cone.
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

        from compas.geometry import Plane, Circle, Cone
        from compas_blender.artists import ConeArtist

        cone = Cone(Circle(Plane([0, 0, 0], [0, 0, 1]), 0.3), 1.0)

        artist = ConeArtist(cone)
        artist.draw()

    Or, use the artist through the plugin mechanism.

    .. code-block:: python

        from compas.geometry import Plane, Circle, Cone
        from compas.artists import Artist

        cone = Cone(Circle(Plane([0, 0, 0], [0, 0, 1]), 0.3), 1.0)

        artist = Artist(cone)
        artist.draw()

    """

    def __init__(self, cone: Cone, collection: Optional[Union[str, bpy.types.Collection]] = None, **kwargs: Any):

        super().__init__(shape=cone, collection=collection or cone.name, **kwargs)

    def draw(self, color: Optional[Color] = None, u: int = None) -> List[bpy.types.Object]:
        """Draw the cone associated with the artist.

        Parameters
        ----------
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`~compas.colors.Color`, optional
            The RGB color of the cone.
            The default color is :attr:`compas.artists.ShapeArtist.color`.
        u : int, optional
            Number of faces in the "u" direction.
            Default is :attr:`ConeArtist.u`.

        Returns
        -------
        list[:blender:`bpy.types.Object`]
            The objects created in Blender.

        """
        u = u or self.u
        color = Color.coerce(color) or self.color
        vertices, faces = self.shape.to_vertices_and_faces(u=u)
        obj = compas_blender.draw_mesh(
            vertices,
            faces,
            name=self.shape.name,
            color=color,
            collection=self.collection,
        )
        return [obj]
