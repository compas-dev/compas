"""
********************************************************************************
rpc
********************************************************************************

.. currentmodule:: compas.rpc

**COMPAS** runs in many different environments, but some environments
limit the availablity of libraries, for example, when running **COMPAS** from
an IronPython environment like Rhino/Grasshopper, plenty of the CPython libraries
such as ``numpy``, ``scipy``, etc are not usable.

To workaround this limitation, **COMPAS** provides two mechanisms to access the
CPython environment seemlessly from any other Python environment. One of them is
called ``XFunc`` (:class:`compas.utilities.XFunc`) and it works very effectively to
make single, but expensive calls that execute long-running bits of code. The other
one is called ``RPC``, which stands for `Remote Procedure Call`` and it allows to
create a transparent proxy/connection between our environment and the one where
all the fast libraries and dependencies of **COMPAS** are installed. It also allows
to re-use the same process for many small calls, making it much more effective for
the cases in which the required functionality  is not easily isolated in one
long-running function.

Proxy
=====

In order to use the RPC communication package, we create an instance of the
``Proxy`` class to one specific package that we want to have access to.
After the proxy is created, it behaves as a regular Python on which the functions
of the proxied package are available as if they were directly present in our environment.

.. autosummary::
    :toctree: generated/
    :nosignatures:

    Proxy

RPC Command-line utility
========================

Besides the API of the RPC module, there is a command-line utility
provided to start and stop the RPC server easily from the terminal.

To start a new RPC server use the following command (default port is ``1753``):

::

    $ compas_rpc start <port>

Conversely, to stop an existing RPC server:

::

    $ compas_rpc stop <port>


.. note::

    If COMPAS is installed in a virtual environment, make sure it is activated
    before trying to use this command-line utility.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


class RPCServerError(Exception):
    pass


class RPCClientError(Exception):
    pass


from .proxy import *
from .server import *
from .dispatcher import *


__all__ = [name for name in dir() if not name.startswith('_')]
