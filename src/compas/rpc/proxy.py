from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import json
import time

import compas
import compas._os
from compas.data import DataDecoder
from compas.data import DataEncoder
from compas.rpc import RPCServerError

try:
    from xmlrpclib import ServerProxy
except ImportError:
    from xmlrpc.client import ServerProxy

try:
    from subprocess import PIPE
    from subprocess import Popen
except ImportError:
    from System.Diagnostics import Process


class Proxy(object):
    """Create a proxy object as intermediary between client code and remote functionality.

    This class is a context manager, so when used in a ``with`` statement,
    it ensures the remote proxy server is stopped and disposed correctly.

    However, if the proxy server is left open, it can be re-used for a follow-up connection,
    saving start up time.

    Parameters
    ----------
    package : str, optional
        The base package for the requested functionality.
        Default is None, in which case a full path to function calls should be provided.
    python : str, optional
        The python executable that should be used to execute the code.
    url : str, optional
        The server address.
    port : int, optional
        The port number on the remote server.
    service : str, optional
        Package name to start server.
        Default is ``'compas.rpc.services.default'``.
    max_conn_attempts: int, optional
        Amount of attempts to connect to RPC server before time out.
    autoreload : bool, optional
        If True, automatically reload the proxied package if changes are detected.
        This is particularly useful during development. The server will monitor changes to the files
        that were loaded as a result of accessing the specified `package` and if any change is detected,
        it will unload the module, so that the next invocation uses a fresh version.
    capture_output : bool, optional
        If True, capture the stdout/stderr output of the remote process.
        In general, `capture_output` should be True when using a `pythonw` as executable (default).
    path : str, optional
        Path to the folder containing the module to be proxied.
        This is useful for cases where the module to be proxied is not on the PYTHONPATH.
    working_directory : str, optional
        Current working directory for the process that will be started to run the server.
        This is useful for cases where a custom service is used and the service is not on the PYTHONPATH.

    Attributes
    ----------
    address : str, read-only
        Address of the server as a combination of `url` and `port`.
    profile : str
        A profile of the code executed by the server.
    package : str
        Fully qualified name of the package or module
        from where functions should be imported on the server side.
    service : str
        Fully qualified package name required for starting the server/service.
    python : str
        The type of Python executable that should be used to execute the code.

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

    >>> from compas.rpc import Proxy  # doctest: +SKIP
    >>> with Proxy("compas.numerical") as numerical:  # doctest: +SKIP
    ...     pass  # doctest: +SKIP
    ...     # doctest: +SKIP
    Starting a new proxy server...                          # doctest: +SKIP
    New proxy server started.                               # doctest: +SKIP
    Stopping the server proxy.                              # doctest: +SKIP
    """

    def __init__(
        self,
        package=None,
        python=None,
        url="http://127.0.0.1",
        port=1753,
        service=None,
        max_conn_attempts=100,
        autoreload=True,
        capture_output=True,
        path=None,
        working_directory=None,
    ):
        self._package = None
        self._python = compas._os.select_python(python)
        self._url = url
        self._port = port
        self.max_conn_attempts = max_conn_attempts
        self._service = None
        self._process = None
        self._function = None
        self._profile = None
        self._path = path
        self._working_directory = working_directory

        self.service = service
        self.package = package
        self.autoreload = autoreload
        self.capture_output = capture_output

        self._implicitely_started_server = False
        self._server = self._try_reconnect()
        if self._server is None:
            self._server = self.start_server()
            self._implicitely_started_server = True

    # ==========================================================================
    # properties
    # ==========================================================================

    @property
    def address(self):
        return "{}:{}".format(self._url, self._port)

    @property
    def profile(self):
        return self._profile

    @profile.setter
    def profile(self, profile):
        self._profile = profile

    @property
    def package(self):
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
            self._service = "compas.rpc.services.default"
        else:
            self._service = service

    @property
    def python(self):
        return self._python

    @python.setter
    def python(self, python):
        self._python = python

    # ==========================================================================
    # customization
    # ==========================================================================

    def __enter__(self):
        return self

    def __exit__(self, *args):
        # If we started the RPC server, we will try to clean up and stop it
        # otherwise we just disconnect from it
        if self._implicitely_started_server:
            self.stop_server()
        else:
            self._server.__close()

    def __getattr__(self, name):
        """Find server attributes (methods) corresponding to attributes that do not exist on the proxy itself.

        1. Use :attr:`package` as a namespace for the requested attribute to create a fully qualified path on the server.
        2. Try to get the fully qualified attribute from :attr:`_server`.
        3. If successful, store the result in :attr:`_function`.
        3. Return a handle to :meth:`_proxy`, which will delegate calls to :attr:`_function`.

        Returns
        -------
        callable

        """
        if self.package:
            name = "{}.{}".format(self.package, name)
        try:
            self._function = getattr(self._server, name)
        except Exception:
            raise RPCServerError()
        return self._proxy

    # ==========================================================================
    # methods
    # ==========================================================================

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
            100 contact attempts (*pings*). The number of attempts is set by
            :attr:`Proxy.max_conn_attempts`.

        Examples
        --------
        >>> p = Proxy()  # doctest: +SKIP
        >>> p.stop_server()  # doctest: +SKIP
        >>> p.start_server()  # doctest: +SKIP

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
            self._process.StartInfo.RedirectStandardOutput = self.capture_output
            self._process.StartInfo.RedirectStandardError = self.capture_output
            self._process.StartInfo.FileName = self.python
            self._process.StartInfo.Arguments = "-m {0} --port {1} --{2}autoreload".format(self.service, self._port, "" if self.autoreload else "no-")
            self._process.Start()
        else:
            args = [
                self.python,
                "-m",
                self.service,
                "--port",
                str(self._port),
                "--{}autoreload".format("" if self.autoreload else "no-"),
            ]
            kwargs = dict(env=env)
            if self.capture_output:
                kwargs["stdout"] = PIPE
                kwargs["stderr"] = PIPE
            if self._working_directory:
                kwargs["cwd"] = self._working_directory

            self._process = Popen(args, **kwargs)

        # this starts the client side
        # it creates a proxy for the server
        # and tries to connect the proxy to the actual server
        server = ServerProxy(self.address)

        print("Starting a new proxy server...")
        success = False
        attempt_count = 0
        while attempt_count < self.max_conn_attempts:
            try:
                server.ping()
            except Exception:
                time.sleep(0.1)
                attempt_count += 1
                print("    {} attempts left.".format(self.max_conn_attempts - attempt_count))
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

        Returns
        -------
        None

        Examples
        --------
        >>> p = Proxy()  # doctest: +SKIP
        >>> p.stop_server()  # doctest: +SKIP
        >>> p.start_server()  # doctest: +SKIP

        """
        print("Stopping the server proxy.")
        try:
            self._server.remote_shutdown()
        except Exception:
            pass
        self._terminate_process()

    def restart_server(self):
        """Restart the server.

        Returns
        -------
        None

        """
        self.stop_server()
        self.start_server()

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

    def _proxy(self, *args, **kwargs):
        """Callable replacement for the requested functionality.

        Parameters
        ----------
        *args : list
            Positional arguments to be passed to the remote function.
        **kwargs : dict, optional
            Named arguments to be passed to the remote function.

        Returns
        -------
        object
            The 'data' part of the result dict returned by the remote function.
            The result dict has the following structure ::

                {
                    "error": ...,  # A traceback of the error raised on the server, if any.
                    "profile": ...,  # A profile of the code executed on the server, if there was no error.
                    "data": ...,  # The result returned by the target function, if there was no error.
                }

        Warnings
        --------
        The `args` and `kwargs` have to be JSON-serializable.
        This means that, currently, only COMPAS data objects (geometry, robots, data structures) and native Python objects are supported.
        The returned results will also always be in the form of COMPAS data objects and built-in Python objects.
        Numpy objects are automatically converted to their built-in Python equivalents.

        """
        idict = {"args": args, "kwargs": kwargs}
        istring = json.dumps(idict, cls=DataEncoder)
        # it makes sense that there is a broken pipe error
        # because the process is not the one receiving the feedback
        # when there is a print statement on the server side
        # this counts as output
        # it should be sent as part of RPC communication
        try:
            ostring = self._function(istring, self._path or "")
        except Exception:
            # not clear what the point of this is
            # self.stop_server()
            # if this goes wrong, it means a Fault error was generated by the server
            # no need to stop the server for this
            raise

        if not ostring:
            raise RPCServerError("No output was generated.")

        result = json.loads(ostring, cls=DataDecoder)

        if result["error"]:
            raise RPCServerError(result["error"])

        self.profile = result["profile"]
        return result["data"]
