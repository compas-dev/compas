from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas_rhino

from compas_rhino.artists import Artist

from compas_rhino.artists.mixins import VertexArtist
from compas_rhino.artists.mixins import EdgeArtist
from compas_rhino.artists.mixins import FaceArtist

from compas.utilities import color_to_colordict
from compas.utilities import pairwise
from compas.geometry import add_vectors
from compas.geometry import scale_vector
from compas.geometry import centroid_polygon


__all__ = ['MeshArtist']


class MeshArtist(FaceArtist, EdgeArtist, VertexArtist, Artist):
    """A mesh artist defines functionality for visualising COMPAS meshes in Rhino.

    Parameters
    ----------
    mesh : compas.datastructures.Mesh
        A COMPAS mesh.
    layer : str, optional
        The name of the layer that will contain the mesh.

    Attributes
    ----------
    defaults : dict
        Default settings for color, scale, tolerance, ...

    Examples
    --------
    .. code-block:: python

        import compas
        from compas.datastructures import Mesh
        from compas_rhino.artists import MeshArtist

        mesh = Mesh.from_obj(compas.get('faces.obj'))

        artist = MeshArtist(mesh, layer='COMPAS::MeshArtist')
        artist.clear_layer()
        artist.draw_faces(join_faces=True)
        artist.draw_vertices(color={key: '#ff0000' for key in mesh.vertices_on_boundary()})
        artist.draw_edges()
        artist.redraw()

    """

    __module__ = "compas_rhino.artists"

    def __init__(self, mesh, layer=None):
        super(MeshArtist, self).__init__(layer=layer)
        self.mesh = mesh
        self.defaults.update({
            'color.vertex': (255, 255, 255),
            'color.edge': (0, 0, 0),
            'color.face': (210, 210, 210),
            'color.normal': (0, 255, 0),

            'scale.normal': 0.1,
        })

    @property
    def mesh(self):
        """Mesh: The mesh that should be painted."""
        return self.datastructure

    @mesh.setter
    def mesh(self, mesh):
        self.datastructure = mesh

    def draw_normals(self, keys=None, color=None, scale=None):
        keys = keys or list(self.mesh.vertices())
        scale = scale or self.defaults.get('scale.normal')
        colordict = color_to_colordict(color,
                                       keys,
                                       default=self.defaults.get('color.normal'),
                                       colorformat='rgb',
                                       normalize=False)
        lines = []
        for key in keys:
            a = self.mesh.vertex_coordinates(key)
            n = self.mesh.vertex_normal(key)
            b = add_vectors(a, scale_vector(n, scale))
            lines.append({
                'start': a,
                'end': b,
                'color': colordict[key],
                'name': "{}.normal.{}".format(self.mesh.name, key),
                'layer': self.layer,
                'arrow': 'end'})
        return compas_rhino.draw_lines(lines, layer=self.layer, clear=False, redraw=False)

    def draw_mesh(self, color=None, disjoint=False):
        """Draw the mesh as a consolidated RhinoMesh.

        Notes
        -----
        The mesh should be a valid Rhino Mesh object, which means it should have
        only triangular or quadrilateral faces.

        """
        key_index = self.mesh.key_index()
        vertices = self.mesh.get_vertices_attributes('xyz')
        faces = [[key_index[key] for key in self.mesh.face_vertices(fkey)] for fkey in self.mesh.faces()]
        new_faces = []
        for face in faces:
            f = len(face)
            if f == 3:
                new_faces.append(face + face[-1:])
            elif f == 4:
                new_faces.append(face)
            elif f > 4:
                centroid = len(vertices)
                vertices.append(centroid_polygon([vertices[index] for index in face]))
                for a, b in pairwise(face + face[0:1]):
                    new_faces.append([centroid, a, b, b])
            else:
                continue
        layer = self.layer
        name = "{}.mesh".format(self.mesh.name)
        return compas_rhino.draw_mesh(vertices, new_faces, layer=layer, name=name, color=color, disjoint=disjoint)

    def clear_mesh(self):
        compas_rhino.delete_objects(compas_rhino.get_objects(name="{}.mesh".format(self.mesh.name)))

    def clear_normals(self, keys=None):
        """Clear all normals previously drawn by the ``MeshArtist``.

        Parameters
        ----------
        keys : list, optional
            The keys of a specific set of normals that should be cleared.
            Default is to clear all normals.

        """
        if not keys:
            name = '{}.normal.*'.format(self.mesh.name)
            guids = compas_rhino.get_objects(name=name)
        else:
            guids = []
            for key in keys:
                name = '{}.normal.{}'.format(self.mesh.name, key)
                guid = compas_rhino.get_object(name=name)
                guids.append(guid)
        compas_rhino.delete_objects(guids)

    def clear(self):
        """Clear the vertices, faces and edges of the mesh, without clearing the
        other elements in the layer.

        """
        self.clear_vertices()
        self.clear_faces()
        self.clear_mesh()
        self.clear_edges()
        self.clear_normals()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    pass
