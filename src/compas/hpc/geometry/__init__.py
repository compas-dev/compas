"""
High performance version of the geometry library.
These implementations are not the default, because they are not compatible with
IronPython.

# custom types in C
# python extension modules in C and through cython
# acceleration through numba JIT?
# acceleration through ?
"""

from compas.geometry.hpc.cvector import CVector
from compas.geometry.hpc.cpoint import CPoint

__all__ = ['CVector', 'CPoint']
