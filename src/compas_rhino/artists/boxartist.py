from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino
from compas_rhino.artists._shapeartist import ShapeArtist


class BoxArtist(ShapeArtist):
    """Artist for drawing box shapes.

    Parameters
    ----------
    shape : :class:`compas.geometry.Box`
        A COMPAS box.

    Notes
    -----
    See :class:`compas_rhino.artists.ShapeArtist` for all other parameters.

    Examples
    --------
    .. code-block:: python

        import random
        from compas.geometry import Pointcloud
        from compas.geometry import Box
        from compas.utilities import i_to_rgb

        import compas_rhino
        from compas_rhino.artists import BoxArtist

        pcl = Pointcloud.from_bounds(10, 10, 10, 100)
        tpl = Box.from_width_height_depth(0.3, 0.3, 0.3)

        compas_rhino.clear()

        for point in pcl.points:
            box = tpl.copy()
            box.frame.point = point
            artist = BoxArtist(box, layer="Test::BoxArtist")
            artist.color = i_to_rgb(random.random())
            artist.draw()
    """

    def draw(self):
        """Draw the box associated with the artist.

        Returns
        -------
        list
            The GUIDs of the objects created in Rhino.
        """
        vertices = [list(vertex) for vertex in self.shape.vertices]
        faces = self.shape.faces
        guids = []
        guid = compas_rhino.draw_mesh(vertices, faces, layer=self.layer, name=self.shape.name, color=self.color, disjoint=True, clear=False, redraw=False)
        guids.append(guid)
        return guids
