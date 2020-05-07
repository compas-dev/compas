********************************************************************************
Remote Procedure Calls
********************************************************************************

* :mod:`compas.rpc`

Remote Procedure Calls (``RPC``) is a mechanism to transparently execute code in
a remote process or computer. This is especially useful in scenarios where COMPAS
runs inside an IronPython host (eg. Rhino) and needs to execute code that only
runs on CPython (eg. code that requires ``numpy``).

COMPAS provides **two ways to achieve** this: ``rcp`` and `XFunc``.

Through ``Xfunc``, COMPAS provides a mechanism for calling Python functions through
a separately launched subprocess.

A drawback of the ``Xfunc`` mechanism is that evey call launches a new Python
(sub)process with all the overhead that that entails. For infrequent calls to
long-running processes this is not an issue. However, for frequent calls to function
that are expected to run quickly, this is not ideal.

The second mechanism is the ``rpc`` module. The principle of RPC is to start a server
that handles all requests. The advantage is that once the server is started,
no additional processes have to launched and the server can handle the requests
without any overhead. Therefore, the response time is much faster than with ``XFunc``.


Basic Usage
===========

.. code-block:: python

    from compas.rpc import Proxy

    with Proxy('compas.numerical') as numerical:
        result = numerical.fd_numpy(...)


Supported data types
====================

The RPC service is able to serialize objects that implement the ``to_data/from_data`` protocol
of COMPAS, as well as all python built-ins, ``numpy`` arrays and ``numpy`` primitive data types.

.. note::

    RPC implies that data needs to be converted back and forth. Internally, RPC uses JSON as a serialization
    format. This means that some floating-point precision loss will occur when passing around ``numpy`` values.

Switching packages
==================

The RPC proxy is usually initialized with one package name, but it can be switched at any point.
The following example shows how to calculate the inverse of a ``numpy`` matrix using ``scipy``
lineal algebra functions.

.. code-block:: python

    from compas.rpc import Proxy

    with Proxy('numpy') as proxy:

        A = proxy.array([[1, 2], [3, 4]])

        proxy.package = 'scipy.linalg'
        r = proxy.inv(A)

Starting an RPC server manually
===============================

``Proxy`` will try to start an RPC server automatically
if no server is already running, but very often it is recommended
to start it manually from the command-line.

To start a new RPC server use the following command on the terminal
(default port is ``1753``):

::

    $ compas_rpc start [--port PORT]

Conversely, to stop an existing RPC server:

::

    $ compas_rpc stop [--port PORT]


.. note::

    If COMPAS is installed in a virtual environment, make sure it is activated
    before trying to use this command-line utility.

.. note::

    Currently, the RPC server is launched on the ``localhost``.
    However, it would also be possible to launch it on a remote computer on a
    network, or on a server reachable over the internet.
