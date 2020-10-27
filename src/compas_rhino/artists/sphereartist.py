from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.utilities import pairwise
import compas_rhino
from ._shapeartist import ShapeArtist


class SphereArtist(ShapeArtist):
    """Artist for drawing sphere shapes.

    Parameters
    ----------
    shape : :class:`compas.geometry.Sphere`
        A COMPAS sphere.

    Notes
    -----
    See :class:`compas_rhino.artists.ShapeArtist` for all other parameters.

    Examples
    --------
    .. code-block:: python

        import random
        from compas.geometry import Pointcloud
        from compas.geometry import Sphere
        from compas.geometry import Translation
        from compas.utilities import i_to_rgb

        import compas_rhino
        from compas_rhino.artists import SphereArtist

        pcl = Pointcloud.from_bounds(10, 10, 10, 100)
        tpl = Sphere([0, 0, 0], 0.15)

        compas_rhino.clear_layer("Test::SphereArtist")

        for point in pcl.points:
            sphere = tpl.transformed(Translation.from_vector(point))
            artist = SphereArtist(sphere, color=i_to_rgb(random.random()), layer="Test::SphereArtist")
            artist.draw()

    """

    def draw(self, u=10, v=10, show_vertices=False, show_edges=False, show_faces=True, join_faces=True):
        """Draw the sphere associated with the artist.

        Parameters
        ----------
        u : int, optional
            Number of faces in the "u" direction.
            Default is ``10``.
        v : int, optional
            Number of faces in the "v" direction.
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
        vertices, faces = self.shape.to_vertices_and_faces(u=u, v=v)
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
