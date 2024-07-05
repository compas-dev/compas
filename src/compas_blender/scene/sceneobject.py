from typing import Any
from typing import Optional
from typing import Union

import bpy  # type: ignore

import compas_blender
from compas.colors import Color
from compas.geometry import Transformation
from compas.scene import SceneObject
from compas_blender import conversions


class BlenderSceneObject(SceneObject):
    """Base class for all Blender scene objects.

    Parameters
    ----------
    collection : str | :blender:`bpy.types.Collection`, optional
        The Blender scene collection the object(s) created by the scene object belong to.
    show_wire : bool, optional
        Display the wireframe of the object.
    **kwargs : dict, optional
        Additional keyword arguments.

    Attributes
    ----------
    objects : list[:blender:`bpy.types.Object`]
        The Blender objects created by the scene object.
    collection : str | :blender:`bpy.types.Collection`
        The Blender scene collection the object(s) created by the scene object belong to.
    show_wire : bool
        Display the wireframe of the object.

    """

    def __init__(self, collection: Union[str, bpy.types.Collection] = None, show_wire: bool = True, **kwargs: Any):
        super().__init__(**kwargs)
        self.objects = []
        self.collection = collection
        self.show_wire = show_wire

    # many of the methods below will be added to a general scene object in the future
    # to make them universaly accessible they are added here for now

    # =============================================================================
    # Objects
    # =============================================================================

    def create_object(self, geometry: Union[bpy.types.Mesh, bpy.types.Curve], name: Optional[str] = None) -> bpy.types.Object:
        """Add an object to the Blender scene.

        Parameters
        ----------
        geometry : :blender:`bpy.types.Mesh` | :blender:`bpy.types.Curve`
            The Blender object data.
        name : str, optional
            The name of the object.

        Returns
        -------
        :blender:`bpy.types.Object`
            The Blender object.

        """
        obj = bpy.data.objects.new(name, geometry)
        self.objects.append(obj)
        return obj

    def update_object(
        self,
        obj: bpy.types.Object,
        name: Optional[str] = None,
        color: Optional[Color] = None,
        collection: Optional[str] = None,
        transformation: Optional[Transformation] = None,
        show_wire: Optional[bool] = False,
    ) -> None:
        """Update an object in the Blender scene.

        Parameters
        ----------
        obj : :blender:`bpy.types.Object`
            The Blender object data.
        name : str, optional
            The name of the object.
        color : :class:`compas.colors.Color`, optional
            The color specification.
        collection : str, optional
            The collection to which the object should be added.
        transformation : :class:`compas.geometry.Transformation`, optional
            The transformation to apply to the object.
        show_wire : bool, optional
            Show the wireframe of the object.

        Returns
        -------
        None

        """
        if show_wire:
            obj.show_wire = True

        if name:
            obj.name = name

        if color:
            self.set_object_color(obj, color)

        self.set_object_tranformation(obj, transformation)
        self.add_object_to_collection(obj, collection)

    def add_object_to_collection(self, obj: bpy.types.Object, name: Optional[str] = None, do_unlink: Optional[bool] = True) -> bpy.types.Collection:
        """Add an object to a collection.

        Parameters
        ----------
        obj : :blender:`bpy.types.Object`
            The Blender object.
        name : str, optional
            The name of the collection to which the object should be added.

        Returns
        -------
        :blender:`bpy.types.Collection`

        """
        if name:
            collection = self.create_collection(name)
        else:
            collection = bpy.context.scene.collection

        if do_unlink:
            for c in obj.users_collection:
                c.objects.unlink(obj)

        collection.objects.link(obj)
        return collection

    def set_object_color(self, obj: bpy.types.Object, color: Color) -> None:
        """Set the color of a Blender object.

        Parameters
        ----------
        obj : :class:`bpy.types.Object`
            The Blender object.
        color : rgb1 | rgb255 | :class:`compas.colors.Color`
            The color specification.

        Returns
        -------
        None

        """
        color = Color.coerce(color)  # type: ignore
        if not color:
            return

        material = conversions.color_to_blender_material(color)
        obj.color = color.rgba
        if obj.data.materials:
            obj.data.materials[0] = material
        else:
            obj.data.materials.append(material)
        obj.active_material = material

    def set_object_tranformation(self, obj: bpy.types.Object, transformation: Optional[Transformation] = None) -> None:
        """Set the transformation of a Blender object.

        Parameters
        ----------
        obj : :class:`bpy.types.Object`
            The Blender object.
        transformation : :class:`compas.geometry.Transformation`
            The transformation.

        Returns
        -------
        None

        """
        if transformation:
            obj.transformation = transformation

        obj.matrix_world = conversions.transformation_to_blender(self.worldtransformation)

    # =============================================================================
    # Collections
    # =============================================================================

    def create_collection(self, name: str) -> bpy.types.Collection:
        """Create a collection with the given name.

        Parameters
        ----------
        name : str
            The name of the collection.
        parent : bpy.types.Collection, optional
            A parent collection.

        Returns
        -------
        :blender:`bpy.types.Collection`

        """
        parts = name.split("::")
        parent = bpy.context.scene.collection
        collection = None
        for index, name in enumerate(parts):
            if index > 0:
                name = f"{parent.name}::{name}"
            if name not in bpy.data.collections:
                collection = bpy.data.collections.new(name)
                parent.children.link(collection)
            else:
                collection = bpy.data.collections[name]
            parent = collection
        return collection

    def clear_collection(self, name: str, include_children: Optional[bool] = True) -> None:
        """Clear the objects in a collection.

        Parameters
        ----------
        name : str
            The name of the collection to clear.
        include_children : bool, optional
            Clear the children collections as well.

        Returns
        -------
        None

        """
        if name not in bpy.data.collections:
            return
        compas_blender.clear_collection(name)
        if include_children:
            collection = bpy.data.collections.get(name)
            for child in collection.children:
                self.clear_collection(child.name)

    def delete_collection(self, name: str) -> None:
        """Delete a collection.

        Parameters
        ----------
        name : str
            The name of the collection to delete.

        Returns
        -------
        None

        """
        self.clear_collection(name)
        bpy.data.collections.remove(bpy.data.collections[name])
