from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from functools import partial

import Rhino

import compas_ghpython
from compas_ghpython.artists._artist import BaseArtist

from compas.geometry import centroid_polygon
from compas.utilities import color_to_colordict
from compas.utilities import pairwise


colordict = partial(color_to_colordict, colorformat='rgb', normalize=False)


__all__ = ['MeshArtist']


class MeshArtist(BaseArtist):
    """A mesh artist defines functionality for visualising COMPAS meshes in GhPython.

    Parameters
    ----------
    mesh : :class:`compas.datastructures.Mesh`
        A COMPAS mesh.

    Attributes
    ----------
    mesh : :class:`compas.datastructures.Mesh`
        The COMPAS mesh associated with the artist.
    color_vertices : 3-tuple
        Default color of the vertices.
    color_edges : 3-tuple
        Default color of the edges.
    color_faces : 3-tuple
        Default color of the faces.

    Examples
    --------
    .. code-block:: python

        import compas
        from compas.datastructures import Mesh
        from compas_ghpython.artists import MeshArtist

        mesh = Mesh.from_obj(compas.get('faces.obj'))

        artist = MeshArtist(mesh)
        artist.draw_faces(join_faces=True)
        artist.draw_vertices(color={key: '#ff0000' for key in mesh.vertices_on_boundary()})
        artist.draw_edges()

    """

    def __init__(self, mesh):
        self._mesh = None
        self.mesh = mesh
        self.color_vertices = (255, 255, 255)
        self.color_edges = (0, 0, 0)
        self.color_faces = (210, 210, 210)

    @property
    def mesh(self):
        """compas.datastructures.Mesh: The mesh that should be painted."""
        return self._mesh

    @mesh.setter
    def mesh(self, mesh):
        self._mesh = mesh

    def draw(self, color=None):
        """Draw the mesh as a RhinoMesh.

        Parameters
        ----------
        color : 3-tuple, optional
            RGB color components in integer format (0-255).

        Returns
        -------
        :class:`Rhino.Geometry.Mesh`

        """
        vertex_index = self.mesh.key_index()
        vertices = self.mesh.vertices_attributes('xyz')
        faces = [[vertex_index[vertex] for vertex in self.mesh.face_vertices(face)] for face in self.mesh.faces()]
        new_faces = []
        for face in faces:
            f = len(face)
            if f == 3:
                new_faces.append(face + [face[-1]])
            elif f == 4:
                new_faces.append(face)
            elif f > 4:
                centroid = len(vertices)
                vertices.append(centroid_polygon(
                    [vertices[index] for index in face]))
                for a, b in pairwise(face + face[0:1]):
                    new_faces.append([centroid, a, b, b])
            else:
                continue
        return compas_ghpython.draw_mesh(vertices, new_faces, color)

    def draw_vertices(self, vertices=None, color=None):
        """Draw a selection of vertices.

        Parameters
        ----------
        vertices : list, optional
            A selection of vertices to draw.
            Default is ``None``, in which case all vertices are drawn.
        color : 3-tuple or dict of 3-tuple, optional
            The color specififcation for the vertices.
            The default color is ``(255, 255, 255)``.

        Returns
        -------
        list of :class:`Rhino.Geometry.Point3d`

        """
        vertices = vertices or list(self.mesh.vertices())
        vertex_color = colordict(color, vertices, default=self.color_vertices)
        points = []
        for vertex in vertices:
            points.append({
                'pos': self.mesh.vertex_coordinates(vertex),
                'name': "{}.vertex.{}".format(self.mesh.name, vertex),
                'color': vertex_color[vertex]})
        return compas_ghpython.draw_points(points)

    def draw_faces(self, faces=None, color=None, join_faces=False):
        """Draw a selection of faces.

        Parameters
        ----------
        faces : list
            A selection of faces to draw.
            The default is ``None``, in which case all faces are drawn.
        color : 3-tuple or dict of 3-tuple, optional
            The color specififcation for the faces.
            The default color is ``(0, 0, 0)``.

        Returns
        -------
        list of :class:`Rhino.Geometry.Mesh`

        """
        faces = faces or list(self.mesh.faces())
        face_color = colordict(color, faces, default=self.color_faces)
        faces_ = []
        for face in faces:
            faces_.append({
                'points': self.mesh.face_coordinates(face),
                'name': "{}.face.{}".format(self.mesh.name, face),
                'color': face_color[face]})
        meshes = compas_ghpython.draw_faces(faces_)
        if not join_faces:
            return meshes
        joined_mesh = Rhino.Geometry.Mesh()
        for mesh in meshes:
            joined_mesh.Append(mesh)
        return [joined_mesh]

    def draw_edges(self, edges=None, color=None):
        """Draw a selection of edges.

        Parameters
        ----------
        edges : list, optional
            A selection of edges to draw.
            The default is ``None``, in which case all edges are drawn.
        color : 3-tuple or dict of 3-tuple, optional
            The color specififcation for the edges.
            The default color is ``(210, 210, 210)``.

        Returns
        -------
        list of :class:`Rhino.Geometry.Line`

        """
        edges = edges or list(self.mesh.edges())
        edge_color = colordict(color, edges, default=self.color_edges)
        lines = []
        for edge in edges:
            start, end = self.mesh.edge_coordinates(*edge)
            lines.append({
                'start': start,
                'end': end,
                'color': edge_color[edge],
                'name': "{}.edge.{}-{}".format(self.mesh.name, *edge)})
        return compas_ghpython.draw_lines(lines)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
