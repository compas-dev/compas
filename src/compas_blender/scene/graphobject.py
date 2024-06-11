from typing import List

import bpy  # type: ignore

import compas_blender
import compas_blender.objects
from compas.geometry import Line
from compas.geometry import Sphere
from compas.scene import GraphObject as BaseGraphObject
from compas_blender import conversions

from .sceneobject import BlenderSceneObject


class GraphObject(BlenderSceneObject, BaseGraphObject):
    """Scene object for drawing graph data structures in Blender.

    Parameters
    ----------
    node_u : int, optional
        Number of segments in the U direction of the node spheres.
        Default is ``16``.
    node_v : int, optional
        Number of segments in the V direction of the node spheres.
        Default is ``16``.
    **kwargs : dict, optional
        Additional keyword arguments.
        For more info,
        see :class:`compas_blender.scene.BlenderSceneObject` and :class:`compas.scene.GraphObject`.

    Attributes
    ----------
    node_u : int
        Number of segments in the U direction of the node spheres.
    node_v : int
        Number of segments in the V direction of the node spheres.
    nodeobjects : list[:blender:`bpy.types.Object`]
        List of Blender objects representing the nodes.
    edgeobjects : list[:blender:`bpy.types.Object`]
        List of Blender objects representing the edges.

    """

    def __init__(self, node_u=16, node_v=16, **kwargs: dict):
        super().__init__(**kwargs)
        self.nodeobjects = []
        self.edgeobjects = []
        self.node_u = node_u
        self.node_v = node_v

    # ==========================================================================
    # clear
    # ==========================================================================

    def clear_nodes(self):
        """Clear all objects contained in the node collection.

        Returns
        -------
        None

        """
        compas_blender.objects.delete_objects(self.nodeobjects)

    def clear_edges(self):
        """Clear all objects contained in the edge collection.

        Returns
        -------
        None

        """
        compas_blender.objects.delete_objects(self.edgeobjects)

    # ==========================================================================
    # draw
    # ==========================================================================

    def draw(self) -> list[bpy.types.Object]:
        """Draw the graph.

        Returns
        -------
        list[:blender:`bpy.types.Object`]
            The objects created in Blender.

        """
        self._guids = self.draw_nodes() + self.draw_edges()
        return self.guids

    def draw_nodes(self) -> List[bpy.types.Object]:
        """Draw a selection of nodes.

        Returns
        -------
        list[:blender:`bpy.types.Object`]

        """
        objects = []

        nodes = list(self.graph.nodes()) if self.show_nodes is True else self.show_nodes or []

        for node in nodes:
            name = f"{self.graph.name}.node.{node}"
            color = self.nodecolor[node]
            point = self.graph.node_coordinates(node)

            # # there is no such thing as a sphere data block
            # # this doesn't work with application of worl transformation matrix
            # bpy.ops.mesh.primitive_uv_sphere_add(location=point, radius=self.nodesize, segments=self.node_u, ring_count=self.node_v)
            # obj = bpy.context.object
            # self.update_object(obj, name=name, color=color, collection=self.collection)
            sphere = Sphere(radius=self.nodesize, point=point)
            sphere.resolution_u = self.node_u
            sphere.resolution_v = self.node_v
            mesh = conversions.vertices_and_faces_to_blender_mesh(sphere.vertices, sphere.faces, name=name)
            obj = self.create_object(mesh, name=name)
            self.update_object(obj, color=color, collection=self.collection)

            objects.append(obj)

        self.nodeobjects = objects
        return objects

    def draw_edges(self) -> List[bpy.types.Object]:
        """Draw a selection of edges.

        Returns
        -------
        list[:blender:`bpy.types.Object`]

        """
        objects = []

        edges = list(self.graph.edges()) if self.show_edges is True else self.show_edges or []

        for u, v in edges:
            name = f"{self.graph.name}.edge.{u}-{v}"
            color = self.edgecolor[u, v]
            curve = conversions.line_to_blender_curve(Line(self.graph.node_coordinates(u), self.graph.node_coordinates(v)))

            obj = self.create_object(curve, name=name)
            self.update_object(obj, color=color, collection=self.collection)
            objects.append(obj)

        self.edgeobjects = objects
        return objects
