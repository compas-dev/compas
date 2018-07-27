"""
********************************************************************************
compas.robots
********************************************************************************

.. module:: compas.robots

This package provides basic structures and data exchange mechanisms that are
building blocks for robotics support.

The primary data representation for robot models is based on the Unified Robot Description Format
(`URDF`_). A detailed description of the model is avaible on the `URDF Model wiki`_.

This package parses URDF v1.0 according to the `URDF XSD Schema`_.

.. _URDF: http://wiki.ros.org/urdf
.. _URDF Model wiki: http://wiki.ros.org/urdf/XML/model
.. _URDF XSD Schema: https://github.com/ros/urdfdom/blob/master/xsd/urdf.xsd


Model
=====

The root of the URDF model is the :class::`Robot` class, which
describes a robot consisting of a set of link elements, and a set of joint
elements connecting the links together.

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Robot
    Joint
    Link
    Inertial
    Visual
    Collision
    Geometry
    Box
    Cylinder
    Sphere
    MeshDescriptor
    Origin
    Mass
    Inertia
    ParentJoint
    ChildJoint
    Calibration
    Dynamics
    Limit
    Axis
    Mimic
    SafetyController

"""

from __future__ import absolute_import

from .model import *

from . import model

__all__ = model.__all__
