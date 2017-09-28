from compas.datastructures.network import Network

from compas.geometry import centroid_points

from compas_blender.utilities import draw_bmesh
from compas_blender.utilities import deselect_all_objects
from compas_blender.utilities import xdraw_cubes
from compas_blender.utilities import xdraw_labels
from compas_blender.utilities import xdraw_lines

from compas_blender.geometry import bmesh_data

import json

try:
    import bpy
except ImportError:
    pass


__author__     = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2016, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'liew@arch.ethz.ch'


__all__ = [
    'draw_network',
    'network_from_bmesh',
    'display_network_vertex_labels',
    'display_network_edge_labels',
    'display_network_face_labels'
]


# ==============================================================================
# drawing
# ==============================================================================

def draw_network(network, type='mesh', layer=0, show_vertices=0.01, show_edges=0.005, show_faces=True,
                 vertex_name_attr=[], edge_name_attr=[], face_name_attr=[]):
    """ Draw a representation of a Network datastructure.

    Parameters:
        network (obj): Network datastructure.
        type (str): Draw as 'mesh' or 'lines'.
        layer (int): Layer to draw Network on.
        show_vertices (float): Size of vertex cubes when type is 'lines'.
        show_edges (float): Size of lines when type is 'lines'.
        show_faces (bool): Draw Network faces.
        vertex_name_attr (list): Attributes to show in vertex names.
        edge_name_attr (list): Attributes to show in edge names.
        face_name_attr (list): Attributes to show in face names.

    Returns:
        obj: Created Blender mesh or None.
    """
    keys = list(network.vertices())
    vertices = [network.vertex_coordinates(key) for key in keys]

    k_i = network.key_index()
    uv_i = network.uv_index()
    u_v = list(network.edges())
    edges = [(k_i[u], k_i[v]) for u, v in u_v]

    fkeys = list(network.faces())
    faces = [network.face[fkey] for fkey in fkeys]

    if type == 'mesh':

        return draw_bmesh('network', vertices=vertices, edges=edges, faces=faces)

    elif type == 'lines':

        if show_vertices:
            cubes_vertices = []
            for key in keys:
                vertex = network.vertex[key]
                xyz = network.vertex_coordinates(key)
                color = 'black' if vertex.get('is_fixed', None) else 'white'
                name_dic = {}
                for attr in vertex_name_attr:
                    name_dic[attr] = vertex.get(attr, 'None')
                name = json.dumps(name_dic)
                cubes_vertices.append({'radius': show_vertices, 'pos': xyz, 'color': color, 'name': name})
            xdraw_cubes(cubes_vertices)

        if show_edges:
            lines_edges = []
            for u, v in u_v:
                sp = network.vertex_coordinates(u)
                ep = network.vertex_coordinates(v)
                i = uv_i[(u, v)]
                color = network.edge[u][v].get('color', 'grey')
                name_dic = {}
                for attr in edge_name_attr:
                    name_dic[attr] = network.edge[u][v].get(attr, 'None')
                name = json.dumps(name_dic)
                lines_edges.append({'name': name, 'start': sp, 'end': ep, 'layer': layer, 'color': color, 'width': show_edges})
            xdraw_lines(lines_edges)

        if show_faces:
            for fkey in fkeys:
                facedata = network.facedata[fkey]
                color = facedata.get('color', 'grey')
                pts = [vertices[i] for i in network.face[fkey]]
                name_dic = {}
                for attr in face_name_attr:
                    name_dic[attr] = facedata.get(attr, 'None')
                name = json.dumps(name_dic)
                draw_bmesh(name=name, vertices=pts, faces=[list(range(len(pts)))], layer=layer, color=color)

    deselect_all_objects()


def draw_network_as_lines():
    raise NotImplementedError


def display_network_vertex_labels(network, layer=0):
    """ Draw Network vertex labels.

    Parameters:
        network (obj): Network datastructure.
        layer (int): Layer to draw labels on.

    Returns:
        None
    """
    keys = list(network.vertices())
    vertices = [network.vertex_coordinates(key) for key in keys]
    labels = []
    for i, xyz in enumerate(vertices):
        labels.append({'name': 'V{0}'.format(i), 'pos': xyz, 'layer': layer})
    xdraw_labels(labels)


def display_network_edge_labels(network, layer=0):
    """ Draw Network edge labels.

    Parameters:
        network (obj): Network datastructure.
        layer (int): Layer to draw labels on.

    Returns:
        None
    """
    uv_i = network.uv_index()
    u_v = list(network.edges())
    labels = []
    for u, v in u_v:
        sp = network.vertex_coordinates(u)
        ep = network.vertex_coordinates(v)
        xyz = centroid_points([sp, ep])
        i = uv_i[(u, v)]
        labels.append({'name': 'E{0}'.format(i), 'pos': xyz, 'layer': layer})
    xdraw_labels(labels)


def display_network_face_labels(network, layer=0):
    """ Draw Network face labels.

    Parameters:
        network (obj): Network datastructure.
        layer (int): Layer to draw labels on.

    Returns:
        None
    """
    fkeys = list(network.faces())
    labels = []
    for fkey in fkeys:
        xyz = centroid_points([network.vertex_coordinates(i) for i in network.face[fkey]])
        labels.append({'name': 'F{0}'.format(fkey), 'pos': xyz, 'layer': layer})
    xdraw_labels(labels)


# ==============================================================================
# constructors
# ==============================================================================

def network_from_bmesh(bmesh, add_faces=False):
    """ Create a Network datastructure from a Blender mesh.

    Parameters:
        bmesh (obj): Blender mesh object.
        add_faces (bool): Add the bmesh faces to the Network.

    Returns:
        obj: Network object.
    """
    vertices, edges, faces = bmesh_data(bmesh)
    network = Network.from_vertices_and_edges(vertices, edges)
    if add_faces:
        for c, face in enumerate(faces):
            network.add_face(face, fkey=c)
    return network


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    from compas_blender.utilities import delete_all_objects
    from compas_blender.utilities import draw_plane

    network = network_from_bmesh(draw_plane(dx=1, dy=1, bracing='cross'), add_faces=True)

    delete_all_objects()

    draw_network(network, type='lines')
    display_network_vertex_labels(network)
    display_network_edge_labels(network)
    display_network_face_labels(network)
