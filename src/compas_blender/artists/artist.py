import bpy
import abc
import compas_blender

from compas.artists import Artist


class BlenderArtist(Artist, abc.ABC):
    """Base class for all Blender artists.

    Attributes
    ----------
    objects : list
        A list of Blender objects (unique object names) created by the artist.

    """

    def __init__(self):
        self.objects = []

    def draw(self):
        """Draw the item."""
        raise NotImplementedError

    def redraw(self):
        """Trigger a redraw."""
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)

    def clear(self):
        """Delete all objects created by the artist."""
        if not self.objects:
            return
        compas_blender.delete_objects(self.objects)
        self.objects = []
