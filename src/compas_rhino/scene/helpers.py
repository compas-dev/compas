from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import rhinoscriptsyntax as rs  # type: ignore
import scriptcontext as sc  # type: ignore

from compas_rhino.layers import create_layers_from_path

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


def ngon(v):
    if v < 3:
        return
    if v == 3:
        return [0, 1, 2]
    if v == 4:
        return [0, 1, 2, 3]
    return list(range(v))
