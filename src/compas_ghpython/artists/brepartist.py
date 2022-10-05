from compas_ghpython.artists import GHArtist
from compas_ghpython.utilities import draw_brep


class BrepArtist(GHArtist):
    """An artist for drawing a brep in Grasshopper.

    Parameters
    ==========
    brep : :class:`~compas_rhino.geometry.RhinoBrep`
        The brep to draw.

    """

    def __init__(self, brep):
        super(BrepArtist, self).__init__()
        self._brep = brep

    def draw(self):
        """Draw the brep as a Grasshopper geometry.

        Returns
        -------
        :rhino:`Rhino.Geometry.Brep`
            The Grasshopper geometry instance.

        """
        return draw_brep(self._brep)
