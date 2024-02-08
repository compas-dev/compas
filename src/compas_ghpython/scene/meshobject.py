from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.scene import MeshObject as BaseMeshObject
from compas.colors import Color
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

    def __init__(self, mesh, **kwargs):
        super(MeshObject, self).__init__(mesh=mesh, **kwargs)

    def draw(self, color=None, vertexcolors=None, facecolors=None, disjoint=False):
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
        if not vertexcolors and not facecolors:
            color = Color.coerce(color) or self.color

        vertex_index = self.mesh.vertex_index()  # type: ignore
        vertex_xyz = self.vertex_xyz

        vertices = [vertex_xyz[vertex] for vertex in self.mesh.vertices()]  # type: ignore
        faces = [[vertex_index[vertex] for vertex in self.mesh.face_vertices(face)] for face in self.mesh.faces()]  # type: ignore

        geometry = conversions.vertices_and_faces_to_rhino(
            vertices,
            faces,
            color=color,
            vertexcolors=vertexcolors,
            facecolors=facecolors,
            disjoint=disjoint,
        )

        self._guids = [geometry]
        return self.guids

    def draw_vertices(self, vertices=None):
        """Draw a selection of vertices.

        Parameters
        ----------
        vertices : list[int], optional
            A selection of vertices to draw.
            Default is None, in which case all vertices are drawn.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.Point3d`]

        """
        points = []

        for vertex in vertices or self.mesh.vertices():  # type: ignore
            points.append(conversions.point_to_rhino(self.vertex_xyz[vertex]))

        return points

    def draw_edges(self, edges=None):
        """Draw a selection of edges.

        Parameters
        ----------
        edges : list[tuple[int, int]], optional
            A selection of edges to draw.
            The default is None, in which case all edges are drawn.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.Line`]

        """
        lines = []

        for edge in edges or self.mesh.edges():  # type: ignore
            lines.append(conversions.line_to_rhino((self.vertex_xyz[edge[0]], self.vertex_xyz[edge[1]])))

        return lines

    def draw_faces(self, faces=None, color=None):
        """Draw a selection of faces.

        Parameters
        ----------
        faces : list[int], optional
            A selection of faces to draw.
            The default is None, in which case all faces are drawn.
        color : :class:`compas.colors.Color` | dict[int, :class:`compas.colors.Color`], optional
            The color specification for the faces.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.Mesh`]

        """
        faces = faces or self.mesh.faces()  # type: ignore

        self.facecolor = color

        meshes = []

        for face in faces:
            color = self.facecolor[face]  # type: ignore
            vertices = [self.vertex_xyz[vertex] for vertex in self.mesh.face_vertices(face)]  # type: ignore
            facet = ngon(len(vertices))
            if facet:
                meshes.append(conversions.vertices_and_faces_to_rhino(vertices, [facet]))

        return meshes
