import bpy
import compas_blender

from compas.scene import BaseArtist


__all__ = ['Artist']


class Artist(BaseArtist):
    """Base class for all Blender artists.

    Attributes
    ----------
    objects : list
        A list of Blender objects (unique object names) created by the artist.

    """

    def __init__(self):
        super().__init__()
        self.objects = []

    @staticmethod
    def draw_collection(collection):
        raise NotImplementedError

    def draw(self):
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


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
