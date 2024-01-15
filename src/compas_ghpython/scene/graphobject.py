from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_rhino import conversions

from compas.scene import GraphObject as BaseGraphObject
from .sceneobject import GHSceneObject


class GraphObject(GHSceneObject, BaseGraphObject):
    """Scene object for drawing graph data structures.

    Parameters
    ----------
    graph : :class:`compas.datastructures.Graph`
        A COMPAS graph.
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, graph, **kwargs):
        super(GraphObject, self).__init__(graph=graph, **kwargs)

    def draw(self):
        """Draw the entire graph with default color settings.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.Point3d`, :rhino:`Rhino.Geometry.Line`]
            List of created Rhino geometries.
        """
        self._guids = self.draw_edges() + self.draw_nodes()
        return self.guids

    def draw_nodes(self, nodes=None):
        """Draw a selection of nodes.

        Parameters
        ----------
        nodes: list[hashable], optional
            The selection of nodes that should be drawn.
            Default is None, in which case all nodes are drawn.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.Point3d`]

        """
        points = []

        for node in nodes or self.graph.nodes():  # type: ignore
            points.append(conversions.point_to_rhino(self.node_xyz[node]))

        return points

    def draw_edges(self, edges=None):
        """Draw a selection of edges.

        Parameters
        ----------
        edges : list[tuple[hashable, hashable]], optional
            A list of edges to draw.
            The default is None, in which case all edges are drawn.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.Line`]

        """
        lines = []

        for edge in edges or self.graph.edges():  # type: ignore
            lines.append(conversions.line_to_rhino((self.node_xyz[edge[0]], self.node_xyz[edge[1]])))

        return lines
