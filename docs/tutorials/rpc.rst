********************************************************************************
Setting up an RPC service
********************************************************************************

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

.. note::

    Currently, the RPC server is launched on the ``localhost``.
    However, it would also be possible to launch it on a remote computer on a
    network, or on a server reachable over the internet.


