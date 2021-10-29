from typing import Union
from typing import Tuple
from typing import Optional
from typing import Any

import bpy
import mathutils

import compas_blender
from compas.datastructures import Mesh
from compas.geometry import Transformation, Shape
from compas.robots import RobotModel
from compas.artists import RobotModelArtist
from .artist import BlenderArtist


class RobotModelArtist(BlenderArtist, RobotModelArtist):
    """Visualizer for robot models inside a Blender environment.

    Parameters
    ----------
    model : :class:`compas.robots.RobotModel`
        Robot model.
    collection: str or :class:`bpy.types.Collection`
        The name of the collection the object belongs to.
    """

    def __init__(self,
                 model: RobotModel,
                 collection: Optional[Union[str, bpy.types.Collection]] = None,
                 **kwargs: Any):
        super().__init__(model=model, collection=collection or model.name, **kwargs)

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
        for obj in self.collection.objects:
            obj.hide_set(True)

    def draw(self) -> None:
        self.draw_visual()

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
