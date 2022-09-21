from compas_ghpython.artists import GHArtist
from compas_ghpython.utilities import draw_brep


class BrepArtist(GHArtist):
    def __init__(self, brep):
        super(BrepArtist, self).__init__()
        self._brep = brep

    def draw(self):
        return draw_brep(self._brep)

