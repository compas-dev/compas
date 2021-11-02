from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import Rhino
import compas_rhino
from compas.geometry import Cylinder
from ..conversions import cylinder_to_rhino
from ..conversions import cylinder_to_compas
from ..conversions import ConversionError
from ._geometry import RhinoGeometry


class RhinoCylinder(RhinoGeometry):
    """Wrapper for Rhino cylinder objects.
    """

    @classmethod
    def from_object(cls, obj):
        """Construct a cylinder wrapper from an existing Rhino object.

        Parameters
        ----------
        obj : :class:`Rhino.DocObjects.ExtrusionObject`
            The Rhino object.

        Returns
        -------
        :class:`RhinoCylinder`
            The Rhino cylinder wrapper.

        Raises
        ------
        :class:`ConversionError`
            If the Rhino (brep) object cannot be converted to a cylinder.
        """
        wrapper = cls()
        wrapper.guid = obj.Id
        wrapper.object = obj
        geometry = obj.Geometry
        if not isinstance(geometry, Rhino.Geometry.Cylinder):
            if isinstance(geometry, Rhino.Geometry.Extrusion):
                geometry = geometry.ToBrep()
            if isinstance(geometry, Rhino.Geometry.Brep):
                if geometry.Faces.Count > 3:
                    raise ConversionError('Object brep cannot be converted to a cylinder.')
                faces = geometry.Faces
                geometry = None
                for face in faces:
                    if face.IsCylinder():
                        result, geometry = face.TryGetFiniteCylinder(0.001)
                    if result:
                        break
                if not geometry:
                    raise ConversionError('Object brep cannot be converted to a cylinder.')
            else:
                raise ConversionError('Rhino object cannot be converted to a cylinder: {}'.format(obj))
        wrapper.geometry = geometry
        return wrapper

    @classmethod
    def from_geometry(cls, geometry):
        """Construct a cylinder wrapper from an existing geometry object.

        Parameters
        ----------
        geometry : :class:`Rhino.Geometry.Cylinder` or :class:`compas.geometry.Cylinder`
            The geometry object defining a cylinder.

        Returns
        -------
        :class:`RhinoCylinder`
            The Rhino cylinder wrapper.

        Raises
        ------
        :class:`ConversionError`
            If the geometry cannot be converted to a cylinder.
        """
        if not isinstance(geometry, Rhino.Geometry.Cylinder):
            if isinstance(geometry, Rhino.Geometry.Brep):
                if geometry.Faces.Count > 3:
                    raise ConversionError('Object brep cannot be converted to a cylinder.')
                faces = geometry.Faces
                geometry = None
                for face in faces:
                    if face.IsCylinder():
                        result, geometry = face.TryGetFiniteCylinder(0.001)
                    if result:
                        break
                if not geometry:
                    raise ConversionError('Object brep cannot be converted to a cylinder.')
            elif isinstance(geometry, Cylinder):
                geometry = cylinder_to_rhino(geometry)
            else:
                raise ConversionError('Geometry object cannot be converted to a cylinder: {}'.format(geometry))
        cylinder = cls()
        cylinder.geometry = geometry
        return cylinder

    @classmethod
    def from_selection(cls):
        """Construct a cylinder wrapper by selecting an existing Rhino curve object.

        Returns
        -------
        :class:`RhinoCylinder`
            The Rhino cylinder wrapper.
        """
        guid = compas_rhino.select_object()
        return cls.from_guid(guid)

    def to_compas(self):
        """Convert to a COMPAS geometry object.

        Returns
        -------
        :class:`compas.geometry.Cylinder`
            A COMPAS cylinder.
        """
        return cylinder_to_compas(self.geometry)
