
    import pycuda.curandom
    import pycuda.gpuarray








def cuda_random(shape, bit=64):
    """ Create random values in the range [0, 1] as GPUArray.

    Parameters:
        shape (tuple): Size of the random array.
        bit (int): 32 or 64 for corresponding float precision.

    Returns:
        gpu: Random floats from 0 to 1 in GPUArray.

    Examples:
        >>> a = cuda_random((2, 2), bit=64)
        array([[ 0.80916596,  0.82687163],
               [ 0.03921388,  0.44197764]])
        >>> type(a)
        <class 'pycuda.gpuarray.GPUArray'>
    """
    if bit == 32:
        return pycuda.curandom.rand(shape, float32)
    elif bit == 64:
        return pycuda.curandom.rand(shape, float64)


def cuda_tile(a, shape):
    """ Horizontally and vertically tile a GPUArray.

    Notes:
        May be slow for large tiling shapes as For loops are used.

    Parameters:
        a (gpu): GPUArray to tile.
        shape (tuple): Number of vertical and horizontal tiles.

    Returns:
        gpu: Tiled GPUArray.

    Examples:
        >>> a = cuda_tile(cuda_give([[1, 2], [3, 4]]), (2, 2))
        array([[ 1.,  2.,  1.,  2.],
               [ 3.,  4.,  3.,  4.],
               [ 1.,  2.,  1.,  2.],
               [ 3.,  4.,  3.,  4.]])
        >>> type(a)
        <class 'pycuda.gpuarray.GPUArray'>

    """
    m, n = a.shape
    b = cuda_zeros((m * shape[0], n))
    for i in range(shape[0]):
        b[i * m:i * m + m, :] = a
    c = cuda_zeros((m * shape[0], n * shape[1]))
    for i in range(shape[1]):
        c[:, i * n:i * n + n] = b
    return c





# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    a = cuda_give([[1, 2, 3], [4, 5, 6]], bit=64, type='complex')
    b = cuda_ones((3, 2), bit=64)
    c = cuda_random((2, 2), bit=64)
    d = cuda_real(cuda_give([1 + 2.j, 2 - 4.j], type='complex'))
    e = cuda_zeros((3, 2), bit=64)

    h = cuda_tile(cuda_give([[1, 2], [3, 4]]), (2, 2))
    i = cuda_squeeze(cuda_give([[1], [2]]))
    j = cuda_imag(cuda_give([1 + 2.j, 2 - 4.j], bit=64, type='complex'))
