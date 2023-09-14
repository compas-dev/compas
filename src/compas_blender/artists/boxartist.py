from typing import Any
from typing import Optional
from typing import Union

import bpy  # type: ignore

from compas.geometry import Box
from compas.artists import GeometryArtist
from compas.colors import Color
from compas_blender.conversions import vertices_and_faces_to_blender
from .artist import BlenderArtist


class BoxArtist(BlenderArtist, GeometryArtist):
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
        see :class:`~compas_blender.artists.BlenderArtist` and :class:`~compas.artists.GeometryArtist`.

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

    def __init__(
        self,
        box: Box,
        collection: Optional[Union[str, bpy.types.Collection]] = None,
        **kwargs: Any,
    ):
        super().__init__(
            geometry=box,
            collection=collection or box.name,
            **kwargs,
        )

    def draw(self, color: Optional[Color] = None) -> bpy.types.Object:
        """Draw the box associated with the artist.

        Parameters
        ----------
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`~compas.colors.Color`, optional
            The RGB color of the box.
            The default color is :attr:`compas.artists.GeometryArtist.color`.

        Returns
        -------
        :blender:`bpy.types.Object`
            The object(s) created in Blender to represent the box.

        """
        color = Color.coerce(color) or self.color

        # add option for local coordinates
        vertices, faces = self.geometry.to_vertices_and_faces()
        mesh = vertices_and_faces_to_blender(vertices, faces, name=self.geometry.name)

        obj = bpy.data.objects.new(self.geometry.name, mesh)
        obj.show_wire = True

        # mp = centroid_points(vertices) if centroid else [0, 0, 0]
        # vertices = [subtract_vectors(vertex, mp) for vertex in vertices]
        # obj.location = self.geometry.frame.point

        # obj.matrix_world = self.geometry.transformation.matrix

        self.link_object(obj)
        if color:
            self.assign_object_color(obj, color)

        return obj
