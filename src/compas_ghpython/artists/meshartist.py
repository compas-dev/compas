from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_ghpython

from compas_ghpython.artists.mixins import VertexArtist
from compas_ghpython.artists.mixins import EdgeArtist
from compas_ghpython.artists.mixins import FaceArtist


__all__ = ['MeshArtist']


class MeshArtist(FaceArtist, EdgeArtist, VertexArtist):
    """A mesh artist defines functionality for visualising COMPAS meshes in GhPython.

    Parameters
    ----------
    mesh : compas.datastructures.Mesh
        A COMPAS mesh.

    Attributes
    ----------
    defaults : dict
        Default settings for color, scale, tolerance, ...

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
        self.mesh = mesh
        self.defaults = {
            'color.vertex' : (255, 255, 255),
            'color.edge'   : (0, 0, 0),
            'color.face'   : (210, 210, 210),
        }

    @property
    def mesh(self):
        """compas.datastructures.Mesh: The mesh that should be painted."""
        return self.datastructure

    @mesh.setter
    def mesh(self, mesh):
        self.datastructure = mesh

    def draw(self, color=None):
        key_index = self.mesh.key_index()
        vertices = self.mesh.get_vertices_attributes('xyz')
        faces = [[key_index[key] for key in self.mesh.face_vertices(fkey)] for fkey in self.mesh.faces()]
        new_faces = []
        for face in faces:
            l = len(face)
            if l == 3:
                new_faces.append(face + [face[-1]])
            elif l == 4:
                new_faces.append(face)
        return compas_ghpython.xdraw_mesh(vertices, new_faces, color)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    from compas.datastructures import Mesh
    from compas.geometry import Polyhedron

    from compas_ghpython.artists.meshartist import MeshArtist

    poly = Polyhedron.generate(12)

    mesh = Mesh.from_vertices_and_faces(poly.vertices, poly.faces)

    artist = MeshArtist(mesh)

    vertices = artist.draw_vertices()
    faces = artist.draw_faces()
    edges = artist.draw_edges()
