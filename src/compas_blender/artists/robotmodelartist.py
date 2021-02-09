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
    layer : str, optional
        The name of the layer that will contain the robot meshes.
    """

    def __init__(self, model, collection=None, layer=None):
        self.view_layer = layer
        self.collection = collection
        super(RobotModelArtist, self).__init__(model)

    def transform(self, native_mesh, transformation):
        native_mesh.matrix_world @= mathutils.Matrix(transformation.matrix)

    def draw_geometry(self, geometry, name=None, color=None):
        # Imported colors take priority over a the parameter color

        if 'mesh_color.diffuse' in geometry.attributes:
            color = geometry.attributes['mesh_color.diffuse']

        # If we have a color, we'll discard alpha because draw_mesh is hard coded for a=1
        if color:
            r, g, b, _a = color
            color = [r, g, b]
        else:
            color = [1., 1., 1.]

        if self.collection:
            if self.collection not in bpy.data.collections.keys():
                compas_blender.utilities.create_collection(self.collection)

        v, f = geometry.to_vertices_and_faces()
        return compas_blender.draw_mesh(vertices=v, faces=f, name=name, color=color, centroid=False, collection=self.collection)

    def redraw(self, timeout=None):
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
