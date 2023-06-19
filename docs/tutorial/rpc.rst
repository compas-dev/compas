********************************************************************************
Remote Procedure Calls
********************************************************************************

Remote Procedure Calls (``RPC``) is a mechanism to transparently execute code in
a remote process or computer. This is especially useful in scenarios where COMPAS
runs inside an IronPython host (eg. Rhino) and needs to execute code that only
runs on CPython (eg. code that requires ``numpy``).


Basic Usage
===========

The basic usage of RPC is simple.
For example, consider a CPython script using the Force Density method. ::

    >>> from compas.numerical import fd_numpy
    >>> result = fd_numpy(...)

This script does not work in Rhino or GH because Numpy is not available.
Therefore, instead of importing and calling the function directly,
we call it through a proxy object. ::

    >>> from compas.rpc import Proxy
    >>> numerical = Proxy('compas.numerical')
    >>> result = numerical.fd_numpy(...)

To use functions from more than one package in the same script, simply change the
package attribute of the proxy object, which determines where the proxy will look
for the requested function. ::

    >>> from compas.rpc import Proxy
    >>> proxy = Proxy()

    >>> proxy.package = 'compas.numerical'
    >>> proxy.fd_numpy(...)

    >>> proxy.package = 'compas.geometry'
    >>> proxy.bestfit_plane_numpy(...)

The use of :mod:`compas.rpc` is not restricted to COMPAS packages only. ::

    >>> from compas.rpc import Proxy
    >>> linalg = Proxy('scipy.linalg')
    >>> x = linalg.solve(A, b)

Note that Numpy arrays are automatically converted to lists.


Configuration Options
=====================

The :class:`compas.rpc.Proxy` object has several configuration options.
We will discuss only a few of those here.
For a complete overview, please refer to the API docs (:mod:`compas.rpc`).

``python``
----------

The :class:`compas.rpc.Proxy` object will automatically try to reconnect to an
active instance of the command server, or start a new one if no active server can be found.
By default, a newly started server will run an instance of the default Python interpreter
of the active environment, for example, when running RPC from the command line;
or of the Python interpreter specified in `compas_bootstrapper`, for example, when running RPC from Rhino.

In some cases, this might not be what you want, or might not result in the expected behaviour,
for example when `compas_bootstrapper` does not exist.

To use a specific Python iterpreter, you can specify the path to an executable through the ``python`` parameter.

.. code-block:: python

    >>> from compas.rpc import Proxy
    >>> proxy = Proxy(python=r"C:\\Users\\<username>\\anaconda3\\envs\\research\\python.exe")


``path``
--------

Sometimes you will want the server to run custom functions that are not (yet) part of a specific package.
To allow the server to find such functions, you can specify an additional search path.

For example, if you have a Python script on your desktop,
defining a wrapper for the k-means clustering algorithm of ``scikit-learn``,
you can tell the command server where to find it using the ``path`` parameter.

.. code-block:: python

    # C:\Users\<username>\Desktop\clustering.py

    from sklearn.cluster import KMeans
    from numpy import array


    def cluster(points, n_clusters):
        kmeans = KMeans(n_clusters=n_clusters, n_init=2000, max_iter=1000).fit(array(cloud, dtype=float))
        clusters = {}
        for label, point in zip(kmeans.labels_, cloud):
            if label not in clusters:
                clusters[label] = []
            clusters[label].append(point)
        return clusters


.. code-block:: python

    >>> from compas.geometry import Pointcloud
    >>> from compas.rpc import Proxy
    >>> cloud = Pointcloud.from_bounds(10, 5, 3, 100)
    >>> proxy = Proxy(package='clustering', path=r'C:\\Users\\<username>\\Desktop')
    >>> clusters = proxy.cluster(cloud, 10)


Supported data types
====================

:mod:`compas.rpc` uses JSON serialization to transfer data between the "client"
(your script) and the server running the selected CPython environment.

All COMPAS objects (primitives, shapes, data structures, etc.) support JSON
serialization through their ``to_json`` ``from_json`` methods. On a lower level,
these methods convert (complex) internal data to simple dictionaries, and
vice versa, with ``to_data`` and ``from_data``.

In combination with custom JSON encoders and decoders this allows for COMPAS
objects to be serialized and de-serialized without loss of information on either
side of the RPC communication network.

Therefore the data types supported by :mod:`compas.rpc` include all native Python
data types and COMPAS objects. Numpy arrays are automatically converted to lists.


Starting and Stopping
=====================

Once a server is started it will keep running "as long as possible".
There are many reasons to stop and (re)start the server during its lifetime.
For example, to load functionality from a different conda environment, or to
load changes that were made to the packages in the environment after it was started.
This happens frequently while a package is still under active development.

Stopping and starting the server is easy. ::

    >>> from compas.rpc import Proxy
    >>> proxy = Proxy()
    >>> proxy.stop_server()
    >>> proxy.start_server()

To restart the server after every call, you can use a context manager.
When used in this way, RPC behaves much like its predecessor ``XFunc``. ::

    >>> with Proxy('compas.numerical') as numerical:
    ...     numerical.fd_numpy(...)
    ...


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
