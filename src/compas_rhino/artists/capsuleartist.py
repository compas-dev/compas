from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.utilities import pairwise
import compas_rhino
from compas.artists import ShapeArtist
from ._artist import RhinoArtist


class CapsuleArtist(RhinoArtist, ShapeArtist):
    """Artist for drawing capsule shapes.

    Parameters
    ----------
    capsule : :class:`compas.geometry.Capsule`
        A COMPAS capsule.
    layer : str, optional
        The layer that should contain the drawing.
    """

    def __init__(self, capsule, layer=None):
        super(CapsuleArtist, self).__init__(capsule)
        self.layer = layer

    def draw(self, u=None, v=None, show_vertices=False, show_edges=False, show_faces=True, join_faces=True):
        """Draw the capsule associated with the artist.

        Parameters
        ----------
        u : int, optional
            Number of faces in the "u" direction.
            Default is ``~CapsuleArtist.u``.
        v : int, optional
            Number of faces in the "v" direction.
            Default is ``~CapsuleArtist.v``.
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
        u = u or self.u
        v = v or self.v
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
                guid = compas_rhino.draw_mesh(vertices, faces, layer=self.layer, name=self.shape.name, color=self.color, disjoint=True)
                guids.append(guid)
            else:
                polygons = [{'points': [vertices[index] for index in face], 'color': self.color} for face in faces]
                guids += compas_rhino.draw_faces(polygons, layer=self.layer, clear=False, redraw=False)
        return guids
