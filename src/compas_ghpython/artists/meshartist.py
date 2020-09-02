from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import Rhino

import compas_ghpython
from compas_ghpython.artists._artist import BaseArtist

from compas.geometry import centroid_polygon
from compas.utilities import color_to_colordict as colordict
from compas.utilities import pairwise


__all__ = ['MeshArtist']


class MeshArtist(BaseArtist):
    """A mesh artist defines functionality for visualising COMPAS meshes in GhPython.

    Parameters
    ----------
    mesh : :class:`compas.datastructures.Mesh`
        A COMPAS mesh.
    settings : dict, optional
        A dict with custom visualisation settings.

    Attributes
    ----------
    mesh : :class:`compas.datastructures.Mesh`
        The COMPAS mesh associated with the artist.

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
        self.settings = {
            'color.vertices': (255, 255, 255),
            'color.edges': (0, 0, 0),
            'color.faces': (210, 210, 210),
        }

    @property
    def mesh(self):
        """compas.datastructures.Mesh: The mesh that should be painted."""
        return self._mesh

    @mesh.setter
    def mesh(self, mesh):
        self._mesh = mesh

    def draw(self):
        """For meshes (and data structures in general), a main draw function does not exist.
        Instead, you should use the drawing functions for the various components of the mesh:

        * ``draw_vertices``
        * ``draw_faces``
        * ``draw_edges``

        To simply draw a mesh, use ``draw_mesh``.
        """
        raise NotImplementedError

    # ==============================================================================
    # components
    # ==============================================================================

    def draw_mesh(self, color=None):
        """Draw the mesh as a RhinoMesh.

        Parameters
        ----------
        color : 3-tuple, optional
            RGB color components in integer format (0-255).

        Returns
        -------
        :class:`Rhino.Geometry.Mesh`

        Notes
        -----
        Faces with more than 4 vertices will be triangulated on-the-fly.

        """
        key_index = self.mesh.key_index()
        vertices = self.mesh.vertices_attributes('xyz')
        faces = [[key_index[key] for key in self.mesh.face_vertices(fkey)] for fkey in self.mesh.faces()]
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
        color : rgb-tuple or dict of rgb-tuple, optional
            The color specififcation for the vertices.
            The default color is defined in the class settings.

        Returns
        -------
        list of :class:`Rhino.Geometry.Point3d`

        """
        vertices = vertices or list(self.mesh.vertices())
        vertex_color = colordict(color, vertices, default=self.settings['color.vertices'], colorformat='rgb', normalize=False)
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
        color : rgb-tuple or dict of rgb-tuple, optional
            The color specififcation for the faces.
            The default color is in the class settings.

        Returns
        -------
        list of :class:`Rhino.Geometry.Mesh`

        """
        faces = faces or list(self.mesh.faces())
        face_color = colordict(color, faces, default=self.settings['color.faces'], colorformat='rgb', normalize=False)
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
        color : rgb-tuple or dict of rgb-tuple, optional
            The color specififcation for the edges.
            The default color is in the class settings.

        Returns
        -------
        list of :class:`Rhino.Geometry.Line`

        """
        edges = edges or list(self.mesh.edges())
        edge_color = colordict(color, edges, default=self.settings['color.edges'], colorformat='rgb', normalize=False)
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
