from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas
import compas_rhino

if compas.IPY:
    import Rhino


__all__ = ['RhinoGeometry']


class RhinoGeometry(object):
    """Base class for Rhino geometry objects."""

    __module__ = 'compas_rhino.geometry'

    def __init__(self, guid):
        self._guid = None
        self._object = None
        self.guid = guid

    @property
    def guid(self):
        return self._guid

    @guid.setter
    def guid(self, guid):
        self._guid = guid
        self._object = compas_rhino.sc.doc.Objects.Find(guid)

    @property
    def object(self):
        return self._object

    @object.setter
    def object(self, obj):
        self._object = obj
        self._guid = obj.Id

    @property
    def geometry(self):
        return self.object.Geometry

    @property
    def attributes(self):
        return self.object.Attributes

    @property
    def type(self):
        return self.object.ObjectType

    @property
    def name(self):
        return self.object.Name

    @name.setter
    def name(self, value):
        self.attributes.Name = value
        self.object.CommitChanges()

    @staticmethod
    def from_guid(guid):
        """Create a ``RhinoGeometry`` instance of the correct type based on a given guid.

        Parameters
        ----------
        guid : str or System.Guid
            The *guid* of the Rhino object.

        Returns
        -------
        RhinoPoint
            If the type of the Rhino object is ``Rhino.DocObjects.ObjectType.Point``.
        RhinoCurve
            If the type of the Rhino object is ``Rhino.DocObjects.ObjectType.Curve``.
        RhinoMesh
            If the type of the Rhino object is ``Rhino.DocObjects.ObjectType.Mesh``.
        RhinoSurface
            If the type of the Rhino object is ``Rhino.DocObjects.ObjectType.Surface``.

        Examples
        --------
        >>>
        """
        from compas_rhino.geometry import RhinoPoint
        from compas_rhino.geometry import RhinoCurve
        from compas_rhino.geometry import RhinoMesh
        from compas_rhino.geometry import RhinoSurface

        obj = compas_rhino.find_object(guid)

        if obj.ObjectType == Rhino.DocObjects.ObjectType.Point:
            return RhinoPoint(guid)

        if obj.ObjectType == Rhino.DocObjects.ObjectType.Curve:
            return RhinoCurve(guid)

        if obj.ObjectType == Rhino.DocObjects.ObjectType.Mesh:
            return RhinoMesh(guid)

        if obj.ObjectType == Rhino.DocObjects.ObjectType.Surface:
            return RhinoSurface(guid)

        # if obj.ObjectType == Rhino.DocObjects.ObjectType.Brep:
        #     return RhinoBrep(guid)

        raise NotImplementedError

    @staticmethod
    def from_name(name):
        """Create a ``RhinoGeometry`` instance of the correct type based on a given object name.

        Parameters
        ----------
        name : str
            The name of the Rhino object.

        Returns
        -------
        RhinoPoint
            If the type of the Rhino object is ``Rhino.DocObjects.ObjectType.Point``.
        RhinoCurve
            If the type of the Rhino object is ``Rhino.DocObjects.ObjectType.Curve``.
        RhinoMesh
            If the type of the Rhino object is ``Rhino.DocObjects.ObjectType.Mesh``.
        RhinoSurface
            If the type of the Rhino object is ``Rhino.DocObjects.ObjectType.Surface``.

        Examples
        --------
        >>>
        """
        guids = compas_rhino.get_objects(name=name)
        if len(guids) > 1:
            raise NotImplementedError
        return RhinoGeometry.from_guid(guids[0])

    # def delete(self):
    #     """Delete the Rhino object.
    #     """
    #     compas_rhino.delete_object(self.guid)

    # def purge(self):
    #     """Purge the Rhino object."""
    #     compas_rhino.delete_object(self.guid, purge=True)

    # def hide(self):
    #     """Hide the Rhino object."""
    #     return rs.HideObject(self.guid)

    # def show(self):
    #     """Show the Rhino object."""
    #     return rs.ShowObject(self.guid)

    # def select(self):
    #     """Select the Rhino object."""
    #     return rs.SelectObject(self.guid)

    # def unselect(self):
    #     """Unselect the Rhino object."""
    #     return rs.UnselectObject(self.guid)

    def closest_point(self, *args, **kwargs):
        raise NotImplementedError

    def closest_points(self, *args, **kwargs):
        raise NotImplementedError


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
