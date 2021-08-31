from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import Rhino
import compas_rhino
from compas.geometry import Cone
from ..conversions import cone_to_rhino
from ..conversions import cone_to_compas
from ..conversions import ConversionError
from ._geometry import BaseRhinoGeometry


class RhinoCone(BaseRhinoGeometry):
    """Wrapper for Rhino cone objects.
    """

    def __init__(self):
        super(RhinoCone, self).__init__()

    @classmethod
    def from_object(cls, obj):
        """Construct a cone wrapper from an existing Rhino object.

        Parameters
        ----------
        obj : :class:`Rhino.DocObjects.ExtrusionObject`
            The Rhino object.

        Returns
        -------
        :class:`RhinoCone`
            The Rhino cone wrapper.
        """
        wrapper = cls()
        wrapper.guid = obj.Id
        wrapper.object = obj
        geometry = obj.Geometry
        if not isinstance(geometry, Rhino.Geometry.Cone):
            if isinstance(geometry, Rhino.Geometry.Brep):
                if geometry.Faces.Count > 2:
                    raise ConversionError('Object brep cannot be converted to a cone.')
                faces = geometry.Faces
                geometry = None
                for face in faces:
                    if face.IsCone():
                        result, geometry = face.TryGetCone()
                    if result:
                        break
                if not geometry:
                    raise ConversionError('Object brep cannot be converted to a cone.')
            else:
                raise ConversionError('Rhino object cannot be converted to a cone: {}'.format(obj))
        wrapper.geometry = geometry
        return wrapper

    @classmethod
    def from_geometry(cls, geometry):
        """Construct a cone wrapper from an existing geometry object.

        Parameters
        ----------
        geometry : :class:`Rhino.Geometry.Cone` or :class:`compas.geometry.Cone`
            The geometry object defining a cone.

        Returns
        -------
        :class:`RhinoCone`
            The Rhino cone wrapper.
        """
        if not isinstance(geometry, Rhino.Geometry.Cone):
            if isinstance(geometry, Rhino.Geometry.Brep):
                if geometry.Faces.Count > 2:
                    raise ConversionError('Object brep cannot be converted to a cone.')
                faces = geometry.Faces
                geometry = None
                for face in faces:
                    if face.IsCone():
                        result, geometry = face.TryGetCone()
                    if result:
                        break
                if not geometry:
                    raise ConversionError('Object brep cannot be converted to a cone.')
            elif isinstance(geometry, Cone):
                geometry = cone_to_rhino(geometry)
            else:
                raise ConversionError('Geometry object cannot be converted to a cone: {}'.format(geometry))
        cone = cls()
        cone.geometry = geometry
        return cone

    @classmethod
    def from_selection(cls):
        """Construct a cone wrapper by selecting an existing Rhino curve object.

        Returns
        -------
        :class:`RhinoCone`
            The Rhino cone wrapper.
        """
        guid = compas_rhino.select_object()
        return cls.from_guid(guid)

    def to_compas(self):
        """Convert to a COMPAS geometry object.

        Returns
        -------
        :class:`compas.geometry.Cone`
            A COMPAS cone.
        """
        return cone_to_compas(self.geometry)
