"""
********************************************************************************
robots
********************************************************************************

.. currentmodule:: compas.robots


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
    ToolModel
    Configuration


Geometric description
=====================

The robot itself as well as its links can be geometrically described
using the following classes.

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Geometry
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

Deprecated
==========

.. deprecated:: 1.13.3
    Use `compas.geometry` primitives instead

The following classes are available for backwards compatibility but are deprecated.

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Origin
    Cylinder
    Box
    Sphere
    Capsule

"""
from __future__ import absolute_import

from .configuration import Configuration
from .model import (
    Axis,
    Calibration,
    ChildLink,
    Collision,
    Color,
    Dynamics,
    Geometry,
    Inertia,
    Inertial,
    Joint,
    Limit,
    Link,
    Mass,
    Material,
    MeshDescriptor,
    Mimic,
    ParentLink,
    RobotModel,
    SafetyController,
    Texture,
    ToolModel,
    Visual,
)
from .resources import (
    AbstractMeshLoader,
    DefaultMeshLoader,
    GithubPackageMeshLoader,
    LocalPackageMeshLoader,
)

# Deprecated aliases
from .model import (
    Origin,
    Box,
    Capsule,
    Cylinder,
    Sphere,
)

__all__ = [
    "Geometry",
    "MeshDescriptor",
    "Color",
    "Texture",
    "Material",
    "Joint",
    "ParentLink",
    "ChildLink",
    "Calibration",
    "Dynamics",
    "Limit",
    "Axis",
    "Mimic",
    "SafetyController",
    "Link",
    "Inertial",
    "Visual",
    "Collision",
    "Mass",
    "Inertia",
    "RobotModel",
    "ToolModel",
    "AbstractMeshLoader",
    "DefaultMeshLoader",
    "LocalPackageMeshLoader",
    "GithubPackageMeshLoader",
    "Configuration",
    # Deprecated aliases
    "Origin",
    "Box",
    "Capsule",
    "Cylinder",
    "Sphere",
]
