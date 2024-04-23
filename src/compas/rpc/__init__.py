"""
COMPAS runs in many different environments, but in some environments the availablity of libraries is limited.
For example, when running COMPAS in an IronPython-based environment like Rhino/Grasshopper,
plenty of CPython libraries such as `numpy` and `scipy` are not available.
To workaround this limitation, COMPAS provides a mechanisms to access the functionality of a CPython environment
seemlessly from any other Python environment through a "Remote Procedure Call" or RPC.
Through RPC, COMPAS can be used as a server for remote clients, and as a client for remote servers.
A typical use case is to run algorithms that require packages like ``numpy`` or ``scipy`` on a remote server,
when working in Rhino. Or to use COMPAS in a browser application.
"""

from __future__ import absolute_import

from .errors import RPCClientError, RPCServerError
from .proxy import Proxy
from .server import Server
from .dispatcher import Dispatcher


__all__ = ["RPCClientError", "RPCServerError", "Proxy", "Server", "Dispatcher"]
