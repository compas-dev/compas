"""
.. _compas.com:

********************************************************************************
com
********************************************************************************

.. module:: compas.com


Interface(s) for communication with external software.


Matlab
======

.. autosummary::
    :toctree: generated/
    :nosignatures:

    MatlabClient
    MatlabEngine
    MatlabProcess
    MatlabSession

ssh
===

.. autosummary::
    :toctree: generated/
    :nosignatures:

    connect_to_server
    local_command
    receive_file
    send_file
    send_folder
    sync_folder
    server_command

"""


class Process(object):
    pass


class Client(object):
    pass


from .matlab import *
from .ssh import *
# from .rhino import *

from .matlab import __all__ as a
from .ssh import __all__ as b
# from .rhino import __all__ as b

__all__ = a + b
