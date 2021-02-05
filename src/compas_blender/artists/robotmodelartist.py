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

    def __init__(self, model, layer=None):
        self.layer = layer
        super(RobotModelArtist, self).__init__(model)

    def transform(self, native_mesh, transformation):
        native_mesh.matrix_world @= mathutils.Matrix(transformation.matrix)

    def draw_geometry(self, geometry, name=None, color=None):
        # Imported colors take priority over a the parameter color
        # TODO: cleanup confusion between layers and collections

        if 'mesh_color.diffuse' in geometry.attributes:
            color = geometry.attributes['mesh_color.diffuse']

        # If we have a color, we'll discard alpha because draw_mesh is hard coded for a=1
        if color:
            r, g, b, _a = color
            color = [r, g, b]
        else:
            color = [1., 1., 1.]

        if self.layer:
            
            current_collections = bpy.data.collections.items()
            #print(bpy.data.collections)
            #print(bpy.data.collections.keys())

            if self.layer not in bpy.data.collections.keys():
                collection = bpy.data.collections.new(self.layer)  # create new collection if none exists
                bpy.context.scene.collection.children.link(collection)  # link the new collection to the base collection
            else: 
                collection = bpy.data.collections.get(self.layer)
               # print(collection)
            

        v, f = geometry.to_vertices_and_faces()
        # Draw the mesh in blender in the specified collection
        return compas_blender.draw_mesh(vertices=v, faces=f, name=name, color=color, centroid=False, collection=self.layer)

    def redraw(self, timeout=None):
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
