from __future__ import absolute_import

from .configuration import Configuration

from .resources.basic import AbstractMeshLoader, DefaultMeshLoader, LocalPackageMeshLoader
from .resources.github import GithubPackageMeshLoader

# from .model.base import FrameProxy, ProxyObject
from .model.geometry import Box, Capsule, Color, Cylinder, Geometry, Material, MeshDescriptor, Origin, Sphere, Texture
from .model.joint import Axis, Calibration, ChildLink, Dynamics, Joint, Limit, Mimic, ParentLink, SafetyController
from .model.link import Collision, Inertia, Inertial, Link, Mass, Visual
from .model.robot import RobotModel
from .model.tool import ToolModel

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
