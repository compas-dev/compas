from __future__ import print_function

from numpy import asarray

import pyopencl as cl
import pyopencl.array as cl_array


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = [
    'opencl_cross',
]


def opencl_cross(a, b):
    a     = asarray(a, dtype=float)
    b     = asarray(b, dtype=float)
    ctx   = cl.create_some_context()
    queue = cl.CommandQueue(ctx)
    a_dev = cl_array.to_device(queue, a)
    b_dev = cl_array.to_device(queue, b)
    c_dev = cl_array.empty_like(a_dev)
    code  = """
    __kernel void crossproduct(__global const float *a, __global const float *b, __global float *c)
    {
        int i = get_global_id(0);

        __global const float * a_ = &a[i * 3];
        __global const float * b_ = &b[i * 3];
        __global float * c_ = &c[i * 3];

        c_[0] = a_[1] * b_[2] - a_[2] * b_[1];
        c_[1] = a_[2] * b_[0] - a_[0] * b_[2];
        c_[2] = a_[0] * b_[1] - a_[1] * b_[0];
    }
    """
    prg = cl.Program(ctx, code).build()
    prg.crossproduct(queue, a.shape, None, a_dev.data, b_dev.data, c_dev.data)
    return c_dev.get()


# ==============================================================================
# Testing
# ==============================================================================

if __name__ == '__main__':

    a = [(1, 0, 0), (1, 0, 0), (1, 0, 0)]
    b = [(0, 1, 0), (0, 0, 1), (1, 0, 0)]

    print(opencl_cross(a, b))
