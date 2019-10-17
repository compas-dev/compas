import json
import time
import compas

if compas.IPY:
    from System.Diagnostics import Process
    import compas_rhino

else:
    from subprocess import Popen
    from subprocess import PIPE
    from subprocess import STDOUT

try:
    from urllib.request import urlopen
    from urllib.request import urlretrieve
    from urllib.parse import urlencode
    from urllib.request import Request

except ImportError:
    from urllib2 import urlopen
    from urllib import urlretrieve
    from urllib import urlencode
    from urllib2 import Request

from compas.remote import ThreadedServer
from compas.remote import ThreadedServerError

from compas.utilities import DataDecoder
from compas.utilities import DataEncoder


__all__ = ['Proxy']


class Proxy(object):
    """Class for handling the client side of calls to functionality made available on a server.

    Parameters
    ----------
    module : str, optional
        The module from which the requested functionality should be loaded on the server side.
    python : {'python', 'pythonw'}, optional
        The type of Python interpreter that should be used to launch the server.
    url : str, optional
        The URL from where the requested functionality should be served.
        Defaults is ``'http://127.0.0.1'``.
    port : int, optional
        The port through which the host at the provided URL should be accessed.
        Default is ``1753``.

    Notes
    -----
    When a :class:`Proxy` class is instantiated, it tries to establish a connection with the server at the specified address.
    The default address is ``http://127.0.0.1:1753``. If no server is available at the provided address that support the
    ``ping_server`` "protokol", it will try to start a new server. If this is unsuccessfull, a ``ThreadedServerError`` will
    be raised.

    If a server is available at the specified address, the :class:`Proxy` object will send JSON encoded requests in the
    following format:

    * ``'module'``: The fully qualified path of the module from which the functionality should be loaded.
    * ``'function'``: The name of the function that should be run by the server.
    * ``'args'`` : A list of positional arguments that should be passed to the remote function.
    * ``'kwargs'`` : A dict of named arguments that should be passed to the remote function.

    The modules available to the server for loading functionality depend on the environment in which the subprocess is launched
    originally started the server. This means that the client side code should be run from the environent that should be
    available on the server side.

    Since the module is only used to qualify the requested functionality whenever that functionality is called, the module
    can be changed at any time to request calls to functionality from different modules.

    Examples
    --------
    >>> from compas.remote import Proxy
    >>> p = Proxy()
    >>> p.ping_server()
    1

    """

    def __init__(self, module=None, python=None, url='http://127.0.0.1', port=1753, service='default'):
        self._process = None
        self._service = service
        self._python = compas._os.select_python(python)  # change to pythonw == True
        self._env = compas._os.prepare_environment()
        self._url = url
        self._port = port
        self.module = module
        self.function = None
        self.profile = None
        self.start_server()

    @property
    def address(self):
        """The address (including the port) of the server host."""
        return "{}:{}".format(self._url, self._port)

    def ping_server(self, attempts=10):
        """Ping the server to check if it is available at the provided address.

        Parameters
        ----------
        attempst : int, optional
            The number of attemps before the function should give up.
            Default is ``10``.

        Returns
        -------
        int
            ``1`` if the server is available.
            ``0`` otherwise.

        """
        while attempts:
            try:
                result = self.send_request('ping')
            except Exception as e:
                if compas.IPY:
                    compas_rhino.wait()
                result = 0
                time.sleep(0.1)
                attempts -= 1
                print("    {} attempts left.".format(attempts))
            else:
                break
        return result

    def start_server(self):
        """Start the remote server.

        Returns
        -------
        ServerProxy
            Instance of the proxy, if the connection was successful.

        Raises
        ------
        ThreadedServerError
            If the server providing the requested service cannot be reached.

        """
        if self.ping_server():
            print("Server running at {}...".format(self.address))
            return

        if compas.IPY:
            self._process = Process()
            for name in self._env:
                if self._process.StartInfo.EnvironmentVariables.ContainsKey(name):
                    self._process.StartInfo.EnvironmentVariables[name] = self._env[name]
                else:
                    self._process.StartInfo.EnvironmentVariables.Add(name, self._env[name])
            self._process.StartInfo.UseShellExecute = False
            self._process.StartInfo.RedirectStandardOutput = True
            self._process.StartInfo.RedirectStandardError = True
            self._process.StartInfo.FileName = self._python
            self._process.StartInfo.Arguments = '-m {0} {1}'.format('compas.remote.services.{}'.format(self._service), str(self._port))
            self._process.Start()

        else:
            args = [self._python, '-m', 'compas.remote.services.{}'.format(self._service)]
            self._process = Popen(args, stdout=PIPE, stderr=STDOUT, env=self._env)

        # this doesn't work because (at least on my computer)
        # you have to allow the server to accept incoming connections
        # while you click on the dialog to confirm
        # the ping times out
        # and the function throws an error
        # it does start the server anyway though :)

        # if not self.ping_server():
        #     raise ThreadedServerError("Server unavailable at {}...".format(self.address))

        print("Started {} service at {}...".format(self._service, self.address))

    def send_request(self, function, module=None, args=None, kwargs=None):
        """Send a request to the server.

        Parameters
        ----------
        function : str
            The name of the function that should be run on the server.
        module : str, optional
            The fully qualified name of the module from where the function should be loaded.
        args : list, optional
            Positional function arguments.
        kwargs : dict, optional
            Named function arguments.

        Returns
        -------
        object
            The data returned by the server function.

        Raises
        ------
        ThreadedServerError
            If the execution of the function on the server throws an error.

        Notes
        -----
        The response of the server is a dict with the following items:

        * ``'error'``: Stores a traceback of any exception thrown during execution of the requested function on the server.
        * ``'data'``: Stores data returned by the server function.
        * ``'profile'``: Stores a profile of the function execution.

        """
        idata = {'function': function,
                 'module': module,
                 'args': args,
                 'kwargs': kwargs}
        ibody = json.dumps(idata, cls=DataEncoder).encode('utf-8')
        request = Request(self.address, ibody)
        request.add_header('Content-Type', 'application/json; charset=utf-8')
        request.add_header('Content-Length', len(ibody))
        response = urlopen(request)
        obody = response.read().decode('utf-8')
        odata = json.loads(obody, cls=DataDecoder)
        self.profile = odata['profile']
        if odata['error']:
            raise ThreadedServerError(odata['error'])
        return odata['data']

    def __getattr__(self, function):
        self.function = function
        return self._function_proxy

    def _function_proxy(self, *args, **kwargs):
        """"""
        return self.send_request(self.function, module=self.module, args=args, kwargs=kwargs)

    def stop_server(self):
        """"""
        self.send_request('stop_server')
        self.terminate_process()

    def terminate_process(self):
        """Attempts to terminate the python process hosting the http server.

        The process reference might not be present, e.g. in the case
        of reusing an existing connection. In that case, this is a no-op.
        """
        # find the process listening to port 1753?
        # kill that process instead?

        if not self._process:
            return
        try:
            self._process.terminate()
        except:
            pass
        try:
            self._process.kill()
        except:
            pass


# =============================================================================
# Main
# =============================================================================

if __name__ == '__main__':

    pass
