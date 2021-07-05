**************
Data
**************

.. rst-class:: lead

    The data package provides a base class (:class:`compas.data.Data`) for all data objects in the COMPAS framework (see :ref:`Inheritance Diagrams`),
    the mechanism for serialisation of data to JSON format,
    and the base infrastructure for validation of the data of COMPAS objects in both the original Python and serialised JSON formats.

::

    >>> from compas.data import Data
    >>> from compas.geometry import Point, Box, Rotation
    >>> from compas.datastructures import Mesh
    >>> from compas.robots import RobotModel

::

    >>> issubclass(Point, Data)
    True
    >>> issubclass(Box, Data)
    True
    >>> issubclass(Rotation, Data)
    True
    >>> issubclass(Mesh, Data)
    True
    >>> issubclass(RobotModel, Data)
    True


.. note::

    This tutorial is loosely based on the COMPAS exchange meeting about `compas.data` that is available here
    `COMPAS exchange: data <https://github.com/compas-dev/compas-exchange>`_

Interface
=========

The base data class defines a common data interface for all objects.
Among other things, this interface provides a read-only GUID (:attr:`compas.data.Data.guid`),
a modifiable object name (:attr:`compas.data.Data.name`) that defaults to the class name,
a read-only data type (:attr:`compas.data.Data.dtype`),
and, most importantly, an attribute containing the underlying data of the object (:attr:`compas.data.Data.data`).

::

    >>> from compas.geometry import Point
    >>> point = Point(0, 0, 0)
    >>> point.guid
    UUID('48613a5b-4c9b-4d7c-8c88-59c28297fd75')
    >>> point.name
    'Point'
    >>> point.dtype
    'compas.geometry/Point'
    >>> point.data
    [0.0, 0.0, 0.0]


JSON Serialisation
==================


Validation
==========


GH Components
=============


Inherticance Diagrams
=====================

.. currentmodule:: compas.geometry

.. inheritance-diagram:: Bezier Circle Ellipse Frame Line Plane Point Polygon Polyline Quaternion Vector Box Capsule Cone Cylinder Polyhedron Sphere Torus Projection Reflection Rotation Shear Transformation Translation
    :parts: 1

.. currentmodule:: compas.datastructures

.. inheritance-diagram:: Mesh Network VolMesh
    :parts: 1

.. currentmodule:: compas.robots

.. inheritance-diagram:: RobotModel Joint Link ToolModel Configuration
    :parts: 1
