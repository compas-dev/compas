from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import ast
from compas.utilities import is_color_rgb
import compas_rhino
from compas.geometry import Point
from compas.geometry import Scale
from compas.geometry import Translation
from compas.geometry import Rotation

import Rhino
from Rhino.Geometry import Point3d

from ._object import Object


__all__ = ['NetworkObject']


class NetworkObject(Object):
    """Class for representing COMPAS networkes in Rhino.

    Parameters
    ----------
    network : :class:`compas.datastructures.Network`
        A network data structure.
    scene : :class:`compas.scenes.Scene`, optional
        A scene object.
    name : str, optional
        The name of the object.
    layer : str, optional
        The layer for drawing.
    visible : bool, optional
        Toggle for the visibility of the object.

    """

    def __init__(self, network, scene=None, name=None, visible=True, layer=None,
                 show_nodes=True, show_edges=True,
                 nodetext=None, edgetext=None,
                 nodecolor=None, edgecolor=None):
        super(NetworkObject, self).__init__(network, scene, name, visible, layer)
        self._guids = []
        self._guid_node = {}
        self._guid_edge = {}
        self._anchor = None
        self._location = None
        self._scale = None
        self._rotation = None
        self._node_color = None
        self._edge_color = None
        self._node_text = None
        self._edge_text = None
        self.show_nodes = show_nodes
        self.show_edges = show_edges
        self.node_color = nodecolor
        self.edge_color = edgecolor
        self.node_text = nodetext
        self.edge_text = edgetext

    @property
    def network(self):
        return self.item

    @network.setter
    def network(self, network):
        self.item = network
        self._guids = []
        self._guid_node = {}
        self._guid_edge = {}

    @property
    def anchor(self):
        """The node of the network that is anchored to the location of the object."""
        return self._anchor

    @anchor.setter
    def anchor(self, node):
        if self.network.has_node(node):
            self._anchor = node

    @property
    def location(self):
        """:class:`compas.geometry.Point`:
        The location of the object.
        Default is the origin of the world coordinate system.
        The object transformation is applied relative to this location.

        Setting this location will make a copy of the provided point object.
        Moving the original point will thus not affect the object's location.
        """
        if not self._location:
            self._location = Point(0, 0, 0)
        return self._location

    @location.setter
    def location(self, location):
        self._location = Point(*location)

    @property
    def scale(self):
        """float:
        A uniform scaling factor for the object in the scene.
        The scale is applied relative to the location of the object in the scene.
        """
        if not self._scale:
            self._scale = 1.0
        return self._scale

    @scale.setter
    def scale(self, scale):
        self._scale = scale

    @property
    def rotation(self):
        """list of float:
        The rotation angles around the 3 axis of the coordinate system
        with the origin placed at the location of the object in the scene.
        """
        if not self._rotation:
            self._rotation = [0, 0, 0]
        return self._rotation

    @rotation.setter
    def rotation(self, rotation):
        self._rotation = rotation

    @property
    def node_xyz(self):
        """dict : The view coordinates of the mesh object."""
        origin = Point(0, 0, 0)
        if self.anchor is not None:
            xyz = self.network.node_attributes(self.anchor, 'xyz')
            point = Point(* xyz)
            T1 = Translation.from_vector(origin - point)
            S = Scale.from_factors([self.scale] * 3)
            R = Rotation.from_euler_angles(self.rotation)
            T2 = Translation.from_vector(self.location)
            X = T2 * R * S * T1
        else:
            S = Scale.from_factors([self.scale] * 3)
            R = Rotation.from_euler_angles(self.rotation)
            T = Translation.from_vector(self.location)
            X = T * R * S
        network = self.network.transformed(X)
        node_xyz = {node: network.node_attributes(node, 'xyz') for node in network.nodes()}
        return node_xyz

    @property
    def guid_node(self):
        """dict: Map between Rhino object GUIDs and network node identifiers."""
        if not self._guid_node:
            self._guid_node = {}
        return self._guid_node

    @guid_node.setter
    def guid_node(self, values):
        self._guid_node = dict(values)

    @property
    def guid_edge(self):
        """dict: Map between Rhino object GUIDs and network edge identifiers."""
        if not self._guid_edge:
            self._guid_edge = {}
        return self._guid_edge

    @guid_edge.setter
    def guid_edge(self, values):
        self._guid_edge = dict(values)

    @property
    def guids(self):
        guids = self._guids
        guids += list(self.guid_node)
        guids += list(self.guid_edge)
        return guids

    @property
    def node_color(self):
        """dict: Dictionary mapping vertices to colors."""
        if not self._node_color:
            self._node_color = {node: self.artist.default_nodecolor for node in self.network.nodes()}
        return self._node_color

    @node_color.setter
    def node_color(self, node_color):
        if isinstance(node_color, dict):
            self._node_color = node_color
        elif is_color_rgb(node_color):
            self._node_color = {node: node_color for node in self.network.nodes()}

    @property
    def edge_color(self):
        """dict: Dictionary mapping edges to colors."""
        if not self._edge_color:
            self._edge_color = {edge: self.artist.default_edgecolor for edge in self.network.edges()}
        return self._edge_color

    @edge_color.setter
    def edge_color(self, edge_color):
        if isinstance(edge_color, dict):
            self._edge_color = edge_color
        elif is_color_rgb(edge_color):
            self._edge_color = {edge: edge_color for edge in self.network.edges()}

    def clear(self):
        compas_rhino.delete_objects(self.guids, purge=True)
        self._guids = []
        self._guid_node = {}
        self._guid_edge = {}

    def draw(self):
        """Draw the object representing the network.
        """
        self.clear()
        if not self.visible:
            return

        self.artist.node_xyz = self.node_xyz

        if self.show_nodes:
            nodes = list(self.network.nodes())
            node_color = self.node_color
            guids = self.artist.draw_nodes(nodes=nodes, color=node_color)
            self.guid_node = zip(guids, nodes)

        if self.show_edges:
            edges = list(self.network.edges())
            edge_color = self.edge_color
            guids = self.artist.draw_edges(edges=edges, color=edge_color)
            self.guid_edge = zip(guids, edges)

    def select(self):
        # there is currently no "general" selection method
        # for the entire mesh object
        raise NotImplementedError

    def select_node(self, message="Select one node."):
        """Select one node of the network.

        Returns
        -------
        int
            A node identifiers.
        """
        guid = compas_rhino.select_point(message=message)
        if guid and guid in self.guid_node:
            return self.guid_node[guid]

    def select_nodes(self, message="Select nodes."):
        """Select nodes of the network.

        Returns
        -------
        list
            A list of node identifiers.
        """
        guids = compas_rhino.select_points(message=message)
        nodes = [self.guid_node[guid] for guid in guids if guid in self.guid_node]
        return nodes

    def select_edges(self, message="Select edges."):
        """Select edges of the network.

        Returns
        -------
        list
            A list of edge identifiers.
        """
        guids = compas_rhino.select_lines(message=message)
        edges = [self.guid_edge[guid] for guid in guids if guid in self.guid_edge]
        return edges

    def modify(self):
        """Update the attributes of the network.

        Returns
        -------
        bool
            ``True`` if the update was successful.
            ``False`` otherwise.
        """
        names = sorted(self.network.attributes.keys())
        values = [str(self.network.attributes[name]) for name in names]
        values = compas_rhino.update_named_values(names, values)
        if values:
            for name, value in zip(names, values):
                try:
                    self.network.attributes[name] = ast.literal_eval(value)
                except (ValueError, TypeError):
                    self.network.attributes[name] = value
            return True
        return False

    def modify_nodes(self, nodes, names=None):
        """Update the attributes of the nodes.

        Parameters
        ----------
        nodes : list
            The identifiers of the nodes to update.
        names : list, optional
            The names of the atrtibutes to update.
            Default is to update all attributes.

        Returns
        -------
        bool
            ``True`` if the update was successful.
            ``False`` otherwise.

        """
        names = names or self.network.default_node_attributes.keys()
        names = sorted(names)
        values = self.network.node_attributes(nodes[0], names)
        if len(nodes) > 1:
            for i, name in enumerate(names):
                for node in nodes[1:]:
                    if values[i] != self.network.node_attribute(node, name):
                        values[i] = '-'
                        break
        values = map(str, values)
        values = compas_rhino.update_named_values(names, values)
        if values:
            for name, value in zip(names, values):
                if value == '-':
                    continue
                for node in nodes:
                    try:
                        self.network.node_attribute(node, name, ast.literal_eval(value))
                    except (ValueError, TypeError):
                        self.network.node_attribute(node, name, value)
            return True
        return False

    def modify_edges(self, edges, names=None):
        """Update the attributes of the edges.

        Parameters
        ----------
        edges : list
            The identifiers of the edges to update.
        names : list, optional
            The names of the atrtibutes to update.
            Default is to update all attributes.

        Returns
        -------
        bool
            ``True`` if the update was successful.
            ``False`` otherwise.
        """
        names = names or self.network.default_edge_attributes.keys()
        names = sorted(names)
        edge = edges[0]
        values = self.network.edge_attributes(edge, names)
        if len(edges) > 1:
            for i, name in enumerate(names):
                for edge in edges[1:]:
                    if values[i] != self.network.edge_attribute(edge, name):
                        values[i] = '-'
                        break
        values = map(str, values)
        values = compas_rhino.update_named_values(names, values)
        if values:
            for name, value in zip(names, values):
                if value == '-':
                    continue
                for edge in edges:
                    try:
                        value = ast.literal_eval(value)
                    except (SyntaxError, ValueError, TypeError):
                        pass
                    self.network.edge_attribute(edge, name, value)
            return True
        return False

    def move(self):
        """Move the entire mesh object to a different location."""
        raise NotImplementedError

    def move_node(self, node, constraint=None, allow_off=False):
        """Move a single node of the network object and update the data structure accordingly.

        Parameters
        ----------
        node : int
            The identifier of the node.

        Returns
        -------
        bool
            True if the operation was successful.
            False otherwise.
        """
        def OnDynamicDraw(sender, e):
            for ep in nbrs:
                sp = e.CurrentPoint
                e.Display.DrawDottedLine(sp, ep, color)

        color = Rhino.ApplicationSettings.AppearanceSettings.FeedbackColor
        nbrs = [self.network.node_coordinates(nbr) for nbr in self.network.node_neighbors(node)]
        nbrs = [Point3d(*xyz) for xyz in nbrs]

        gp = Rhino.Input.Custom.GetPoint()

        gp.SetCommandPrompt('Point to move to?')
        gp.DynamicDraw += OnDynamicDraw
        if constraint:
            gp.Constrain(constraint, allow_off)

        gp.Get()
        if gp.CommandResult() != Rhino.Commands.Result.Success:
            return False

        self.network.node_attributes(node, 'xyz', list(gp.Point()))
        return True
