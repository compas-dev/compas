from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import os
import time
import json

try:
    from xmlrpclib import ServerProxy
except ImportError:
    from xmlrpc.client import ServerProxy

from subprocess import Popen, PIPE, STDOUT

import compas
import compas._os

from compas.utilities import DataEncoder
from compas.utilities import DataDecoder

from compas.rpc import RPCServerError


__all__ = ['Proxy']


class Proxy(object):
    """Create a proxy object as intermediary between client code and remote functionality.

    Parameters
    ----------
    package : string, optional
        The base package for the requested functionality.
        Default is `None`, in which case a full path to function calls should be provided.
    python : string, optional
        The python executable that should be used to execute the code.
        Default is `'pythonw'`.
    url : string, optional
        The server address.
        Default is `'http://127.0.0.1'`.
    port : int, optional
        The port number on the remote server.
        Default is `1753`.

    Attributes
    ----------
    profile : string
        A time profile of the executed code.

    Notes
    -----
    If the server is your *localhost*, which will often be the case, it is better
    to specify the address explicitly (`'http://127.0.0.1'`) because resolving
    *localhost* takes a surprisingly significant amount of time.

    Examples
    --------
    .. code-block:: python

        import compas
        import time

        from compas.datastructures import Mesh
        from compas.rpc import Proxy

        numerical = Proxy('compas.numerical')

        mesh = Mesh.from_obj(compas.get('faces_big.obj'))

        mesh.update_default_vertex_attributes({'px': 0.0, 'py': 0.0, 'pz': 0.0})
        mesh.update_default_edge_attributes({'q': 1.0})

        key_index = mesh.key_index()

        xyz   = mesh.get_vertices_attributes('xyz')
        edges = [(key_index[u], key_index[v]) for u, v in mesh.edges()]
        fixed = [key_index[key] for key in mesh.vertices_where({'vertex_degree': 2})]
        q     = mesh.get_edges_attribute('q', 1.0)
        loads = mesh.get_vertices_attributes(('px', 'py', 'pz'), (0.0, 0.0, 0.0))

        xyz, q, f, l, r = numerical.fd_numpy(xyz, edges, fixed, q, loads)

        for key, attr in mesh.vertices(True):
            index = key
            attr['x'] = xyz[index][0]
            attr['y'] = xyz[index][1]
            attr['z'] = xyz[index][2]
            attr['rx'] = r[index][0]
            attr['ry'] = r[index][1]
            attr['rz'] = r[index][2]

        for index, (u, v, attr) in enumerate(mesh.edges(True)):
            attr['f'] = f[index][0]
            attr['l'] = l[index][0]

    """

    def __init__(self, package=None, python=None, url='http://127.0.0.1', port=1753):
        self._package = package
        self._python = compas._os.select_python(python)
        self._url = url
        self._port = port
        self._process = None
        self._server = None
        self._function = None
        self.profile = None
        self.stop_server()
        self.start_server()

    def __del__(self):
        self.stop_server()

    def start_server(self):
        """Start the remote server.

        Raises
        ------
        RPCServerError
            If the server providing the requested service cannot be reached after
            100 contact attempts (*pings*).

        """
        python = self._python
        args = [python, '-m', 'compas.rpc.services.default', str(self._port)]
        address = "{}:{}".format(self._url, self._port)

        self._process = Popen(args, stdout=PIPE, stderr=STDOUT)
        self._server = ServerProxy(address)

        success = False
        count = 100
        while count:
            try:
                self._server.ping()
            except:
                time.sleep(0.01)
                count -= 1
            else:
                success = True
                break
        if not success:
            raise RPCServerError("The server is no available.")

    def stop_server(self):
        """Stop the remote server and terminate/kill the python process that was used to start it.
        """
        try:
            self._server.remote_shutdown()
        except:
            pass
        try:
            self._process.terminate()
        except:
            pass
        try:
            self._process.kill()
        except:
            pass

    def __getattr__(self, name):
        if self._package:
            name = "{}.{}".format(self._package, name)
        try:
            self._function = getattr(self._server, name)
        except:
            raise RPCServerError()
        return self.proxy

    def proxy(self, *args, **kwargs):
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

        try:
            ostring = self._function(istring)
        except:
            self.stop_server()
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

    import compas

    from compas.datastructures import Mesh
    from compas.rpc import Proxy

    from compas_rhino.artists import MeshArtist

    # this is not how a server proxy should be used
    # the server should be started somewhere independently
    # and then used in real-time

    numerical = Proxy('compas.numerical')

    mesh = Mesh.from_obj(compas.get('faces.obj'))

    mesh.update_default_vertex_attributes({'px': 0.0, 'py': 0.0, 'pz': 0.0})
    mesh.update_default_edge_attributes({'q': 1.0})

    key_index = mesh.key_index()

    xyz   = mesh.get_vertices_attributes('xyz')
    edges = [(key_index[u], key_index[v]) for u, v in mesh.edges()]
    fixed = [key_index[key] for key in mesh.vertices_where({'vertex_degree': 2})]
    q     = mesh.get_edges_attribute('q', 1.0)
    loads = mesh.get_vertices_attributes(('px', 'py', 'pz'), (0.0, 0.0, 0.0))

    xyz, q, f, l, r = numerical.fd_numpy(xyz, edges, fixed, q, loads)

    for key, attr in mesh.vertices(True):
        index = key
        attr['x'] = xyz[index][0]
        attr['y'] = xyz[index][1]
        attr['z'] = xyz[index][2]
        attr['rx'] = r[index][0]
        attr['ry'] = r[index][1]
        attr['rz'] = r[index][2]

    for index, (u, v, attr) in enumerate(mesh.edges(True)):
        attr['f'] = f[index][0]
        attr['l'] = l[index][0]

    artist = MeshArtist(mesh)

    artist.draw_vertices()
    artist.draw_faces()

    artist.redraw()

    numerical.stop_server()
