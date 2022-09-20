import bpy
from compas.geometry import Point


class BlenderGeometry:
    """Base class for Blender Geometry and Object wrappers.

    Blender scene objects have an underlying data block that represents the actual geometry of the object.
    Multiple objects can share the same data block.

    Every object adds a "location", "rotation", and "scale" to the data block to place it in the scene.
    To change an individual object without changing the underlying data block, change its location, rotation or scale.
    Change a data block directly to change all the connected objects.
    """

    def __init__(self):
        self._object = None
        self._geometry = None

    @property
    def object(self):
        """:blender:`bpy.types.Object` - The Blender scene object."""
        return self._object

    @object.setter
    def object(self, obj):
        raise NotImplementedError

    @property
    def geometry(self):
        """The data block."""
        return self._geometry

    @geometry.setter
    def geometry(self, data):
        raise NotImplementedError

    @property
    def type(self):
        """:obj:`str` - The type of Blender object."""
        if self.object:
            return self.object.type

    @property
    def name(self):
        """:obj:`str` - The name of the Blender object."""
        if self.object:
            return self.object.name

    @name.setter
    def name(self, value):
        if self.object:
            self.object.name = value

    @property
    def location(self):
        """:class:`~compas.geometry.Point` - The location of the Blender object."""
        return Point(*self.object.location)

    @location.setter
    def location(self, location):
        self.object.location = list(location)

    @classmethod
    def from_object(cls, obj):
        """Construct a Blender object wrapper from an existing Blender object.

        Parameters
        ----------
        obj : :blender:`bpy.types.Object`
            The Blender object.

        Returns
        -------
        :class:`~compas_blender.conversions.BlenderGeometry`
            The Blender object wrapper.

        Raises
        ------
        :class:`ConversionError`
            If the geometry of the Blender scene object cannot be converted to the geometry type of the wrapper.
        """
        wrapper = cls()
        wrapper.object = obj
        return wrapper

    @classmethod
    def from_geometry(cls, geometry):
        """Construct a Blender object wrapper from an existing Blender data block.

        Parameters
        ----------
        geometry : Blender data block
            The Blender data block.

        Returns
        -------
        :class:`~compas_blender.conversions.BlenderGeometry`
            The Blender object wrapper.

        Raises
        ------
        :class:`ConversionError`
            If the geometry of the Blender data block cannot be converted to the geometry type of the wrapper.
        """
        wrapper = cls()
        wrapper.geometry = geometry
        return wrapper

    @classmethod
    def from_name(cls, name):
        """Construct a Blender object wrapper from an existing Blender object.

        Parameters
        ----------
        name : :obj:`str`
            The name of the Blender scene object.

        Returns
        -------
        :class:`~compas_blender.conversions.BlenderGeometry`
            The Blender object wrapper.

        Raises
        ------
        :class:`ConversionError`
            If the geometry of the Blender data block cannot be converted to the geometry type of the wrapper.
        """
        wrapper = cls()
        wrapper.object = bpy.data.objects[name]
        return wrapper

    def to_compas(self):
        raise NotImplementedError

    def transform(self, T):
        """Transform the Blender object.

        Parameters
        ----------
        T : :class:`~compas.geometry.Transformation`
            The transformation matrix.

        Returns
        -------
        None
            The Blender object is transformed in place.
        """
        raise NotImplementedError
