from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


class RPCServerError(Exception):
    """Exception for errors originating from the server."""


class RPCClientError(Exception):
    """Exception for errors originating from the client."""
