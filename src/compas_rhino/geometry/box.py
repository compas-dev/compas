from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import Rhino
import compas_rhino
from compas.geometry import Box
from ..conversions import box_to_rhino
from ..conversions import box_to_compas
from ..conversions import ConversionError
from ._geometry import BaseRhinoGeometry


class RhinoBox(BaseRhinoGeometry):
    """Wrapper for Rhino box objects.
    """

    def __init__(self):
        super(RhinoBox, self).__init__()

    @classmethod
    def from_object(cls, obj):
        """Construct a box wrapper from an existing Rhino object.

        Parameters
        ----------
        obj : :class:`Rhino.DocObjects.ExtrusionObject`
            The Rhino object.

        Returns
        -------
        :class:`RhinoBox`
            The Rhino box wrapper.
        """
        wrapper = cls()
        wrapper.guid = obj.Id
        wrapper.object = obj
        geometry = obj.Geometry
        if not isinstance(geometry, Rhino.Geometry.Box):
            if isinstance(geometry, Rhino.Geometry.Extrusion):
                plane = geometry.GetPathPlane(0)
                box = geometry.GetBoundingBox(plane)
                geometry = Rhino.Geometry.Box(plane, box)
            else:
                raise ConversionError('Rhino object cannot be converted to a box: {}'.format(obj))
        wrapper.geometry = geometry
        return wrapper

    @classmethod
    def from_geometry(cls, geometry):
        """Construct a box wrapper from an existing geometry object.

        Parameters
        ----------
        geometry : :class:`Rhino.Geometry.Box` or :class:`compas.geometry.Box`
            The geometry object defining a box.

        Returns
        -------
        :class:`RhinoBox`
            The Rhino box wrapper.
        """
        if not isinstance(geometry, Rhino.Geometry.Box):
            if isinstance(geometry, Rhino.Geometry.Extrusion):
                plane = geometry.GetPathPlane(0)
                box = geometry.GetBoundingBox(plane)
                geometry = Rhino.Geometry.Box(plane, box)
            elif isinstance(geometry, Box):
                geometry = box_to_rhino(geometry)
            else:
                raise ConversionError('Geometry object cannot be converted to a box: {}'.format(geometry))
        box = cls()
        box.geometry = geometry
        return box

    @classmethod
    def from_selection(cls):
        """Construct a box wrapper by selecting an existing Rhino curve object.

        Returns
        -------
        :class:`RhinoBox`
            The Rhino box wrapper.
        """
        guid = compas_rhino.select_object()
        return cls.from_guid(guid)

    def to_compas(self):
        """Convert to a COMPAS geometry object.

        Returns
        -------
        :class:`compas.geometry.Box`
            A COMPAS box.
        """
        return box_to_compas(self.geometry)
