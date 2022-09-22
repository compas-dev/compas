import compas_rhino
from .artist import RhinoArtist


class BrepArtist(RhinoArtist):
    """An artist for drawing a RhinoBrep.

    Parameters
    ==========
    brep : :class:`~compas_rhino.geometry.RhinoBrep`
        The Brep to draw.

    """

    def __init__(self, brep):
        super(BrepArtist, self).__init__()
        self._brep = brep

    def draw(self, color=None):
        """Bakes the Brep into the current document

        Returns
        -------
        list(:rhino:`System.Guid`)
            The guid of the baked Brep.

        """
        return [compas_rhino.draw_brep(self._brep, color)]
