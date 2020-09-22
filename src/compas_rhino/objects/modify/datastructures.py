from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import ast

import compas_rhino

from compas.geometry import add_vectors

import Rhino
import clr

clr.AddReference('Rhino.UI')
import Rhino.UI  # noqa: E402
from Rhino.Geometry import Point3d  # noqa: E402

try:
    from compas_rhino.forms import PropertyListForm
except ImportError:
    from Rhino.UI.Dialogs import ShowPropertyListBox


__all__ = [
    'network_update_attributes',
    'network_update_node_attributes',
    'network_update_edge_attributes',

    'network_move_node',

    'mesh_update_attributes',
    'mesh_update_vertex_attributes',
    'mesh_update_face_attributes',
    'mesh_update_edge_attributes',

    'mesh_move_vertex',
    'mesh_move_vertices',
    'mesh_move_face',
]


def _update_named_values(names, values, message='', title='Update named values'):
    try:
        dialog = PropertyListForm(names, values)
    except Exception:
        values = ShowPropertyListBox(message, title, names, values)
    else:
        if dialog.ShowModal(Rhino.UI.RhinoEtoApp.MainWindow):
            values = dialog.values
        else:
            values = None
    return values


def network_update_attributes(network):
    """Update the attributes of a network.

    Parameters
    ----------
    network : :class:`compas.datastructures.Network`
        A network object.

    Returns
    -------
    bool
        ``True`` if the update was successful.
        ``False`` otherwise.
    """
    names = sorted(network.attributes.keys())
    values = [str(network.attributes[name]) for name in names]
    values = _update_named_values(names, values)
    if values:
        for name, value in zip(names, values):
            try:
                network.attributes[name] = ast.literal_eval(value)
            except (ValueError, TypeError):
                network.attributes[name] = value
        return True
    return False


def network_update_node_attributes(network, nodes, names=None):
    """Update the attributes of the nodes of a network.

    Parameters
    ----------
    network : :class:`compas.datastructures.Network`
        A network object.
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
    names = names or network.default_node_attributes.nodes()
    names = sorted(names)
    values = network.node_attributes(nodes[0], names)
    if len(nodes) > 1:
        for i, name in enumerate(names):
            for node in nodes[1:]:
                if values[i] != network.node_attribute(node, name):
                    values[i] = '-'
                    break
    values = map(str, values)
    values = _update_named_values(names, values)
    if values:
        for name, value in zip(names, values):
            if value == '-':
                continue
            for node in nodes:
                try:
                    network.node_attribute(node, name, ast.literal_eval(value))
                except (ValueError, TypeError):
                    network.node_attribute(node, name, value)
        return True
    return False


def network_update_edge_attributes(network, edges, names=None):
    """Update the attributes of the edges of a network.

    Parameters
    ----------
    network : :class:`compas.datastructures.Network`
        A network object.
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
    names = names or network.default_edge_attributes.edges()
    names = sorted(names)
    edge = edges[0]
    values = network.edge_attributes(edge, names)
    if len(edges) > 1:
        for i, name in enumerate(names):
            for edge in edges[1:]:
                if values[i] != network.edge_attribute(edge, name):
                    values[i] = '-'
                    break
    values = map(str, values)
    values = _update_named_values(names, values)
    if values:
        for name, value in zip(names, values):
            if value == '-':
                continue
            for edge in edges:
                try:
                    value = ast.literal_eval(value)
                except (SyntaxError, ValueError, TypeError):
                    pass
                network.edge_attribute(edge, name, value)
        return True
    return False


def network_move_node(network, node, constraint=None, allow_off=False):
    """Move on node of the network.

    Parameters
    ----------
    network : :class:`compas.datastructures.Network`
        A network object.
    node : hashable
        The identifier of the node to move.
    constraint : Rhino.Geometry, optional
        A Rhino geometry object to constrain the movement to.
        By default the movement is unconstrained.
    allow_off : bool, optional (False)
        Allow the node to move off the constraint.

    """
    def OnDynamicDraw(sender, e):
        for ep in nbrs:
            sp = e.CurrentPoint
            e.Display.DrawDottedLine(sp, ep, color)

    color = Rhino.ApplicationSettings.AppearanceSettings.FeedbackColor
    nbrs = [network.node_coordinates(nbr) for nbr in network.node_neighbors(node)]
    nbrs = [Point3d(*xyz) for xyz in nbrs]

    gp = Rhino.Input.Custom.GetPoint()

    gp.SetCommandPrompt('Point to move to?')
    gp.DynamicDraw += OnDynamicDraw
    if constraint:
        gp.Constrain(constraint, allow_off)

    gp.Get()
    if gp.CommandResult() != Rhino.Commands.Result.Success:
        return False

    network.node_attributes(node, 'xyz', list(gp.Point()))
    return True


def mesh_update_attributes(mesh):
    """Update the attributes of a mesh.

    Parameters
    ----------
    mesh : :class:`compas.datastructures.Mesh`
        A mesh object.

    Returns
    -------
    bool
        ``True`` if the update was successful.
        ``False`` otherwise.

    """
    names = sorted(mesh.attributes.keys())
    values = [str(mesh.attributes[name]) for name in names]
    values = compas_rhino.update_named_values(names, values)
    if values:
        for name, value in zip(names, values):
            try:
                mesh.attributes[name] = ast.literal_eval(value)
            except (ValueError, TypeError):
                mesh.attributes[name] = value
        return True
    return False


def mesh_update_vertex_attributes(mesh, vertices, names=None):
    """Update the attributes of selected vertices of a given datastructure.

    Parameters
    ----------
    mesh : compas.datastructures.Datastructure
        The data structure.
    vertices : list
        The vertices of the vertices of which the attributes should be updated.
    names : list, optional
        The names of the attributes that should be updated.
        Default is to update all available attributes.

    Returns
    -------
    bool
        True if the attributes were successfully updated.
        False otherwise.

    """
    names = names or mesh.default_vertex_attributes.vertices()
    names = sorted(names)
    values = mesh.vertex_attributes(vertices[0], names)
    if len(vertices) > 1:
        for i, name in enumerate(names):
            for vertex in vertices[1:]:
                if values[i] != mesh.vertex_attribute(vertex, name):
                    values[i] = '-'
                    break
    values = map(str, values)
    values = _update_named_values(names, values)
    if values:
        for name, value in zip(names, values):
            if value == '-':
                continue
            for vertex in vertices:
                try:
                    mesh.vertex_attribute(vertex, name, ast.literal_eval(value))
                except (ValueError, TypeError):
                    mesh.vertex_attribute(vertex, name, value)
        return True
    return False


# rename to modify
def mesh_update_face_attributes(mesh, faces, names=None):
    """Update the attributes of the faces of a mesh.

    Parameters
    ----------
    mesh : :class:`compas.datastructures.Mesh`
    faces : list of int
    names : list, optional
        The names of the atrtibutes to update.
        Default is to update all attributes.

    Returns
    -------
    bool
        ``True`` if the update was successful.
        ``False`` otherwise.

    """
    names = names or mesh.default_face_attributes.faces()
    names = sorted(names)
    values = mesh.face_attributes(faces[0], names)
    if len(faces) > 1:
        for i, name in enumerate(names):
            for face in faces[1:]:
                if values[i] != mesh.face_attribute(face, name):
                    values[i] = '-'
                    break
    values = map(str, values)
    values = _update_named_values(names, values)
    if values:
        for name, value in zip(names, values):
            if value == '-':
                continue
            for face in faces:
                try:
                    mesh.face_attribute(face, name, ast.literal_eval(value))
                except (ValueError, TypeError):
                    mesh.face_attribute(face, name, value)
        return True
    return False


def mesh_update_edge_attributes(mesh, edges, names=None):
    """Update the attributes of the edges of a mesh.

    Parameters
    ----------
    mesh : :class:`compas.datastructures.Mesh`
        A mesh object.
    edges : list
        The edges to update.
    names : list, optional
        The names of the atrtibutes to update.
        Default is to update all attributes.

    Returns
    -------
    bool
        ``True`` if the update was successful.
        ``False`` otherwise.

    """
    names = names or mesh.default_edge_attributes.edges()
    names = sorted(names)
    edge = edges[0]
    values = mesh.edge_attributes(edge, names)
    if len(edges) > 1:
        for i, name in enumerate(names):
            for edge in edges[1:]:
                if values[i] != mesh.edge_attribute(edge, name):
                    values[i] = '-'
                    break
    values = map(str, values)
    values = _update_named_values(names, values)
    if values:
        for name, value in zip(names, values):
            if value == '-':
                continue
            for edge in edges:
                try:
                    value = ast.literal_eval(value)
                except (SyntaxError, ValueError, TypeError):
                    pass
                mesh.edge_attribute(edge, name, value)
        return True
    return False


# def mesh_move(mesh):
#     """"""
#     color = Rhino.ApplicationSettings.AppearanceSettings.FeedbackColor

#     vertex_xyz0 = {key: mesh.vertex_coordinates(key) for key in mesh.mesh.vertices()}
#     vertex_xyz = {key: mesh.vertex_coordinates(key) for key in mesh.mesh.vertices()}

#     edges = list(mesh.edges())

#     start = compas_rhino.pick_point('Point to move from?')
#     if not start:
#         return False

#     def OnDynamicDraw(sender, e):
#         current = list(e.CurrentPoint)
#         vector = subtract_vectors(current, start)
#         for vertex in vertex_xyz:
#             vertex_xyz[vertex] = add_vectors(vertex_xyz0[vertex], vector)
#         for u, v in iter(edges):
#             sp = vertex[u]
#             ep = vertex[v]
#             sp = Point3d(*sp)
#             ep = Point3d(*ep)
#             e.Display.DrawDottedLine(sp, ep, color)

#     gp = Rhino.Input.Custom.GetPoint()
#     gp.SetCommandPrompt('Point to move to?')
#     gp.DynamicDraw += OnDynamicDraw
#     gp.Get()

#     if gp.CommandResult() == Rhino.Commands.Result.Success:
#         end = list(gp.Point())
#         vector = subtract_vectors(end, start)
#         for vertex, attr in mesh.vertices(True):
#             attr['x'] += vector[0]
#             attr['y'] += vector[1]
#             attr['z'] += vector[2]
#         return True
#     return False


def mesh_move_vertex(mesh, vertex, constraint=None, allow_off=True):
    """Move on vertex of the mesh.

    Parameters
    ----------
    mesh : :class:`compas.datastructures.Mesh`
    vertex : int
    constraint : :class:`Rhino.Geometry`, optional
        A Rhino geometry object to constrain the movement to.
        By default the movement is unconstrained.
    allow_off : bool, optional (True)
        Allow the vertex to move off the constraint.

    """
    color = Rhino.ApplicationSettings.AppearanceSettings.FeedbackColor
    nbrs = [mesh.vertex_coordinates(nbr) for nbr in mesh.vertex_neighbors(vertex)]
    nbrs = [Point3d(*xyz) for xyz in nbrs]

    def OnDynamicDraw(sender, e):
        for ep in nbrs:
            sp = e.CurrentPoint
            e.Display.DrawDottedLine(sp, ep, color)

    gp = Rhino.Input.Custom.GetPoint()

    gp.SetCommandPrompt('Point to move to?')
    gp.DynamicDraw += OnDynamicDraw
    if constraint:
        gp.Constrain(constraint, allow_off)

    gp.Get()
    if gp.CommandResult() != Rhino.Commands.Result.Success:
        return False

    mesh.vertex_attributes(vertex, 'xyz', list(gp.Point()))
    return True


def mesh_move_vertices(mesh, vertices):
    """Move on vertices of the mesh.

    Parameters
    ----------
    mesh : compas.datastructures.Mesh
        A mesh object.
    keys : list
        The vertices to move.
    constraint : Rhino.Geometry (None)
        A Rhino geometry object to constrain the movement to.
        By default the movement is unconstrained.
    allow_off : bool (False)
        Allow the vertex to move off the constraint.

    """
    color = Rhino.ApplicationSettings.AppearanceSettings.FeedbackColor
    lines = []
    connectors = []

    for vertex in vertices:
        a = mesh.vertex_coordinates(vertex)
        nbrs = mesh.vertex_neighbors(vertex)
        for nbr in nbrs:
            b = mesh.vertex_coordinates(nbr)
            line = [Point3d(* a), Point3d(* b)]
            if nbr in vertices:
                lines.append(line)
            else:
                connectors.append(line)

    gp = Rhino.Input.Custom.GetPoint()

    gp.SetCommandPrompt('Point to move from?')
    gp.Get()
    if gp.CommandResult() != Rhino.Commands.Result.Success:
        return False

    start = gp.Point()

    def OnDynamicDraw(sender, e):
        end = e.CurrentPoint
        vector = end - start
        for a, b in lines:
            a = a + vector
            b = b + vector
            e.Display.DrawDottedLine(a, b, color)
        for a, b in connectors:
            a = a + vector
            e.Display.DrawDottedLine(a, b, color)

    gp.SetCommandPrompt('Point to move to?')
    gp.SetBasePoint(start, False)
    gp.DrawLineFromPoint(start, True)
    gp.DynamicDraw += OnDynamicDraw
    gp.Get()
    if gp.CommandResult() != Rhino.Commands.Result.Success:
        return False

    end = gp.Point()
    vector = list(end - start)

    for vertex in vertices:
        xyz = mesh.vertex_attributes(vertex, 'xyz')
        mesh.vertex_attributes(vertex, 'xyz', add_vectors(xyz, vector))
    return True


def mesh_move_face(mesh, face, constraint=None, allow_off=True):
    """Move a face of the mesh to a different location and update the data structure.

    Parameters
    ----------
    mesh : :class:`compas.datastructures.Mesh`
    face : int

    Returns
    -------
    bool
        ``True`` if the update was successful.
        ``False`` otherwise.

    """
    def OnDynamicDraw(sender, e):
        for ep in nbrs:
            sp = e.CurrentPoint
            e.Display.DrawDottedLine(sp, ep, color)

    color = Rhino.ApplicationSettings.AppearanceSettings.FeedbackColor
    nbrs = [mesh.face_coordinates(nbr) for nbr in mesh.face_neighbors(face)]
    nbrs = [Point3d(*xyz) for xyz in nbrs]

    gp = Rhino.Input.Custom.GetPoint()

    gp.SetCommandPrompt('Point to move to?')
    gp.DynamicDraw += OnDynamicDraw
    if constraint:
        gp.Constrain(constraint, allow_off)

    gp.Get()

    if gp.CommandResult() == Rhino.Commands.Result.Success:
        mesh.face_attributes(face, 'xyz', list(gp.Point()))
        return True

    return False


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
