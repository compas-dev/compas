from typing import Union, Tuple

import bpy
import mathutils

import compas_blender
from compas.datastructures import Mesh
from compas.geometry import Transformation, Shape
from compas.robots import RobotModel
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

    def __init__(self,
                 model: RobotModel,
                 collection: bpy.types.Collection = None):
        self.collection = collection or model.name
        super(RobotModelArtist, self).__init__(model)

    @property
    def collection(self) -> bpy.types.Collection:
        return self._collection

    @collection.setter
    def collection(self, value: Union[str, bpy.types.Collection]):
        if isinstance(value, bpy.types.Collection):
            self._collection = value
        elif isinstance(value, str):
            self._collection = compas_blender.create_collection(value)
        else:
            raise Exception('Collection must be of type `str` or `bpy.types.Collection`.')

    def transform(self, native_mesh: bpy.types.Object, transformation: Transformation) -> None:
        native_mesh.matrix_world = mathutils.Matrix(transformation.matrix) @ native_mesh.matrix_world

    def create_geometry(self,
                        geometry: Union[Mesh, Shape],
                        name: str = None,
                        color: Union[Tuple[int, int, int, int], Tuple[float, float, float, float]] = None
                        ) -> bpy.types.Object:
        # Imported colors take priority over a the parameter color
        if 'mesh_color.diffuse' in geometry.attributes:
            color = geometry.attributes['mesh_color.diffuse']

        # If we have a color, we'll discard alpha because draw_mesh is hard coded for a=1
        if color:
            r, g, b, _a = color
            color = (r, g, b)
        else:
            color = (1., 1., 1.)

        v, f = geometry.to_vertices_and_faces()
        native_mesh = compas_blender.draw_mesh(
            vertices=v, faces=f, name=name, color=color, centroid=False, collection=self.collection
        )
        native_mesh.hide_set(True)
        return native_mesh

    def redraw(self, timeout: float = 0.0) -> None:
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1, time_limit=timeout)

    def clear(self) -> None:
        compas_blender.delete_objects(self.collection.objects)

    def draw_visual(self) -> None:
        visuals = super(RobotModelArtist, self).draw_visual()
        for visual in visuals:
            visual.hide_set(False)

    def draw_collision(self) -> None:
        collisions = super(RobotModelArtist, self).draw_collision()
        for collision in collisions:
            collision.hide_set(False)

    def draw_attached_meshes(self) -> None:
        meshes = super(RobotModelArtist, self).draw_attached_meshes()
        for mesh in meshes:
            mesh.hide_set(False)
