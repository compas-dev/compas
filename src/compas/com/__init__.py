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

    MatlabClient
    MatlabEngine
    MatlabProcess
    MatlabSession


============= ============
Interface     Case
============= ============
MatlabClient  Operating system is Windows. Matlab version is older than 2014b.
MatlabProcess Operating system is not Windows. Matlab version is older than 2014b.
MatlabEngine  All operating systems. Matlab version is 2014b or above. No shared Matlab session is available.
MatlabSession All operating systems. Matlab version is 2014b or above. A shared Matlab session is already available.
============= ============

"""


class Process(object):
    pass


class Client(object):
    pass



from .mlab import *
# from .rhino import *

from .mlab import __all__ as a
# from .rhino import __all__ as b

__all__ = a
