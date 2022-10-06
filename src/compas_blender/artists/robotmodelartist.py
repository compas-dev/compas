from typing import Union
from typing import Tuple
from typing import Optional
from typing import Any
from typing import List

import bpy
import mathutils

import compas_blender
from compas_blender.utilities import RGBColor
from compas.datastructures import Mesh
from compas.geometry import Transformation
from compas.robots import RobotModel
from compas.artists import RobotModelArtist
from .artist import BlenderArtist


class RobotModelArtist(BlenderArtist, RobotModelArtist):
    """Artist for drawing robot models in Blender.

    Parameters
    ----------
    model : :class:`~compas.robots.RobotModel`
        Robot model.
    collection : str | :blender:`bpy.types.Collection`
        The Blender scene collection the object(s) created by this artist belong to.
    **kwargs : dict, optional
        Additional keyword arguments.
        For more info,
        see :class:`~compas_blender.artists.BlenderArtist` and :class:`~compas.artists.RobotModelArtist`.

    """

    def __init__(self, model: RobotModel, collection: Optional[Union[str, bpy.types.Collection]] = None, **kwargs: Any):
        super().__init__(model=model, collection=collection or model.name, **kwargs)

    # this method should not be here
    # it has nothing to do with the current object
    def transform(self, native_mesh: bpy.types.Object, transformation: Transformation) -> None:
        """Transform the mesh of a robot model.

        Parameters
        ----------
        native_mesh : bpy.types.Object
            A mesh scene object.
        transformation : :class:`~compas.geometry.Transformation`
            A transformation matrix.

        Returns
        -------
        None

        """
        native_mesh.matrix_world = mathutils.Matrix(transformation.matrix) @ native_mesh.matrix_world

    # again
    # doesn't make sense to me that there is no reference to self (except for the collection)
    # suggests that this method shouldn't be here
    def create_geometry(
        self,
        geometry: Mesh,
        name: str = None,
        color: Union[RGBColor, Tuple[int, int, int, int], Tuple[float, float, float, float]] = None,
    ) -> bpy.types.Object:
        """Create the scene objecy representing the robot geometry.

        Parameters
        ----------
        geometry : :class:`~compas.datastructures.Mesh`
            The geometry representing the robot.
        name : str, optional
            A name for the scene object.
        color : tuple[int, int, int] or tuple[float, float, float], optional
            The color of the object.

        Returns
        -------
        bpy.types.Object

        """
        # Imported colors take priority over a the parameter color
        if "mesh_color.diffuse" in geometry.attributes:
            color = geometry.attributes["mesh_color.diffuse"]

        # If we have a color, we'll discard alpha because draw_mesh is hard coded for a=1
        if color:
            color = color[:3]
        else:
            color = (1.0, 1.0, 1.0)

        v, f = geometry.to_vertices_and_faces(triangulated=False)

        native_mesh = compas_blender.draw_mesh(
            vertices=v,
            faces=f,
            name=name,
            color=color,
            centroid=False,
            collection=self.collection,
        )
        native_mesh.hide_set(True)
        return native_mesh

    def _ensure_geometry(self):
        if len(self.collection.objects) == 0:
            self.create()

    def draw(self) -> List[bpy.types.Object]:
        """Draw the robot model.

        Returns
        -------
        list[:blender:`bpy.types.Object`]

        """
        self._ensure_geometry()
        return self.draw_visual()

    def draw_visual(self) -> List[bpy.types.Object]:
        """Draw the robot model.

        Returns
        -------
        list[:blender:`bpy.types.Object`]

        """
        self._ensure_geometry()
        visuals = super(RobotModelArtist, self).draw_visual()
        for visual in visuals:
            visual.hide_set(False)
        return visuals

    def draw_collision(self) -> List[bpy.types.Object]:
        """Draw the collision mesh of the robot model.

        Returns
        -------
        list[:blender:`bpy.types.Object`]

        """
        self._ensure_geometry()
        collisions = super(RobotModelArtist, self).draw_collision()
        for collision in collisions:
            collision.hide_set(False)
        return collisions

    def draw_attached_meshes(self) -> List[bpy.types.Object]:
        """Draw the meshes attached to the robot model, if any.

        Returns
        -------
        list[:blender:`bpy.types.Object`]

        """
        self._ensure_geometry()
        meshes = super(RobotModelArtist, self).draw_attached_meshes()
        for mesh in meshes:
            mesh.hide_set(False)
        return meshes
