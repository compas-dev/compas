from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.utilities import pairwise
import compas_rhino
from ._shapeartist import ShapeArtist


class ConeArtist(ShapeArtist):
    """Artist for drawing cone shapes.

    Parameters
    ----------
    shape : :class:`compas.geometry.Cone`
        A COMPAS cone.

    Notes
    -----
    See :class:`compas_rhino.artists.ShapeArtist` for all other parameters.

    Examples
    --------
    .. code-block:: python

        import random
        from compas.geometry import Pointcloud
        from compas.geometry import Cone
        from compas.geometry import Translation
        from compas.utilities import i_to_rgb

        import compas_rhino
        from compas_rhino.artists import ConeArtist

        pcl = Pointcloud.from_bounds(10, 10, 10, 200)
        tpl = Cone([[[0, 0, 0], [0, 0, 1]], 0.2], 0.8)

        vertices, faces = tpl.to_vertices_and_faces(4)

        compas_rhino.clear_layer("Test::ConeArtist")

        for point in pcl.points[:len(pcl) // 2]:
            cone = tpl.transformed(Translation.from_vector(point))
            artist = ConeArtist(cone, color=i_to_rgb(random.random()), layer="Test::ConeArtist")
            artist.draw(u=16)

    """

    def draw(self, u=10, show_vertices=False, show_edges=False, show_faces=True, join_faces=True):
        """Draw the cone associated with the artist.

        Parameters
        ----------
        u : int, optional
            Number of faces in the "u" direction.
            Default is ``10``.
        show_vertices : bool, optional
            Default is ``False``.
        show_edges : bool, optional
            Default is ``False``.
        show_faces : bool, optional
            Default is ``True``.
        join_faces : bool, optional
            Default is ``True``.

        Returns
        -------
        list
            The GUIDs of the objects created in Rhino.
        """
        vertices, faces = self.shape.to_vertices_and_faces(u=u)
        vertices = [list(vertex) for vertex in vertices]
        guids = []
        if show_vertices:
            points = [{'pos': point, 'color': self.color} for point in vertices]
            guids += compas_rhino.draw_points(points, layer=self.layer, clear=False, redraw=False)
        if show_edges:
            lines = []
            seen = set()
            for face in faces:
                for u, v in pairwise(face + face[:1]):
                    if (u, v) not in seen:
                        seen.add((u, v))
                        seen.add((v, u))
                        lines.append({'start': vertices[u], 'end': vertices[v], 'color': self.color})
            guids += compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)
        if show_faces:
            if join_faces:
                guid = compas_rhino.draw_mesh(vertices, faces, layer=self.layer, name=self.name, color=self.color, disjoint=True)
                guids.append(guid)
            else:
                polygons = [{'points': [vertices[index] for index in face], 'color': self.color} for face in faces]
                guids += compas_rhino.draw_faces(polygons, layer=self.layer, clear=False, redraw=False)
        self._guids = guids
        return guids


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
