from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import Rhino
import compas_rhino
from compas.geometry import Sphere
from ..conversions import sphere_to_rhino
from ..conversions import sphere_to_compas
from ..conversions import ConversionError
from ._geometry import BaseRhinoGeometry


class RhinoSphere(BaseRhinoGeometry):
    """Wrapper for Rhino sphere objects.
    """

    def __init__(self):
        super(RhinoSphere, self).__init__()

    @classmethod
    def from_object(cls, obj):
        """Construct a sphere wrapper from an existing Rhino object.

        Parameters
        ----------
        obj : :class:`Rhino.DocObjects.ExtrusionObject`
            The Rhino object.

        Returns
        -------
        :class:`RhinoSphere`
            The Rhino sphere wrapper.
        """
        wrapper = cls()
        wrapper.guid = obj.Id
        wrapper.object = obj
        geometry = obj.Geometry
        if not isinstance(geometry, Rhino.Geometry.Sphere):
            if isinstance(geometry, Rhino.Geometry.Brep):
                if geometry.Faces.Count != 1:
                    raise ConversionError('Object brep cannot be converted to a sphere.')
                face = geometry.Faces.Item[0]
                if not face.IsSphere():
                    raise ConversionError('Object brep cannot be converted to a sphere.')
                result, geometry = face.TryGetSphere()
                if not result:
                    raise ConversionError('Object brep cannot be converted to a sphere.')
            else:
                raise ConversionError('Rhino object cannot be converted to a sphere: {}'.format(obj))
        wrapper.geometry = geometry
        return wrapper

    @classmethod
    def from_geometry(cls, geometry):
        """Construct a sphere wrapper from an existing geometry object.

        Parameters
        ----------
        geometry : :class:`Rhino.Geometry.Sphere` or :class:`compas.geometry.Sphere`
            The geometry object defining a sphere.

        Returns
        -------
        :class:`RhinoSphere`
            The Rhino sphere wrapper.
        """
        if not isinstance(geometry, Rhino.Geometry.Sphere):
            if isinstance(geometry, Rhino.Geometry.Brep):
                if geometry.Faces.Count != 1:
                    raise ConversionError('Object brep cannot be converted to a sphere.')
                face = geometry.Faces.Item[0]
                if not face.IsSphere():
                    raise ConversionError('Object brep cannot be converted to a sphere.')
                result, geometry = face.TryGetSphere()
                if not result:
                    raise ConversionError('Object brep cannot be converted to a sphere.')
            elif isinstance(geometry, Sphere):
                geometry = sphere_to_rhino(geometry)
            else:
                raise ConversionError('Geometry object cannot be converted to a sphere: {}'.format(geometry))
        sphere = cls()
        sphere.geometry = geometry
        return sphere

    @classmethod
    def from_selection(cls):
        """Construct a sphere wrapper by selecting an existing Rhino curve object.

        Returns
        -------
        :class:`RhinoSphere`
            The Rhino sphere wrapper.
        """
        guid = compas_rhino.select_object()
        return cls.from_guid(guid)

    def to_compas(self):
        """Convert to a COMPAS geometry object.

        Returns
        -------
        :class:`compas.geometry.Sphere`
            A COMPAS sphere.
        """
        return sphere_to_compas(self.geometry)
