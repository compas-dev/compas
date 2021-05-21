"""
Draws a frome or plane.
"""
from ghpythonlib.componentbase import executingcomponent as component

from compas_ghpython.artists import FrameArtist
from compas_ghpython.components import coerce_frame


class CompasFrame(component):
    def RunScript(self, plane):
        origin = None
        axes = []

        if plane:
            frame = coerce_frame(plane)
            artist = FrameArtist(frame)

            origin, axes = artist.draw()

        return origin, axes
