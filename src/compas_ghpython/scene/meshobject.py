from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.colors import Color
from compas.scene import MeshObject as BaseMeshObject
from compas_rhino import conversions
from compas_rhino.scene.helpers import ngon

from .sceneobject import GHSceneObject


class MeshObject(GHSceneObject, BaseMeshObject):
    """Scene object for drawing mesh data structures.

    Parameters
    ----------
    mesh : :class:`compas.datastructures.Mesh`
        A COMPAS mesh.
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, mesh, disjoint=False, **kwargs):
        super(MeshObject, self).__init__(mesh=mesh, **kwargs)
        self.disjoint = disjoint

    def draw(self):
        """Draw the mesh.

        Parameters
        ----------
        color : tuple[int, int, int] | tuple[float, float, float] | :class:`compas.colors.Color`, optional
            The color of the mesh.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.Mesh`]

        """
        # the rhino scene object can set an overal color and component colors simultaneously
        # because it can set an overall color on the mesh object attributes
        # this is not possible in GH (since there is no such object)
        # either we set an overall color or we set component colors
        self._guids = []

        if self.show_faces is True:
            vertexcolors = []
            if len(self.vertexcolor):
                vertexcolors = [self.vertexcolor[vertex] for vertex in self.mesh.vertices()]

            facecolors = []
            if len(self.facecolor):
                facecolors = [self.facecolor[face] for face in self.mesh.faces()]

            color = None
            if not vertexcolors and not facecolors:
                color = self.color

            vertex_index = self.mesh.vertex_index()
            vertex_xyz = self.vertex_xyz

            vertices = [vertex_xyz[vertex] for vertex in self.mesh.vertices()]
            faces = [[vertex_index[vertex] for vertex in self.mesh.face_vertices(face)] for face in self.mesh.faces()]

            geometry = conversions.vertices_and_faces_to_rhino(
                vertices,
                faces,
                color=color,
                vertexcolors=vertexcolors,
                facecolors=facecolors,
                disjoint=self.disjoint,
            )

            # geometry.Transform(conversions.transformation_to_rhino(self.worldtransformation))

            self._guids.append(geometry)

        elif self.show_faces:
            self._guids += self.draw_faces()

        if self.show_vertices:
            self._guids += self.draw_vertices()

        if self.show_edges:
            self._guids += self.draw_edges()

        return self.guids

    def draw_vertices(self):
        """Draw a selection of vertices.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.Point3d`]

        """
        points = []

        vertices = list(self.mesh.vertices()) if self.show_vertices is True else self.show_vertices or []

        if vertices:
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

        edges = list(self.mesh.edges()) if self.show_edges is True else self.show_edges or []

        if edges:
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

        faces = list(self.mesh.faces()) if self.show_faces is True else self.show_faces or []

        if faces:
            for face in faces:
                color = self.facecolor[face]
                vertices = [self.vertex_xyz[vertex] for vertex in self.mesh.face_vertices(face)]
                facet = ngon(len(vertices))
                if facet:
                    meshes.append(conversions.vertices_and_faces_to_rhino(vertices, [facet], color=color))

        return meshes
