from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.scene import MeshObject as BaseMeshObject
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


class MeshObject(GHSceneObject, BaseMeshObject):
    """Scene object for drawing mesh data structures.

    Parameters
    ----------
    disjoint : bool, optional
        Draw the mesh as disjoint faces.
    **kwargs : dict, optional
        Additional keyword arguments.

    Attributes
    ----------
    disjoint : bool
        Draw the mesh as disjoint faces.

    """

    def __init__(self, disjoint=False, **kwargs):
        super(MeshObject, self).__init__(**kwargs)
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
            if len(self.vertexcolor):  # type: ignore
                vertexcolors = [self.vertexcolor[vertex] for vertex in self.mesh.vertices()]  # type: ignore

            facecolors = []
            if len(self.facecolor):  # type: ignore
                facecolors = [self.facecolor[face] for face in self.mesh.faces()]  # type: ignore

            vertex_index = self.mesh.vertex_index()

            vertices = [self.mesh.vertex_attributes(vertex, "xyz") for vertex in self.mesh.vertices()]
            faces = [[vertex_index[vertex] for vertex in self.mesh.face_vertices(face)] for face in self.mesh.faces()]

            geometry = conversions.vertices_and_faces_to_rhino(
                vertices,
                faces,
                color=self.color,
                vertexcolors=vertexcolors,
                facecolors=facecolors,
                disjoint=self.disjoint,
            )

            geometry.Transform(conversions.transformation_to_rhino(self.worldtransformation))

            self._guids.append(geometry)

        elif self.show_faces:
            self.draw_faces()

        self.draw_vertices()
        self.draw_edges()

        return self.guids

    def draw_vertices(self):
        """Draw a selection of vertices.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.Point3d`]

        """
        points = []

        vertices = list(self.mesh.vertices()) if self.show_vertices is True else self.show_vertices or []

        transformation = conversions.transformation_to_rhino(self.worldtransformation)

        if vertices:
            for vertex in vertices:
                geometry = conversions.point_to_rhino(self.mesh.vertex_attributes(vertex, "xyz"))
                geometry.Transform(transformation)
                points.append(geometry)

        return points

    def draw_edges(self):
        """Draw a selection of edges.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.Line`]

        """
        lines = []

        edges = list(self.mesh.edges()) if self.show_edges is True else self.show_edges or []

        transformation = conversions.transformation_to_rhino(self.worldtransformation)

        if edges:
            for edge in edges:
                line = self.mesh.edge_line(edge)
                geometry = conversions.line_to_rhino(line)
                geometry.Transform(transformation)
                lines.append(geometry)

        return lines

    def draw_faces(self):
        """Draw a selection of faces.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.Mesh`]

        """
        meshes = []

        faces = list(self.mesh.faces()) if self.show_faces is True else self.show_faces or []

        transformation = conversions.transformation_to_rhino(self.worldtransformation)

        if faces:
            for face in faces:
                color = self.facecolor[face]  # type: ignore
                vertices = [self.mesh.vertex_attributes(vertex, "xyz") for vertex in self.mesh.face_vertices(face)]  # type: ignore
                facet = _create_ngon(len(vertices))

                if facet:
                    geometry = conversions.vertices_and_faces_to_rhino(vertices, [facet], color=color)
                    geometry.Transform(transformation)
                    meshes.append(geometry)

        return meshes
