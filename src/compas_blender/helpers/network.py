from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.datastructures import Network

from compas_blender.geometry import BlenderMesh


__author__     = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2017, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'liew@arch.ethz.ch'


__all__ = [
    'network_from_bmesh'
]


def network_from_bmesh(bmesh):
    """ Create a Network datastructure from a Blender mesh.

    Parameters:
        bmesh (obj): Blender mesh object.

    Returns:
        obj: Network object.
    """
    blendermesh = BlenderMesh(bmesh)
    vertices = blendermesh.get_vertex_coordinates()
    edges = blendermesh.get_edge_vertex_indices()
    network = Network.from_vertices_and_edges(vertices=vertices, edges=edges)
    return network


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    from compas_blender.utilities import get_objects
    
    network = network_from_bmesh(bmesh=get_objects(layer=0)[0])
    
    print(network)