from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


class SceneObjectNotRegisteredError(Exception):
    """Exception that is raised when no scene object is registered for a given data type."""
