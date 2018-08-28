from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import ctypes

from ctypes import c_int
from ctypes import c_float
from ctypes import c_double
from ctypes import POINTER
from ctypes import CFUNCTYPE


__all__ = [
    'Array1D', 'Array2D', 'Array3D', 'shape', 'zeros', 'ones', 'eye'
]


# ==============================================================================
# oo interface
# ==============================================================================


class Array1D(object):
    """"""

    def __init__(self, data, dtype):
        self._data = data
        self._dtype = dtype
        self._cdata = self.__array()

    @property
    def data(self):
        return self._data

    @property
    def cdata(self):
        return self._cdata

    @property
    def pydata(self):
        return list(self.cdata)

    @property
    def dtype(self):
        return self._dtype

    @property
    def shape(self):
        m = len(self.data)
        return m

    @property
    def ctype(self):
        m = self.shape
        if self.dtype == 'int':
            return c_int * m
        if self.dtype == 'float':
            return c_float * m
        if self.dtype == 'double':
            return c_double * m
        raise NotImplementedError

    def __array(self):
        data = self.data
        array = self.ctype
        return array(*data)


class Array2D(object):
    """"""

    def __init__(self, data, dtype):
        self._data = data
        self._dtype = dtype
        self._cdata = self.__array()

    @property
    def data(self):
        return self._data

    @property
    def cdata(self):
        return self._cdata

    @property
    def pydata(self):
        m, n = self.shape
        data = [[self.cdata[i][j] for j in range(n)] for i in range(m)]
        return data

    @property
    def dtype(self):
        return self._dtype

    @property
    def shape(self):
        data = self.data
        m, n = len(data), len(data[0])
        assert all(len(row) == n for row in data), 'The specified shape does not match the provided data.'
        return m, n

    @property
    def ctype(self):
        m, n = self.shape
        if self.dtype == 'int':
            return POINTER(c_int) * m
        if self.dtype == 'float':
            return POINTER(c_float) * m
        if self.dtype == 'double':
            return POINTER(c_double) * m
        raise NotImplementedError

    def __array(self):
        m, n = self.shape
        array = self.ctype(*[Array1D(self.data[i], self.dtype).cdata for i in range(m)])
        return array


class Array3D(object):
    """"""

    def __init__(self, data, dtype):
        self._data = data
        self._dtype = dtype
        self._cdata = self.__array()

    @property
    def data(self):
        return self._data

    @property
    def cdata(self):
        return self._cdata

    @property
    def pydata(self):
        m, n, o = self.shape
        data = [[[self.cdata[i][j][k] for k in range(o)] for j in range(n)] for i in range(m)]
        return data

    @property
    def dtype(self):
        return self._dtype

    @property
    def shape(self):
        data = self.data
        m, n, o = len(data), len(data[0]), len(data[0][0])
        assert all(len(row) == n for row in data), 'The specified shape does not match the provided data.'
        for row in data:
            assert all(len(col) == o for col in row), 'The specified shape does not match the provided data.'
        return m, n, o

    @property
    def ctype(self):
        m, n, o = self.shape
        if self.dtype == 'int':
            return POINTER(POINTER(c_int)) * m
        if self.dtype == 'float':
            return POINTER(POINTER(c_float)) * m
        if self.dtype == 'double':
            return POINTER(POINTER(c_double)) * m
        raise NotImplementedError

    def __array(self):
        m, n, o = self.shape
        if self.dtype == 'int':
            row = POINTER(c_int) * n
            col = c_int * o
        elif self.dtype == 'float':
            row = POINTER(c_float) * n
            col = c_float * o
        elif self.dtype == 'double':
            row = POINTER(c_double) * n
            col = c_double * o
        else:
            raise NotImplementedError
        a = self.ctype()
        for i in range(m):
            a[i] = row()
            for j in range(n):
                a[i][j] = col()
                for k in range(o):
                    a[i][j][k] = self.data[i][j][k]
        return a


# ==============================================================================
# functional interface
# ==============================================================================


def shape(data):
    m, n = len(data), len(data[0])
    assert len(data) == m, 'The specified shape does not match the provided data.'
    assert all(len(row) == n for row in data), 'The specified shape does not match the provided data.'
    return m, n


def zeros():
    pass


def ones():
    pass


def eye():
    pass


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import time

    try:
        lib = ctypes.cdll.LoadLibrary('_test/test.so')
    except (WindowsError, OSError, ImportError):
        lib = ctypes.windll.LoadLibrary('_test/test.dll')

    vectors = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0], [1.0, 1.0, 1.0]]

    m = len(vectors)

    lengths = [0.0 for _ in range(m)]

    def callback(i, l):
        print("Calling back about vector {}: length = {}".format(i, l))
        time.sleep(0.1)

    c_vectors  = Array2D(vectors, 'double')
    c_lengths  = Array1D(lengths, 'double')
    c_callback = CFUNCTYPE(None, c_int, c_double)

    lib.length.argtypes = [c_int, c_vectors.ctype, c_lengths.ctype, c_callback]
    lib.length(c_int(m), c_vectors.cdata, c_lengths.cdata, c_callback(callback))

    print(c_lengths.pydata)
