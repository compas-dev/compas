"""
********************************************************************************
compas_hpc
********************************************************************************

.. module:: compas_hpc

This package provides GPU-accelerated and compiled versions of many geometry,
numerical and topological functions and algorithms. The package is built around
`Numba`_. Future versions will support `PyCUDA`_ and `PyOpenCL`_.

.. _Numba: https://numba.pydata.org/
.. _PyCuda: https://mathema.tician.de/software/pycuda/
.. _PyOpenCL: https://mathema.tician.de/software/pyopencl/


.. warning::

    The functionality of this package is experimental and subject to frequent change.
    For now, don't use it for anything important :)


.. toctree::
    :maxdepth: 1

    compas_hpc.geometry
    compas_hpc.numerical

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# from ._core import *  # noqa: F401 F403

__all__ = [name for name in dir() if not name.startswith('_')]
