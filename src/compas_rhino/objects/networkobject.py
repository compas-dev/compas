from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas_rhino

from compas_rhino.objects.base import BaseObject

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

    Attributes
    ----------
    guid_node : dict
        Dictionary mapping Rhino object GUIDs to COMPAS network node identifiers.
    guid_edge : dict
        Dictionary mapping Rhino object GUIDs to COMPAS network edge identifiers.

    Examples
    --------
    .. code-block:: python

        import compas
        from compas.datastructures import Network
        from compas_rhino.objects import NetworkObject

        network = Network.from_obj(compas.get('tubenetwork.off'))
        networkobject = NetworkObject(network, name='NetworkObject', layer='COMPAS::NetworkObject', visible=True)
        networkobject.clear()
        networkobject.clear_layer()
        networkobject.draw()
        networkobject.redraw()

        nodes = networkobject.select_nodes()
        if networkobject.modify_nodes(nodes):
            networkobject.clear()
            networkobject.draw()
            networkobject.redraw()

    """

    def __init__(self, network, scene=None, name=None, layer=None, visible=True, settings=None):
        super(NetworkObject, self).__init__(network, scene, name, layer, visible, settings)

    @property
    def network(self):
        return self.item

    @network.setter
    def network(self, network):
        self.item = network

    def clear(self):
        self.artist.clear()

    def draw(self):
        """Draw the object representing the network.
        """
        if not self.visible:
            return
        self.artist.draw()

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

    def modify(self):
        return network_update_attributes(self.network)

    def modify_nodes(self, nodes):
        """Modify the attributes of the nodes of the network item.

        Parameters
        ----------
        nodes : list
            The identifiers of the nodes of which the attributes will be updated.

        Returns
        -------
        bool
            ``True`` if the attributes were successfully updated.
            ``False`` otherwise.
        """
        return network_update_node_attributes(self.network, nodes)

    def modify_edges(self, edges):
        """Modify the attributes of the edges of the network item.

        Parameters
        ----------
        edges : list
            The identifiers of the edges of which the attributes will be updated.

        Returns
        -------
        bool
            ``True`` if the attributes were successfully updated.
            ``False`` otherwise.
        """
        return network_update_edge_attributes(self.network, edges)

    def move(self):
        raise NotImplementedError

    def move_node(self, node):
        return network_move_node(self.network, node)


# ============================================================================
# Main
# ============================================================================

if __name__ == "__main__":
    pass
