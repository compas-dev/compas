"""
********************************************************************************
rpc
********************************************************************************

.. currentmodule:: compas.rpc

COMPAS runs in many different environments, but in some environments the availablity of libraries is limited.
For example, when running COMPAS in an IronPython-based environment like Rhino/Grasshopper,
plenty of CPython libraries such as ``numpy`` and ``scipy`` are not available.

To workaround this limitation, COMPAS provides a mechanisms to access the
functionality of a CPython environment seemlessly from any other Python environment
through a ``Remote Procedure Call`` or RPC.


Classes
=======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Proxy

"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from .errors import *  # noqa: F401 F403
from .proxy import *  # noqa: F401 F403
from .server import *  # noqa: F401 F403
from .dispatcher import *  # noqa: F401 F403


__all__ = [name for name in dir() if not name.startswith('_')]
