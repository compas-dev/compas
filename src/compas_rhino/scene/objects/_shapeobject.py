from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from functools import reduce

from collections import deque

import scriptcontext as sc
from Rhino.Geometry import Transform

from compas.geometry import Transformation

import compas_rhino
from compas_rhino.geometry.transformations import xform_from_transformation
from ._object import Object


class ShapeObject(Object):
    """Base class for working visualizing and interacting with COMPAS shapes in Rhino.

    Parameters
    ----------
    shape : :class:`compas.geometry.Shape`
        A COMPAS shape.
    scene : :class:`compas.scenes.Scene`, optional
        A scene object.
    name : str, optional
        The name of the object.
    visible : bool, optional
        Toggle for the visibility of the object.
    layer : str, optional
        The layer for drawing.
    color : rgb color tuple, optional
        A RGB color value.

    Attributes
    ----------
    shape : :class:`compas.geometry.Shape`
        The shape associated with the artist.
    matrix : :class:`Rhino.Geometry.Transform`
        The transformation matrix to apply to the current state of the object.
    guid : :class:`System.Guid`
        The globally unique identifier of the object in the Rhino Objects table.

    """

    def __init__(self, shape, scene=None, name=None, visible=True, layer=None, color=None):
        super(ShapeObject, self).__init__(shape, scene, name, visible, layer)
        self._guid = None
        self._stack = deque()
        self.artist.color = color

    @property
    def guid(self):
        return self._guid

    @property
    def shape(self):
        return self.item

    @shape.setter
    def shape(self, shape):
        self.item = shape
        self._guid = None

    def clear(self):
        """Clear all Rhino objects associated with this object.
        """
        if self._guid:
            compas_rhino.delete_object(self._guid, purge=True)
            self._guid = None

    def draw(self):
        """Draw the shape."""
        self.clear()
        if not self.visible:
            return
        self._guid = self.artist.draw()

    def transform(self, transformation):
        """Update the location of the object using the transformation matrix."""
        matrix = xform_from_transformation(transformation)
        obj = sc.doc.Objects.Find(self.guid)
        obj.Geometry.Transform(matrix)
        obj.CommitChanges()
        self._stack.appendleft(matrix)

    def synchronize(self):
        """Synchronize the geometry with the current location of the object."""
        T = reduce(Transform.Multiply, self._stack)
        M = Transformation()
        for i in range(4):
            for j in range(4):
                M[i, j] = T[i, j]
        self.shape.transform(M)
        self._stack = []
