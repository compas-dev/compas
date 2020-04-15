"""
********************************************************************************
compas
********************************************************************************

.. currentmodule:: compas


.. toctree::
    :maxdepth: 1

    compas.datastructures
    compas.files
    compas.geometry
    compas.numerical
    compas.robots
    compas.rpc
    compas.topology
    compas.utilities

"""

import os
import sys

if sys.version_info[0] != 3:
    del sys.modules['compas']

    TRANSPILED_SRC = os.path.abspath(os.path.join(os.path.dirname(__file__), '_transpiled27'))
    sys.path.insert(0, TRANSPILED_SRC)

    from compas import *
else:
    from compas.__init__3x import *
