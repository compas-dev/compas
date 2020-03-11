from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import time
import json

import compas

try:
    from xmlrpclib import ServerProxy
except ImportError:
    from xmlrpc.client import ServerProxy

try:
    from subprocess import Popen
    from subprocess import PIPE

except ImportError:
    try:
        from System.Diagnostics import Process
    except ImportError:
        compas.raise_if_ironpython()

import compas._os

from compas.utilities import DataEncoder

from compas.rpc import RPCServerError


__all__ = ['Proxy']


class Proxy(object):
    """Create a proxy object as intermediary between client code and remote functionality.

    This class is a context manager, so when used in a ``with`` statement,
    it ensures the remote proxy server is stopped and disposed correctly.

    However, if the proxy server is left open, it can be re-used for a follow-up connection,
    saving start up time.

    Parameters
    ----------
    package : string, optional
        The base package for the requested functionality.
        Default is `None`, in which case a full path to function calls should be provided.
    python : string, optional
        The python executable that should be used to execute the code.
        Default is ``'pythonw'``.
    url : string, optional
        The server address.
        Default is ``'http://127.0.0.1'``.
    port : int, optional
        The port number on the remote server.
        Default is ``1753``.

    Notes
    -----
    If the server is your *localhost*, which will often be the case, it is better
    to specify the address explicitly (``'http://127.0.0.1'``) because resolving
    *localhost* takes a surprisingly significant amount of time.

    The service will make the correct (version of the requested) functionality available
    even if that functionality is part of a virtual environment. This is because it
    will use the specific python interpreter for which the functionality is installed to
    start the server.

    If possible, the proxy will try to reconnect to an already existing service

    Examples
    --------
    Minimal example showing connection to the proxy server, and ensuring the
    server is disposed after using it:

    .. code-block:: python

        from compas.rpc import Proxy

        with Proxy('compas.numerical') as numerical:
            pass

    """

    def __init__(self, package=None, python=None, url='http://127.0.0.1', port=1753, service=None):
        self._package = None
        self._python = compas._os.select_python(python)
        self._url = url
        self._port = port
        self._service = None
        self._process = None
        self._function = None
        self._profile = None

        self.service = service
        self.package = package

        self._implicitely_started_server = False
        self._server = self._try_reconnect()
        if self._server is None:
            self._server = self.start_server()
            self._implicitely_started_server = True

    def __enter__(self):
        return self

    def __exit__(self, *args):
        # If we started the RPC server, we will try to clean up and stop it
        # otherwise we just disconnect from it
        if self._implicitely_started_server:
            self.stop_server()
        else:
            self._server.__close()

    @property
    def address(self):
        return "{}:{}".format(self._url, self._port)

    @property
    def profile(self):
        """A profile of the executed code."""
        return self._profile

    @profile.setter
    def profile(self, profile):
        self._profile = profile

    @property
    def package(self):
        """The base package from which functionality will be called."""
        return self._package

    @package.setter
    def package(self, package):
        self._package = package

    @property
    def service(self):
        return self._service

    @service.setter
    def service(self, service):
        if not service:
            self._service = 'compas.rpc.services.default'
        else:
            self._service = service

    @property
    def python(self):
        return self._python

    @python.setter
    def python(self, python):
        self._python = python

    def _try_reconnect(self):
        """Try and reconnect to an existing proxy server.

        Returns
        -------
        ServerProxy
            Instance of the proxy if reconnection succeeded, otherwise ``None``.
        """
        server = ServerProxy(self.address)
        try:
            server.ping()
        except Exception:
            return None
        else:
            print("Reconnecting to an existing server proxy.")
        return server

    def start_server(self):
        """Start the remote server.

        Returns
        -------
        ServerProxy
            Instance of the proxy, if the connection was successful.

        Raises
        ------
        RPCServerError
            If the server providing the requested service cannot be reached after
            100 contact attempts (*pings*).

        Examples
        --------
        >>> p = Proxy()
        >>> p.stop_server()
        >>> p.start_server()

        """
        env = compas._os.prepare_environment()
        # this part starts the server side of the RPC setup
        # it basically launches a subprocess
        # to start the default service
        # the default service creates a server
        # and registers a dispatcher for custom functionality
        try:
            Popen
        except NameError:
            self._process = Process()

            for name in env:
                if self._process.StartInfo.EnvironmentVariables.ContainsKey(name):
                    self._process.StartInfo.EnvironmentVariables[name] = env[name]
                else:
                    self._process.StartInfo.EnvironmentVariables.Add(name, env[name])
            self._process.StartInfo.UseShellExecute = False
            self._process.StartInfo.RedirectStandardOutput = True
            self._process.StartInfo.RedirectStandardError = True
            self._process.StartInfo.FileName = self.python
            self._process.StartInfo.Arguments = '-m {0} {1}'.format(self.service, str(self._port))
            self._process.Start()
        else:
            args = [self.python, '-m', self.service, str(self._port)]
            self._process = Popen(args, stdout=PIPE, stderr=PIPE, env=env)
        # this starts the client side
        # it creates a proxy for the server
        # and tries to connect the proxy to the actual server
        server = ServerProxy(self.address)
        print("Starting a new proxy server...")
        success = False
        count = 100
        while count:
            try:
                server.ping()
            except Exception:
                time.sleep(0.1)
                count -= 1
                print("    {} attempts left.".format(count))
            else:
                success = True
                break
        if not success:
            raise RPCServerError("The server is not available.")
        else:
            print("New proxy server started.")
        return server

    def stop_server(self):
        """Stop the remote server and terminate/kill the python process that was used to start it.

        Examples
        --------
        >>> p = Proxy()
        >>> p.stop_server()
        >>> p.start_server()
        """
        print("Stopping the server proxy.")
        try:
            self._server.remote_shutdown()
        except Exception:
            pass
        self._terminate_process()

    def _terminate_process(self):
        """Attempts to terminate the python process hosting the proxy server.

        The process reference might not be present, e.g. in the case
        of reusing an existing connection. In that case, this is a no-op.
        """
        if not self._process:
            return
        try:
            self._process.terminate()
        except Exception:
            pass
        try:
            self._process.kill()
        except Exception:
            pass

    def __getattr__(self, name):
        if self.package:
            name = "{}.{}".format(self.package, name)
        try:
            self._function = getattr(self._server, name)
        except Exception:
            raise RPCServerError()
        return self._proxy

    def _proxy(self, *args, **kwargs):
        """Callable replacement for the requested functionality.

        Parameters
        ----------
        args : list
            Positional arguments to be passed to the remote function.
        kwargs : dict
            Named arguments to be passed to the remote function.

        Returns
        -------
        object
            The result returned by the remote function.

        Warning
        -------
        The `args` and `kwargs` have to be JSON-serialisable.
        This means that, currently, only native Python objects are supported.
        The returned results will also always be in the form of built-in Python objects.
        """
        idict = {'args': args, 'kwargs': kwargs}
        istring = json.dumps(idict, cls=DataEncoder)
        # it makes sense that there is a broken pipe error
        # because the process is not the one receiving the feedback
        # when there is a print statement on the server side
        # this counts as output
        # it should be sent as part of RPC communication
        try:
            ostring = self._function(istring)
        except Exception:
            # not clear what the point of this is
            # self.stop_server()
            # if this goes wrong, it means a Fault error was generated by the server
            # no need to stop the server for this
            raise
        if not ostring:
            raise RPCServerError("No output was generated.")
        result = json.loads(ostring)
        if result['error']:
            raise RPCServerError(result['error'])
        self.profile = result['profile']
        return result['data']


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import doctest

    doctest.testmod(globs=globals())
