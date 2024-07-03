from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.scene import GraphObject as BaseGraphObject
from compas_rhino import conversions

from .sceneobject import GHSceneObject


class GraphObject(GHSceneObject, BaseGraphObject):
    """Scene object for drawing graph data structures."""

    def draw(self):
        """Draw the entire graph with default color settings.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.Point3d`, :rhino:`Rhino.Geometry.Line`]
            List of created Rhino geometries.
        """
        self._guids = self.draw_edges() + self.draw_nodes()
        return self.guids

    def draw_nodes(self):
        """Draw a selection of nodes.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.Point3d`]

        """
        points = []

        nodes = list(self.graph.nodes()) if self.show_nodes is True else self.show_nodes or []

        for node in nodes:
            points.append(conversions.point_to_rhino(self.node_xyz[node]))

        return points

    def draw_edges(self, edges=None):
        """Draw a selection of edges.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.Line`]

        """
        lines = []

        edges = list(self.graph.edges()) if self.show_edges is True else self.show_edges or []

        for edge in edges:
            lines.append(conversions.line_to_rhino((self.node_xyz[edge[0]], self.node_xyz[edge[1]])))

        return lines
