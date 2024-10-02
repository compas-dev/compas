from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.scene import VolMeshObject as BaseVolMeshObject
from compas_rhino import conversions

from .sceneobject import GHSceneObject


def _create_ngon(vertex_count):
    if vertex_count < 3:
        return
    if vertex_count == 3:
        return [0, 1, 2]
    if vertex_count == 4:
        return [0, 1, 2, 3]
    return list(range(vertex_count))


class VolMeshObject(GHSceneObject, BaseVolMeshObject):
    """Scene object for drawing volmesh data structures."""

    def draw(self):
        """Draw a selection of cells.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.Mesh`]
            List of created Rhino meshes.

        """
        guids = []

        if self.show_vertices:
            guids += self.draw_vertices()
        if self.show_edges:
            guids += self.draw_edges()
        if self.show_faces:
            guids += self.draw_faces()
        if self.show_cells:
            guids += self.draw_cells()

        self._guids = guids
        return self.guids

    def draw_vertices(self):
        """Draw a selection of vertices.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.Point3d`]

        """
        points = []

        vertices = list(self.volmesh.vertices()) if self.show_vertices is True else self.show_vertices or []

        for vertex in vertices:
            points.append(conversions.point_to_rhino(self.vertex_xyz[vertex]))

        return points

    def draw_edges(self):
        """Draw a selection of edges.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.Line`]

        """
        lines = []

        edges = list(self.volmesh.edges()) if self.show_edges is True else self.show_edges or []

        for edge in edges:
            lines.append(conversions.line_to_rhino((self.vertex_xyz[edge[0]], self.vertex_xyz[edge[1]])))

        return lines

    def draw_faces(self):
        """Draw a selection of faces.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.Mesh`]

        """
        meshes = []

        faces = list(self.volmesh.faces()) if self.show_faces is True else self.show_faces or []

        for face in faces:
            color = self.facecolor[face]
            vertices = [self.vertex_xyz[vertex] for vertex in self.volmesh.face_vertices(face)]
            facet = _create_ngon(len(vertices))
            if facet:
                meshes.append(conversions.vertices_and_faces_to_rhino(vertices, [facet], color=color))

        return meshes

    def draw_cells(self):
        """Draw a selection of cells.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.Mesh`]

        """
        meshes = []

        cells = list(self.volmesh.cells()) if self.show_cells is True else self.show_cells or []

        for cell in cells:
            color = self.cellcolor[cell]

            vertices = self.volmesh.cell_vertices(cell)
            faces = self.volmesh.cell_faces(cell)
            vertex_index = dict((vertex, index) for index, vertex in enumerate(vertices))
            vertices = [self.vertex_xyz[vertex] for vertex in vertices]
            faces = [[vertex_index[vertex] for vertex in self.volmesh.halfface_vertices(face)] for face in faces]

            mesh = conversions.vertices_and_faces_to_rhino(vertices, faces, disjoint=True, color=color)
            meshes.append(mesh)

        return meshes
