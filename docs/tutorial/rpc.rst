********************************************************************************
Remote Procedure Calls
********************************************************************************

* :mod:`compas.rpc`

Through ``Xfunc``, COMPAS provides a mechanism for calling Python functions through
a separately launched subprocess. This provides the posibility of, for example,
using functionality that relies on CPython-specific packages (such as Numpy) directly
from Rhino.

A drawback of the ``Xfunc`` mechanism is that evey call launches a new Python
(sub)process with all the overhead that that entails. For infrequent calls to
long-running processes this is not an issue. However, for frequent calls to function
that are expected to run quickly, this is not ideal.

The principle of RPC is to start a server that handles all requests. The advantage
is that once the server is started, no additional processes have to launched and
the server can handle the requests without any overhead. Therefore, the response
time is much faster than with ``XFunc``.


Basic Usage
===========

.. code-block:: python

    from compas.rpc import Proxy
    numerical = Proxy('compas.numerical')

    result = numerical.fd_numpy(...)


Supported data types
====================


Switching packages
==================


Starting and Stopping
=====================


Starting an RPC server manually
===============================

``Proxy`` will try to start an RPC server automatically
if no server is already running, but very often it is recommended
to start it manually from the command-line.

To start a new RPC server use the following command on the terminal
(default port is ``1753``):

::

    $ compas_rpc start <port>

Conversely, to stop an existing RPC server:

::

    $ compas_rpc stop <port>


.. note::

    If COMPAS is installed in a virtual environment, make sure it is activated
    before trying to use this command-line utility.

.. note::

    Currently, the RPC server is launched on the ``localhost``.
    However, it would also be possible to launch it on a remote computer on a
    network, or on a server reachable over the internet.
