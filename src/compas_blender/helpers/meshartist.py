from compas.cad import ArtistInterface

from compas.utilities import to_valuedict

from compas_blender.utilities import clear_layer
from compas_blender.utilities import delete_objects
from compas_blender.utilities import xdraw_cubes
from compas_blender.utilities import xdraw_faces
from compas_blender.utilities import xdraw_labels
from compas_blender.utilities import xdraw_lines

import time

try:
    import bpy
except ImportError:
    pass


__author__     = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2017, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'liew@arch.ethz.ch'


__all__ = ['MeshArtist']


class MeshArtist(ArtistInterface):
    """"""

    def __init__(self, mesh, layer=None):
        self.mesh = mesh
        self.layer = layer
        self.defaults = {
            'vertex.color': (1, 0, 0),
            'face.color': (1, 1, 1),
            'edge.color': (0, 0, 1)}

    def redraw(self, timeout=None):
        if timeout:
            time.sleep(timeout)
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)

    def clear_layer(self):
        if self.layer:
            clear_layer(layer=self.layer)

    def clear(self):
        self.clear_vertices()
        self.clear_faces()
        self.clear_edges()

    def clear_vertices(self, keys=None):
        if not keys:
            keys = list(self.mesh.vertices())
        objects = []
        for key in keys:
            name = self.mesh.vertex_name(key)
            object = get_objects(name=name)[0]
            if object:
                objects.append(object)
            name = 'V{0}'.format(key)
            object = get_objects(name=name)[0]
            if object:
                objects.append(object)
        delete_objects(objects=objects)

    def clear_faces(self, keys=None):
        if not keys:
            keys = list(self.mesh.faces())
        objects = []
        for key in keys:
            name = self.mesh.face_name(key)
            object = get_objects(name=name)[0]
            if object:
                objects.append(object)
            name = 'F{0}'.format(key)
            object = get_objects(name=name)[0]
            if object:
                objects.append(object)
        delete_objects(objects=objects)

    def clear_edges(self, keys=None):
        if not keys:
            keys = list(self.mesh.edges())
        objects = []
        for u, v in keys:
            name = self.mesh.edge_name(u, v)
            object = get_objects(name=name)[0]
            if object:
                objects.append(object)
            name = 'E{0}-{1}'.format(u, v)
            object = get_objects(name=name)[0]
            if object:
                objects.append(object)
        delete_objects(objects=objects)

    def draw_vertices(self, radius=0.010, keys=None, color=None):
        keys = keys or list(self.mesh.vertices())
        colordict = to_valuedict(keys, color, self.defaults['vertex.color'])
        points = []
        for key in keys:
            points.append({
                'pos': self.mesh.vertex_coordinates(key),
                'name': self.mesh.vertex_name(key),
                'color': colordict[key],
                'layer': self.layer,
                'radius': radius
            })
        return xdraw_cubes(points)

    def draw_faces(self, fkeys=None, color=None, alpha=1):
        fkeys = fkeys or list(self.mesh.faces())
        colordict = to_valuedict(fkeys, color, self.defaults['face.color'])
        faces = []
        for fkey in fkeys:
            faces.append({
                'name': "{}.face.{}".format(self.mesh.attributes['name'], fkey),
                'points': self.mesh.face_coordinates(fkey),
                'color': colordict[fkey],
                'layer': self.layer
            })
        return xdraw_faces(faces, alpha=alpha)

    def draw_edges(self, width=0.010, keys=None, color=None):
        keys = keys or list(self.mesh.edges())
        colordict = to_valuedict(keys, color, self.defaults['edge.color'])
        lines = []
        for u, v in keys:
            lines.append({
                'start': self.mesh.vertex_coordinates(u),
                'end': self.mesh.vertex_coordinates(v),
                'color': colordict[(u, v)],
                'name': self.mesh.edge_name(u, v),
                'width': width,
                'layer': self.layer
            })
        return xdraw_lines(lines)

    def draw_vertexlabels(self, text=None, ds=0.0):
        if text is None:
            textdict = {key: 'V{0}'.format(key) for key in self.mesh.vertices()}
        elif isinstance(text, dict):
            textdict = text
        else:
            raise NotImplementedError
        vlabels = []
        for key, text in iter(textdict.items()):
            xyz = self.mesh.vertex_coordinates(key)
            vlabels.append({
                'pos': [i + ds for i in xyz],
                'name': textdict[key],
                'layer': self.layer
            })
        return xdraw_labels(vlabels)

    def draw_facelabels(self, text=None, ds=0.0):
        if text is None:
            textdict = {key: 'F{0}'.format(key) for key in self.mesh.faces()}
        elif isinstance(text, dict):
            textdict = text
        else:
            raise NotImplementedError
        flabels = []
        for key, text in iter(textdict.items()):
            xyz = self.mesh.face_center(key)
            flabels.append({
                'pos': [i + ds for i in xyz],
                'name': textdict[key],
                'layer': self.layer
            })
        return xdraw_labels(flabels)

    def draw_edgelabels(self, text=None, ds=0.0):
        if text is None:
            textdict = {(u, v): 'E{}-{}'.format(u, v) for u, v in self.mesh.edges()}
        elif isinstance(text, dict):
            textdict = text
        else:
            raise NotImplementedError
        elabels = []
        for (u, v), text in iter(textdict.items()):
            xyz = self.mesh.edge_midpoint(u, v)
            elabels.append({
                'pos': [i + ds for i in xyz],
                'name': textdict[(u, v)],
                'layer': self.layer
            })
        return xdraw_labels(elabels)


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":

    from compas_blender.utilities import delete_all_materials
    from compas_blender.utilities import get_objects
    from compas_blender.helpers import mesh_from_bmesh

    delete_all_materials()

    bmesh = get_objects(layer=0)[0]
    mesh = mesh_from_bmesh(bmesh=bmesh)
    meshartist = MeshArtist(mesh=mesh, layer=1)

    meshartist.redraw()
    meshartist.clear_layer()

    meshartist.draw_vertices(radius=0.010)
    meshartist.draw_vertexlabels()
    meshartist.clear_vertices(keys=[6])

    #meshartist.draw_faces(alpha=0.5)
    #meshartist.draw_facelabels()
    #meshartist.clear_faces(keys=[2])

    meshartist.draw_edges(width=0.005)
    meshartist.draw_edgelabels()
    meshartist.clear_edges(keys=[(7, 6)])
