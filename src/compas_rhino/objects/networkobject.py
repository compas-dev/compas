from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas_rhino
from compas.geometry import Point
from compas.geometry import Scale
from compas.geometry import Translation
from compas.geometry import Rotation
from compas_rhino.objects._object import BaseObject
from compas_rhino.objects.modify import network_update_attributes
from compas_rhino.objects.modify import network_update_node_attributes
from compas_rhino.objects.modify import network_update_edge_attributes
from compas_rhino.objects.modify import network_move_node


__all__ = ['NetworkObject']


class NetworkObject(BaseObject):
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
    settings : dict, optional
        A dictionary of settings.

    """

    modify = network_update_attributes
    modify_nodes = network_update_node_attributes
    modify_edges = network_update_edge_attributes

    def __init__(self, network, scene=None, name=None, layer=None, visible=True, settings=None):
        super(NetworkObject, self).__init__(network, scene, name, layer, visible)
        self._location = None
        self._scale = None
        self._rotation = None
        self.settings.update({
            'color.nodes': (255, 255, 255),
            'color.edges': (0, 0, 0),
            'show.nodes': True,
            'show.edges': True,
            'show.nodelabels': False,
            'show.edgelabels': False,
        })
        if settings:
            self.settings.update(settings)

    @property
    def network(self):
        return self.item

    @network.setter
    def network(self, network):
        self.item = network

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
    def vertex_xyz(self):
        S = Scale.from_factors([self.scale] * 3)
        R = Rotation.from_euler_angles(self.rotation)
        T = Translation.from_vector(self.location)
        network = self.network.transformed(T * R * S)
        node_xyz = {node: network.node_attributes(node, 'xyz') for node in network.nodes()}
        return node_xyz

    def clear(self):
        self.artist.clear()

    def draw(self):
        """Draw the object representing the network.
        """
        self.clear()
        if not self.visible:
            return
        self.artist.node_xyz = self.node_xyz
        if self.settings['show.nodes']:
            self.artist.draw_nodes(color=self.settings['color.nodes'])
            if self.settings['show.nodelabels']:
                self.artist.draw_nodelabels(color=self.settings['color.nodes'])
        if self.settings['show.edges']:
            self.artist.draw_edges(color=self.settings['color.edges'])
            if self.settings['show.edgelabels']:
                self.artist.draw_edgelabels(color=self.settings['color.edges'])
        self.redraw()

    def select(self):
        raise NotImplementedError

    def select_nodes(self):
        """Select nodes of the network.

        Returns
        -------
        list
            A list of node identifiers.
        """
        guids = compas_rhino.select_points()
        nodes = [self.artist.guid_node[guid] for guid in guids if guid in self.artist.guid_node]
        return nodes

    def select_edges(self):
        """Select edges of the network.

        Returns
        -------
        list
            A list of edge identifiers.
        """
        guids = compas_rhino.select_lines()
        edges = [self.artist.guid_edge[guid] for guid in guids if guid in self.artist.guid_edge]
        return edges

    def move(self):
        raise NotImplementedError

    def move_node(self, node):
        return network_move_node(self.network, node)


# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    pass
