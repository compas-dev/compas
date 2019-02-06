"""
********************************************************************************
robots
********************************************************************************

.. currentmodule:: compas.robots

This package provides basic structures and data exchange mechanisms that are
building blocks for robotics support.

The primary data representation for robot models is based on the Unified Robot Description Format
(`URDF`_).

.. note::

    A detailed description of the model is available on the `URDF Model wiki`_.
    This package parses URDF v1.0 according to the `URDF XSD Schema`_.

    * `URDF`_
    * `URDF Model wiki`_
    * `URDF XSD Schema`_

.. _URDF: http://wiki.ros.org/urdf
.. _URDF Model wiki: http://wiki.ros.org/urdf/XML/model
.. _URDF XSD Schema: https://github.com/ros/urdfdom/blob/master/xsd/urdf.xsd


Model
=====

The root of the model is the :class:`RobotModel` class, which
describes a robot consisting of a set of link elements, and a set of joint
elements connecting the links together.

.. autosummary::
    :toctree: generated/
    :nosignatures:

    RobotModel
    Joint
    Link

Geometric description
=====================

The robot itself as well as its links can be geometrically described
using the following classes.

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Origin
    Geometry
    Box
    Cylinder
    Sphere
    Capsule
    MeshDescriptor
    Material
    Texture
    Color

Link
====

The link is described as a rigid body with inertial, visual and collision values.

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Visual
    Collision
    Inertial
    Mass
    Inertia

Joint
=====

The joint describes the kinematics and dynamics of the robot's joint.

.. autosummary::
    :toctree: generated/
    :nosignatures:

    ParentLink
    ChildLink
    Calibration
    Dynamics
    Limit
    Axis
    Mimic
    SafetyController

Resources
=========

Model descriptions usually do not contain embedded geometry information but only
descriptions, filenames or URLs for externally hosted resources.
For that purpose, this package provides various loader classes that help automate
the processing of these resources.

.. autosummary::
    :toctree: generated/
    :nosignatures:

    AbstractMeshLoader
    DefaultMeshLoader
    GithubPackageMeshLoader
    LocalPackageMeshLoader

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from .model import *
from .resources import *

__all__ = [name for name in dir() if not name.startswith('_')]
