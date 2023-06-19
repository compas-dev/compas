from typing import Optional
from typing import Any
from typing import List
from typing import Union

import bpy

import compas_blender
from compas.geometry import Sphere
from compas.artists import ShapeArtist
from compas.colors import Color
from .artist import BlenderArtist


class SphereArtist(BlenderArtist, ShapeArtist):
    """Artist for drawing sphere shapes in Blender.

    Parameters
    ----------
    sphere : :class:`~compas.geometry.Sphere`
        A COMPAS sphere.
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

        from compas.geometry import Sphere
        from compas_blender.artists import SphereArtist

        sphere = Sphere([0, 0, 0], 1)

        artist = SphereArtist(sphere)
        artist.draw()

    Or, use the artist through the plugin mechanism.

    .. code-block:: python

        from compas.geometry import Sphere
        from compas.artists import Artist

        sphere = Sphere([0, 0, 0], 1)

        artist = Artist(sphere)
        artist.draw()

    """

    def __init__(self, sphere: Sphere, collection: Optional[Union[str, bpy.types.Collection]] = None, **kwargs: Any):

        super().__init__(shape=sphere, collection=collection or sphere.name, **kwargs)

    def draw(self, color: Optional[Color] = None, u: int = None, v: int = None) -> List[bpy.types.Object]:
        """Draw the sphere associated with the artist.

        Parameters
        ----------
        color : tuple[float, float, float] | tuple[int, int, int] | :class:`~compas.colors.Color`, optional
            The RGB color of the sphere.
            The default color is :attr:`compas.artists.ShapeArtist.color`.
        u : int, optional
            Number of faces in the "u" direction.
            Default is ``SphereArtist.u``.
        v : int, optional
            Number of faces in the "v" direction.
            Default is ``SphereArtist.v``.

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
