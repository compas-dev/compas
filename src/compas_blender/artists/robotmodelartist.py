import bpy
import mathutils

import compas_blender
from compas.robots.base_artist import BaseRobotModelArtist

__all__ = [
    'RobotModelArtist',
]


class RobotModelArtist(BaseRobotModelArtist):
    """Visualizer for robot models inside a Blender environment.

    Parameters
    ----------
    model : :class:`compas.robots.RobotModel`
        Robot model.
    """

    def __init__(self, model, collection=None):
        self.collection = collection
        super(RobotModelArtist, self).__init__(model)

    def transform(self, native_mesh, transformation):
        native_mesh.matrix_world = mathutils.Matrix(transformation.matrix) @ native_mesh.matrix_world

    def create_geometry(self, geometry, name=None, color=None):
        # Imported colors take priority over a the parameter color
        if 'mesh_color.diffuse' in geometry.attributes:
            color = geometry.attributes['mesh_color.diffuse']

        # If we have a color, we'll discard alpha because draw_mesh is hard coded for a=1
        if color:
            r, g, b, _a = color
            color = (r, g, b)
        else:
            color = (1., 1., 1.)

        if self.collection and self.collection not in bpy.data.collections.keys():
            compas_blender.utilities.create_collection(self.collection)

        v, f = geometry.to_vertices_and_faces()
        native_mesh = compas_blender.draw_mesh(vertices=v, faces=f, name=name, color=color, centroid=False, collection=self.collection)
        native_mesh.hide_set(True)
        return native_mesh

    def redraw(self, timeout=0.0):
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1, time_limit=timeout)

    def draw_visual(self):
        visuals = super(RobotModelArtist, self).draw_visual()
        for visual in visuals:
            visual.hide_set(False)

    def draw_collision(self):
        collisions = super(RobotModelArtist, self).draw_collision()
        for collision in collisions:
            collision.hide_set(False)

    def draw_attached_meshes(self):
        meshes = super(RobotModelArtist, self).draw_attached_meshes()
        for mesh in meshes:
            mesh.hide_set(False)
