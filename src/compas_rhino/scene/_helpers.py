from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from System.Drawing.Color import FromArgb  # type: ignore
from Rhino.DocObjects.ObjectColorSource import ColorFromObject  # type: ignore
from Rhino.DocObjects import ObjectAttributes  # type: ignore
from Rhino.DocObjects.ObjectDecoration import EndArrowhead  # type: ignore
from Rhino.DocObjects.ObjectDecoration import StartArrowhead  # type: ignore

import rhinoscriptsyntax as rs  # type: ignore
import scriptcontext as sc  # type: ignore

from compas_rhino import create_layers_from_path

try:
    find_layer_by_fullpath = sc.doc.Layers.FindByFullPath
except SystemError:
    find_layer_by_fullpath = None


def ensure_layer(layerpath):
    if not rs.IsLayer(layerpath):
        create_layers_from_path(layerpath)
    if find_layer_by_fullpath:
        index = find_layer_by_fullpath(layerpath, True)
    else:
        index = 0
    return index


def attributes(name=None, color=None, layer=None, arrow=None):
    attributes = ObjectAttributes()
    if name:
        attributes.Name = name
    if color:
        attributes.ObjectColor = FromArgb(*color.rgb255)
        attributes.ColorSource = ColorFromObject
    if layer:
        attributes.LayerIndex = ensure_layer(layer)
    if arrow == "end":
        attributes.ObjectDecoration = EndArrowhead
    elif arrow == "start":
        attributes.ObjectDecoration = StartArrowhead
    return attributes


def ngon(v):
    if v < 3:
        return
    if v == 3:
        return [0, 1, 2, 2]
    if v == 4:
        return [0, 1, 2, 3]
    return list(range(v))
