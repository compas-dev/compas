from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


class DataArtistNotRegistered(Exception):
    """Exception that is raised when no artist is registered for a given data type."""
