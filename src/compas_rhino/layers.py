from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from collections import deque

import rhinoscriptsyntax as rs  # type: ignore
import scriptcontext as sc  # type: ignore

find_object = sc.doc.Objects.Find

try:
    purge_object = sc.doc.Objects.Purge
except AttributeError:
    purge_object = None


# ==============================================================================
# helpers
# ==============================================================================


def show_hidden_objects_on_layer(name):
    rs.ShowObjects([guid for guid in rs.HiddenObjects() if rs.ObjectLayer(guid) == name])


def find_objects_on_layer(name, include_hidden=True, include_children=True):
    if include_hidden:
        show_hidden_objects_on_layer(name)
    to_delete = rs.ObjectsByLayer(name)
    if include_children:
        to_visit = deque(rs.LayerChildren(name))
        while to_visit:
            name = to_visit.popleft()
            if include_hidden:
                show_hidden_objects_on_layer(name)
            to_delete += rs.ObjectsByLayer(name)
            if rs.LayerChildCount(name):
                to_visit.extend(rs.LayerChildren(name))
    return to_delete


def delete_objects_on_layer(name, include_hidden=True, include_children=False, purge=True):
    guids = find_objects_on_layer(name, include_hidden, include_children)
    if purge and purge_object:
        rs.EnableRedraw(False)
        for guid in guids:
            obj = find_object(guid)
            if not obj:
                continue
            purge_object(obj.RuntimeSerialNumber)
        rs.EnableRedraw(True)
    else:
        rs.DeleteObjects(guids)


# ==============================================================================
# create
# ==============================================================================


def create_layers_from_path(path, separator="::"):
    """Create a nested layer structure from a hierarchical path string.

    Parameters
    ----------
    path : str
        The path string.
    separator : str, optional
        Separator between components of the layer path.

    Returns
    -------
    None

    Examples
    --------
    The following snippet will created 3 nested layers,
    with "COMPAS" at the root level, "Datastructures" at the first nested level, and "Mesh" at the deepest level.

    * COMPAS
      * Datastructures
        * Mesh

    .. code-block:: python

        create_layers_from_path("COMPAS::Datastructures::Mesh")

    """
    names = path.split(separator)
    parent = None
    for name in names:
        if parent:
            name = parent + separator + name
        if not rs.IsLayer(name):
            rs.AddLayer(name)
        parent = name


def create_layers_from_paths(names, separator="::"):
    """Create nested layers from a lst of hierarchical path strings.

    Parameters
    ----------
    names : list[str]
        The path strings of the nested layer structures.
    separator : str, optional
        Separator between components of the layer path.

    Returns
    -------
    None

    Examples
    --------
    The following snippet will created 2 nested layer structures:

    * COMPAS
      * Datastructures
        * Mesh
        * Graph
      * Geometry
        * Point
        * Vector

    .. code-block:: python

        create_layers_from_paths(
            [
                "COMPAS::Datastructures::Mesh",
                "COMPAS::Datastructures::Graph",
                "COMPAS::Geometry::Point",
                "COMPAS::Geometry::Vector",
            ]
        )

    """
    for name in names:
        create_layers_from_path(name, separator=separator)


def create_layers_from_dict(layers):
    """Create Rhino layers from a dictionary.

    Parameters
    ----------
    layers : dict[str, dict]
        A dictionary of nested layer definitions.
        The keys of the dict are the layer names.
        The corresponding values define optional layer properties and nested layers.

    Returns
    -------
    None

    Examples
    --------
    .. code-block:: python

        layers = {
            "COMPAS",
            {
                "layers": {
                    "Datastructures": {"color": (255, 0, 0), "layers": {"Mesh": {}, "Graph": {}}},
                    "Geometry": {"color": (0, 0, 255), "layers": {"Point": {}, "Vector": {}}},
                }
            },
        }

        create_layers_from_dict(layers)

    """

    def recurse(layers, parent=None):
        for name in layers:
            if not name:
                continue
            fullname = name
            if parent:
                fullname = parent + "::" + name
            try:
                attr = layers[name]
            except TypeError:
                attr = {}
            attr = attr or {}
            color = attr.get("color", (0, 0, 0))
            visible = attr.get("visible", True)
            locked = attr.get("locked", False)
            if not rs.IsLayer(fullname):
                rs.AddLayer(fullname, color, visible, locked)
            if "layers" in attr:
                recurse(attr["layers"], fullname)

    rs.EnableRedraw(False)
    recurse(layers)
    rs.EnableRedraw(True)


create_layers = create_layers_from_dict


# ==============================================================================
# clear
# ==============================================================================


def clear_layer(name, include_hidden=True, include_children=True, purge=True):
    """Delete all objects of a layer.

    Parameters
    ----------
    name : str
        The full, hierarchical name of the layer.
    include_hidden : bool, optional
        If True, include all hidden objects.
    include_children : bool, optional
        If True, include the objects of child layers.
    purge : bool, optional
        If True, purge history after deleting.

    Returns
    -------
    None

    """
    if not rs.IsLayer(name):
        return
    guids = find_objects_on_layer(name, include_hidden, include_children)
    rs.EnableRedraw(False)
    if purge and purge_object:
        for guid in guids:
            obj = find_object(guid)
            if not obj:
                continue
            purge_object(obj.RuntimeSerialNumber)
    else:
        rs.DeleteObjects(guids)
    rs.EnableRedraw(True)


def clear_current_layer():
    """Delete all objects from the current layer.

    Returns
    -------
    None

    """
    layer = rs.CurrentLayer()
    clear_layer(layer)


def clear_layers(layers, include_children=True, include_hidden=True, purge=True):
    """Delete the objects of the specified layers.

    Parameters
    ----------
    layers : list[str]
        A list of layer names as fully qualified hierarchical paths.
    include_hidden : bool, optional
        If True, include all hidden objects.
    include_children : bool, optional
        If True, include the objects of child layers.
    purge : bool, optional
        If True, purge history after deleting.

    Returns
    -------
    None

    """
    rs.EnableRedraw(False)
    to_delete = []
    for name in layers:
        if rs.IsLayer(name):
            to_delete += find_objects_on_layer(name, include_hidden, include_children)
    if purge and purge_object:
        for guid in to_delete:
            obj = find_object(guid)
            if not obj:
                continue
            purge_object(obj.RuntimeSerialNumber)
    else:
        rs.DeleteObjects(to_delete)
    rs.EnableRedraw(True)


# ==============================================================================
# delete
# ==============================================================================


def delete_layers(layers):
    """Delete layers and all contained objects.

    Parameters
    ----------
    layers : dict or list[str]
        When given as a list the list elements should be name of layers given
        with ``"::"`` as a separator between hierarchies.
        When provided as a dictionary, keys represent layer names, and values are dictionaries defining optional nested layers.

    Returns
    -------
    None

    Examples
    --------
    .. code-block:: python

        layers = {"COMPAS": {"layers": {"Datastructures": {"layers": {"Mesh": {}, "Graph": {}}}}}}

        create_layers(layers)

        delete_layers(["COMPAS::Datastructures::Graph"])
        delete_layers({"COMPAS": {"layers": {"Datastructures": {"layers": {"Mesh": {}}}}}})

    """
    to_delete = []

    def recurse(layers, parent=None):
        for name in layers:
            if not name:
                continue
            fullname = name
            if parent:
                fullname = parent + "::" + name
            try:
                attr = layers[name]
            except TypeError:
                attr = {}
            if "layers" in attr:
                recurse(attr["layers"], fullname)
            to_delete.append(fullname)

    rs.EnableRedraw(False)
    recurse(layers)

    for layer in to_delete:
        if rs.IsLayer(layer):
            if rs.IsLayerCurrent(layer):
                print("Can't delete {} as it is the current layer".format(layer))
                continue

            rs.PurgeLayer(layer)

    rs.EnableRedraw(True)
