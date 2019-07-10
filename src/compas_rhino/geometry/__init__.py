"""
********************************************************************************
compas_rhino.geometry
********************************************************************************

.. currentmodule:: compas_rhino.geometry

Object-oriented convenience wrappers for Rhino geometry objects.

Base class
==========

.. autosummary::
    :toctree: generated/
    :nosignatures:

    RhinoGeometry

Specific wrappers
=================

.. autosummary::
    :toctree: generated/
    :nosignatures:

    RhinoPoint
    RhinoCurve
    RhinoMesh
    RhinoSurface

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import compas
import compas_rhino

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
        >>>

        """
        guid = compas_rhino.select_object()
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
        >>>

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
        >>>

        """
        from compas_rhino.geometry import RhinoPoint
        from compas_rhino.geometry import RhinoCurve
        from compas_rhino.geometry import RhinoMesh
        from compas_rhino.geometry import RhinoSurface

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
        >>>

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


from .point import *
from .curve import *
from .mesh import *
from .surface import *


__all__ = [name for name in dir() if not name.startswith('_')]
