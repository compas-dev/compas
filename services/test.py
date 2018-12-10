import os
import inspect
import json
import socket

import compas

from compas.datastructures import Mesh
from compas.numerical import mesh_fd_numpy

from compas.rpc import Server
from compas.rpc import Service
from compas.rpc import kill
from compas.rpc import ping


class TestService(object):

    def mesh_fd_numpy(self, data):
        """Compute mesh equilibrium using the force density method.

        Parameters
        ----------
        data : str
            Mesh data serialised to a JSON string.

        Returns
        -------
        str
            Updated mesh data serialised to a JSON string.

        Examples
        --------
        .. code-block:: python

            data = client.mesh_fd_numpy(json.dumps(mesh.to_data()))
            mesh.data = json.loads(data)

        """
        mesh = Mesh.from_data(json.loads(data))
        mesh_fd_numpy(mesh)
        return json.dumps(mesh.to_data())


if __name__ == '__main__':

    server = Server(("localhost", 8888))

    server.register_function(ping)
    server.register_function(kill)

    server.register_instance(DefaultService())

    server.serve_forever()
