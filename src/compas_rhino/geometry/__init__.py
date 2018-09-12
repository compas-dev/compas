"""
********************************************************************************
compas_rhino.geometry
********************************************************************************

.. currentmodule:: compas_rhino.geometry


Object-oriented convenience wrappers for native Rhino geometry.


.. autosummary::
    :toctree: generated/

    RhinoCurve
    RhinoMesh
    RhinoPoint
    RhinoSurface

"""
from __future__ import absolute_import

import compas
import compas_rhino

from compas_rhino.utilities import select_object

try:
    import rhinoscriptsyntax as rs
    import scriptcontext as sc

    find_object = sc.doc.Objects.Find

except ImportError:
    compas.raise_if_ironpython()


class RhinoGeometry(object):
    """Base class for Rhino geometry objects."""

    def __init__(self, guid):
        self.guid = guid
        self.object = RhinoGeometry.find(guid)
        self.geometry = self.object.Geometry
        self.attributes = self.object.Attributes
        self.otype = self.geometry.ObjectType

    @classmethod
    def from_selection(cls):
        """Create a ``RhinoGeometry`` instance of the correct type from a selected object.

        Returns
        -------
        RhinoPoint
            If the type of the Rhino object is ``rs.filter.point``.
        RhinoCurve
            If the type of the Rhino object is ``rs.filter.curve``.
        RhinoMesh
            If the type of the Rhino object is ``rs.filter.mesh``.
        RhinoSurface
            If the type of the Rhino object is ``rs.filter.surface``.

        Examples
        --------
        .. code-block:: python

            #

        """
        guid = select_object()
        return cls(guid)

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
            If the type of the Rhino object is ``rs.filter.point``.
        RhinoCurve
            If the type of the Rhino object is ``rs.filter.curve``.
        RhinoMesh
            If the type of the Rhino object is ``rs.filter.mesh``.
        RhinoSurface
            If the type of the Rhino object is ``rs.filter.surface``.

        Examples
        --------
        .. code-block:: python

            import compas
            import compas_rhino

            from compas.datastructures import Mesh
            from compas_rhino.geometry import RhinoGeometry

            mesh = Mesh.from_json(...)

            mesh.update_default_vertex_attributes(constraint=None)

            # interesting stuff happens here

            for key, attr in mesh.vertices(True):
                name = attr['constraint']

                if name:
                    constraint = RhinoGeometry.from_name(name)
                    xyz = constraint.closest_point(mesh.get_vertex_attributes(key, 'xyz'))
                    mesh.set_vertex_attributes(key, 'xyz', xyz)

            # more interesting stuff happens here

        """
        guids = compas_rhino.get_objects(name=name)
        if len(guids) > 1:
            raise NotImplementedError

        return RhinoGeometry.from_guid(guids[0])

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
            If the type of the Rhino object is ``rs.filter.point``.
        RhinoCurve
            If the type of the Rhino object is ``rs.filter.curve``.
        RhinoMesh
            If the type of the Rhino object is ``rs.filter.mesh``.
        RhinoSurface
            If the type of the Rhino object is ``rs.filter.surface``.

        Examples
        --------
        .. code-block:: python

            import compas
            import compas_rhino

            from compas.datastructures import Mesh
            from compas_rhino.geometry import RhinoGeometry

            mesh = Mesh.from_json(...)

            mesh.update_default_vertex_attributes(constraint=None)

            # interesting stuff happens here

            for key, attr in mesh.vertices(True):
                guid = attr['constraint']

                if guid:
                    constraint = RhinoGeometry.from_guid(guid)
                    xyz = constraint.closest_point(mesh.get_vertex_attributes(key, 'xyz'))
                    mesh.set_vertex_attributes(key, 'xyz', xyz)

            # more interesting stuff happens here

        """
        otype = rs.ObjectType(guid)

        if otype == rs.filter.point:
            return RhinoPoint(guid)

        if otype == rs.filter.curve:
            return RhinoCurve(guid)

        if otype == rs.filter.mesh:
            return RhinoMesh(guid)

        if otype == rs.filter.surface:
            return RhinoSurface(guid)

    @staticmethod
    def find(guid):
        """Find the Rhino object corresponding to a given guid.

        Parameters
        ----------
        guid : str or System.Guid
            The *guid* of the Rhino object.

        Returns
        -------
        Rhino.DocObjects.Object
            A Rhino object.

        Examples
        --------
        .. code-block:: python

            #

        """
        return find_object(guid)

    @property
    def name(self):
        """str : The name of the Rhino object."""
        value = self.object.Name
        return value

    @name.setter
    def name(self, value):
        self.attributes.Name = value
        self.object.CommitChanges()

    def delete(self):
        """Delete the Rhino object.
        """
        compas_rhino.delete_object(self.guid)

    def purge(self):
        """Purge the Rhino object."""
        compas_rhino.delete_object(self.guid, purge=True)

    def hide(self):
        """Hide the Rhino object."""
        return rs.HideObject(self.guid)

    def show(self):
        """Show the Rhino object."""
        return rs.ShowObject(self.guid)

    def select(self):
        """Select the Rhino object."""
        return rs.SelectObject(self.guid)

    def unselect(self):
        """Unselect the Rhino object."""
        return rs.UnselectObject(self.guid)

    def closest_point(self, *args, **kwargs):
        raise NotImplementedError

    def closest_points(self, *args, **kwargs):
        raise NotImplementedError


from .point import RhinoPoint
from .curve import RhinoCurve
from .mesh import RhinoMesh
from .surface import RhinoSurface


__all__ = ['RhinoGeometry', 'RhinoPoint', 'RhinoCurve', 'RhinoMesh', 'RhinoSurface']
