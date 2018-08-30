from __future__ import print_function

from collections import deque

import compas

try:
    import rhinoscriptsyntax as rs
    import scriptcontext as sc

    find_object = sc.doc.Objects.Find

except ImportError:
    compas.raise_if_ironpython()

else:
    try:
        purge_object = sc.doc.Objects.Purge
    except AttributeError:
        purge_object = None


__all__ = [
    'create_layers_from_path',
    'create_layers_from_paths',
    'create_layers_from_dict',
    'create_layers',
    'clear_layer',
    'clear_current_layer',
    'clear_layers',
    'delete_layers',
]


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


def create_layers_from_path(path, separator='::'):
    names = path.split(separator)
    parent = None
    for name in names:
        if parent:
            name = parent + separator + name
        if not rs.IsLayer(name):
            rs.AddLayer(name)
        parent = name


def create_layers_from_paths(names, separator='::'):
    for name in names:
        create_layers_from_path(name, separator=separator)


def create_layers_from_dict(layers):
    def recurse(layers, parent=None):
        for name in layers:
            if not name:
                continue
            fullname = name
            if parent:
                fullname = parent + '::' + name
            try:
                attr = layers[name]
            except TypeError:
                attr = {}
            attr = attr or {}
            color   = attr.get('color', (0, 0, 0))
            visible = attr.get('visible', True)
            locked  = attr.get('locked', False)
            if not rs.IsLayer(fullname):
                rs.AddLayer(fullname, color, visible, locked)
            if 'layers' in attr :
                recurse(attr['layers'], fullname)
    rs.EnableRedraw(False)
    recurse(layers)
    rs.EnableRedraw(True)


create_layers = create_layers_from_dict


# ==============================================================================
# clear
# ==============================================================================


def clear_layer(name, include_hidden=True, include_children=True, purge=True):
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
    layer = rs.CurrentLayer()
    clear_layer(layer)


def clear_layers(layers, include_children=True, include_hidden=True):
    rs.EnableRedraw(False)
    to_delete = []
    for name in layers:
        to_delete += find_objects_on_layer(name, include_hidden, include_children)
    for guid in to_delete:
        obj = find_object(guid)
        if not obj:
            continue
        if purge_object:
            purge_object(obj.RuntimeSerialNumber)
    rs.EnableRedraw(True)


# ==============================================================================
# delete
# ==============================================================================


def delete_layers(layers):
    to_delete = []
    def recurse(layers, parent=None):
        for name in layers:
            if not name:
                continue
            fullname = name
            if parent:
                fullname = parent + '::' + name
            try:
                attr = layers[name]
            except TypeError:
                attr = {}
            if 'layers' in attr:
                recurse(attr['layers'], fullname)
            to_delete.append(fullname)
    rs.EnableRedraw(False)
    recurse(layers)
    for layer in to_delete:
        if rs.IsLayer(layer):
            rs.DeleteLayer(layer)
    rs.EnableRedraw(True)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    layers = {
        '1': {'layers': {
            '1.1': {},
            '1.2': {},
            '1.3': {'layers': {
                '1.3.1': {},
            }},
        }},
        '2': {'layers': {
            '2.1': {},
        }},
    }

    layers = ['1::1.1', '1::1.2', '1::1.3::1.3.1', '2::2.1']

    create_layers_from_paths(layers)
