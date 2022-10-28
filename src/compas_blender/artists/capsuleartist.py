from typing import Any
from typing import List
from typing import Optional
from typing import Union

import bpy

import compas_blender
from compas.geometry import Capsule
from compas.artists import ShapeArtist
from compas.colors import Color
from .artist import BlenderArtist


class CapsuleArtist(BlenderArtist, ShapeArtist):
    """Artist for drawing capsule shapes in Blender.

    Parameters
    ----------
    capsule : :class:`~compas.geometry.Capsule`
        A COMPAS capsule.
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

        from compas.geometry import Capsule
        from compas_blender.artists import CapsuleArtist

        capsule = Capsule(([0, 0, 0], [1, 0, 0]), 0.3)

        artist = CapsuleArtist(capsule)
        artist.draw()

    Or, use the artist through the plugin mechanism.

    .. code-block:: python

        from compas.geometry import Capsule
        from compas.artists import Artist

        capsule = Capsule(([0, 0, 0], [1, 0, 0]), 0.3)

        artist = Artist(capsule)
        artist.draw()

    """

    def __init__(self, capsule: Capsule, collection: Optional[Union[str, bpy.types.Collection]] = None, **kwargs: Any):

        super().__init__(shape=capsule, collection=collection or capsule.name, **kwargs)

    def draw(self, color: Optional[Color] = None, u: int = None, v: int = None) -> List[bpy.types.Object]:
        """Draw the capsule associated with the artist.

        Parameters
        ----------
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`~compas.colors.Color`, optional
            The RGB color of the capsule.
            The default color is :attr:`compas.artists.ShapeArtist.color`.
        u : int, optional
            Number of faces in the "u" direction.
            Default is :attr:`CapsuleArtist.u`.
        v : int, optional
            Number of faces in the "v" direction.
            Default is :attr:`CapsuleArtist.v`.

        Returns
        -------
        list[:blender:`bpy.types.Object`]
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
