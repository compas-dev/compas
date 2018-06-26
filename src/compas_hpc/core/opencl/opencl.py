
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

try:
    from numpy import array
    from numpy import float32
    from numpy import complex64
except:
    pass

try:
    import pyopencl as cl
    import pyopencl.array as cl_array
    import pyopencl.clrandom
except:
    pass


__author__    = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__ = 'Copyright 2018, BLOCK Research Group - ETH Zurich'
__license__   = 'MIT License'
__email__     = 'liew@arch.ethz.ch'


__all__ = [
    'rand_cl',
    'give_cl',
    'get_cl',
    'ones_cl',
    'zeros_cl',
    # 'tile_cl',
    # 'hstack_cl',
    'vstack_cl',
]


def rand_cl(queue, shape):

    """ Create random values in the range [0, 1] as GPUArray.

    Parameters
    ----------
    queue
        PyOpenCL queue.
    shape : tuple
        Size of the random array.

    Returns
    -------
    gpuarray
        Random floats from 0 to 1 in GPUArray.

    """

    return pyopencl.clrandom.rand(queue, shape, dtype=float32)


def give_cl(queue, a, type='real'):

    """ Give a list or an array to GPU memory.

    Parameters
    ----------
    queue
        PyOpenCL queue.
    a : array, list
        Data to send to the GPU memory.
    type : str
        'real' or 'complex'.

    Returns
    -------
    gpuarray
        GPUArray of the input array.

    """

    if type == 'real':
        return cl_array.to_device(queue, array(a, dtype=float32))
    elif type == 'complex':
        pass
        # return cl_array.to_device(queue, array(a, dtype=complex64))


def get_cl(a):

    """ Get back GPUArray from GPU memory as NumPy array.

    Parameters
    ----------
    a : gpuarray
        Data on the GPU memory to retrieve.

    Returns
    -------
    array
        The GPUArray returned to RAM as NumPy array.

    """

    return a.get()


def ones_cl(queue, shape):

    """ Create GPUArray of ones directly on GPU memory.

    Parameters
    ----------
    queue
        PyOpenCL queue.
    shape : tuple
        Dimensions of the GPUArray.

    Returns
    -------
    gpuarray
        GPUArray of ones.

    """

    a = cl_array.zeros(queue, shape, dtype=float32)
    a.fill(1.0)
    return a


def zeros_cl(queue, shape):

    """ Create GPUArray of zeros directly on GPU memory.

    Parameters
    ----------
    queue
        PyOpenCL queue.
    shape : tuple
        Dimensions of the GPUArray.

    Returns
    -------
    gpuarray
        GPUArray of zeros.

    """

    return cl_array.zeros(queue, shape, dtype=float32)


# def hstack_cl(a):

#     """ Horizontally stack GPUArrays.

#     Parameters
#     ----------
#     a : list
#         List of GPUArrays.

#     Returns
#     -------
#     gpuarray
#         Horizontally stack GPUArrays.

#     """

#     return cl_array.concatenate(a, axis=1)


def vstack_cl(a):

    """ Vertically stack GPUArrays.

    Parameters
    ----------
    a : list
        List of GPUArrays.

    Returns
    -------
    gpuarray
        Vertically stack GPUArrays.

    """

    return cl_array.concatenate(a, axis=0)


def tile_cl():
    raise NotImplementedError


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    ctx = cl.create_some_context()
    queue = cl.CommandQueue(ctx)

    a_ = give_cl(queue, [0, 1, 2])
    b_ = give_cl(queue, [3, 4, 5])
    c_ = a_ + b_
    d_ = a_ - b_
    e_ = a_ * b_
    f_ = a_ / b_
    g_ = a_**3
    z_ = ones_cl(queue, (2, 2))
    o_ = zeros_cl(queue, (2, 2))
    # h_ = vstack_cl([z_, o_, z_])
    # g_ = hstack_cl([z_, o_, z_])

    print(get_cl(z_))
    print(get_cl(o_))
    print(get_cl(c_))
    print(get_cl(d_))
    print(get_cl(e_))
    print(get_cl(f_))
    print(get_cl(g_))
    print(get_cl(e_ > c_))
    # print(get_cl(h_))
    # print(get_cl(g_))
    print(get_cl(rand_cl(queue, (2, 2))))

# ==============================================================================

    # ctx = cl.create_some_context()
    # queue = cl.CommandQueue(ctx)

    # a_ = give_cl(queue, [0, 1, 2])
    # b_ = give_cl(queue, [3, 4, 5])
    # c_ = cl_array.empty_like(a_)

    # prg = cl.Program(ctx, """

    # __kernel void sum(__global const float *a,

    # __global const float *b, __global float *c)
    #     {
    #         int gid = get_global_id(0);

    #         c[gid] = a[gid] + b[gid];
    #     }
    # """).build()

    # prg.sum(queue, a_.shape, None, a_.data, b_.data, c_.data)

    # print((c_).get())

# ==============================================================================

    # from numpy import empty
    # from numpy import int32

    # demo_r = empty((3, 5), dtype=int32)
    # ctx = cl.create_some_context()
    # queue = cl.CommandQueue(ctx)

    # mf = cl.mem_flags
    # demo_buf = cl.Buffer(ctx, mf.WRITE_ONLY, demo_r.nbytes)

    # prg = cl.Program(ctx,
    # """
    # __kernel void demo(__global uint *demo)
    # {
    #     int i;
    #     int gid = get_global_id(0);

    #     for(i = 0; i < 5; i++)
    #     {
    #         demo[gid*5+i] = i;
    #     }
    # }""")

    # prg.build()
    # prg.demo(queue, (3,), None, demo_buf)
    # cl.enqueue_read_buffer(queue, demo_buf, demo_r).wait()

    # for res in demo_r:
    #     print(res)


# ====================================================================================

    # from __future__ import absolute_import
    # from __future__ import print_function
    # #!/usr/bin/env python
    # # -*- coding: utf-8 -*-

    # import numpy as np
    # import pyopencl as cl
    # import pyopencl.array
    # from pyopencl.elementwise import ElementwiseKernel

    # n = 10
    # a_np = np.random.randn(n).astype(np.float32)
    # b_np = np.random.randn(n).astype(np.float32)

    # ctx = cl.create_some_context()
    # queue = cl.CommandQueue(ctx)

    # a_g = cl.array.to_device(queue, a_np)
    # b_g = cl.array.to_device(queue, b_np)

    # lin_comb = ElementwiseKernel(ctx,
    #     "float k1, float *a_g, float k2, float *b_g, float *res_g",
    #     "res_g[i] = k1 * a_g[i] + k2 * b_g[i]",
    #     "lin_comb"
    # )

    # res_g = cl.array.empty_like(a_g)
    # lin_comb(2, a_g, 3, b_g, res_g)

    # # Check on GPU with PyOpenCL Array:
    # print((res_g - (2 * a_g + 3 * b_g)).get())

    # # Check on CPU with Numpy:
    # res_np = res_g.get()
    # print(res_np - (2 * a_np + 3 * b_np))
    # print(np.linalg.norm(res_np - (2 * a_np + 3 * b_np)))
