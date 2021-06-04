"""
Draws a frame or plane.
"""
from ghpythonlib.componentbase import executingcomponent as component

from compas_ghpython.artists import FrameArtist
from compas_ghpython.components import coerce_frame


class CompasFrame(component):
    def RunScript(self, frame):
        plane = None

        if frame:
            frame = coerce_frame(frame)
            artist = FrameArtist(frame)

            plane = artist.draw()

        return plane
