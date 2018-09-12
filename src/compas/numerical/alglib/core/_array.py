from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import sys
import array
import compas

from compas.utilities import flatten

try:
    from compas.numerical.alglib.core import xalglib

except ImportError:
    compas.raise_if_ironpython()


__all__ = ['Array', 'Zeros', 'Ones', 'Diagonal', 'Eye', 'ZerosLike']


class ArrayError(Exception):
    pass


class Array(object):
    """"""

    dtypes = {
        'i'    : 'i',
        'int'  : 'i',
        'f'    : 'f',
        'float': 'f',
    }

    __slots__ = ['_data', '_dtype', '_shape']

    def __init__(self, data, shape, dtype=None):
        self._data = None
        self._dtype = None
        self._shape = None
        self.dtype = dtype
        self.data = data
        self.shape = shape

    @property
    def dtype(self):
        return self._dtype

    @dtype.setter
    def dtype(self, dtype):
        if not dtype:
            dtype = 'float'
        dtype = str(dtype)
        if dtype not in Array.dtypes:
            raise ArrayError('Data type not supported.')
        self._dtype = Array.dtypes[dtype]

    @property
    def data(self):
        m, n = self.shape
        data = self._data.tolist()
        if not n:
            return data
        return [data[i * n: (i + 1) * n] for i in range(m)]

    @data.setter
    def data(self, data):
        if isinstance(data, array.array):
            self._data = data
        else:
            self._data = array.array(self.dtype)

            if isinstance(data[0], (array.array, list, tuple)):
                data = list(flatten(data))

            self._data.fromlist(list(data))

    @property
    def flatdata(self):
        return self._data.tolist()

    @property
    def size(self):
        """"""
        return len(self._data)

    @property
    def shape(self):
        """"""
        return self._shape

    @shape.setter
    def shape(self, shape):
        m, n = shape
        if not n:
            n = 1
        if m * n != self.size:
            raise ArrayError('Size and shape are not compatible.')
        self._shape = shape

    @property
    def rows(self):
        m, n = self.shape
        data = self._data.tolist()
        if not n:
            return data
        return [data[i * n: (i + 1) * n] for i in range(m)]

    @property
    def cols(self):
        m, n = self.shape
        data = self._data.tolist()
        if not n:
            return data
        return [[data[i + j * n] for j in range(m)] for i in range(n)]

    # ==========================================================================
    # customisation
    # ==========================================================================

    def __len__(self):
        return self.shape[0]

    def __str__(self):
        return "Array({})".format(self.data)

    def __iter__(self):
        return iter(self.rows)

    # ==========================================================================
    # access
    # ==========================================================================

    def __getitem__(self, key):
        m, n = self.shape

        if isinstance(key, int):
            if key > m - 1:
                raise KeyError
            if not n:
                return self._data[m]
            return Array(self._data[key * n: (key + 1) * n], (n, None), self.dtype)

        if isinstance(key, list):
            if not n:
                data = [self._data[i] for i in key]
            else:
                data = [self._data[i * n: (i + 1) * n] for i in key]
            return Array(data, (len(key), n), self.dtype)

        if isinstance(key, slice):
            keys = list(range(* key.indices(m)))
            return self[keys]

        if isinstance(key, tuple):
            i, j = key
            i_int = isinstance(i, int)
            j_int = isinstance(j, int)
            if i_int and j_int:
                return self._data[i * n + j]
            if i_int:
                return self[i][j]
            if j_int:
                return self[i].transpose()[j]
            return self[i].transpose()[j].transpose()

        raise KeyError

    # ==========================================================================
    # modification
    # ==========================================================================

    def __setitem__(self, key, value):
        m, n = self.shape

        if not n:
            n = 1

        if isinstance(key, int):
            if n == 1:
                self._data[key] = value
            else:
                if key >= m:
                    raise KeyError
                if isinstance(value, Array):
                    a, b = value.shape
                    if b and b > 1:
                        raise ValueError
                    if a != n:
                        raise ValueError
                    for i, v in enumerate(value._data):
                        self._data[key * n + i] = v
                else:
                    if len(value) != n:
                        raise ValueError
                    for i, v in enumerate(value):
                        self._data[key * n + i] = v

        elif isinstance(key, list):
            for i, k in enumerate(key):
                self[k] = value[i]

        elif isinstance(key, slice):
            keys = list(range(* key.indices(m)))
            self[keys] = value

        elif isinstance(key, tuple):
            i, j = key
            i_int = isinstance(i, int)
            j_int = isinstance(j, int)
            if i_int and j_int:
                if i >= m or j >= n:
                    raise KeyError
                self._data[i * n + j] = value

            elif i_int:
                if isinstance(j , slice):
                    j = list(range(* j.indices(m)))
                if len(j) != len(value):
                    raise ValueError(
                        "Sizes of row slice and replacement values don't match: {} != {}".format(len(j), len(value)))
                for index, data in zip(j, value):
                    self._data[i * n + index] = data

            elif j_int:
                if isinstance(i , slice):
                    i = list(range(* i.indices(m)))
                if len(i) != len(value):
                    raise ValueError(
                        "Sizes of column slice and replacement values don't match: {} != {}".format(len(i), len(value)))
                for index, data in zip(i, value):
                    self._data[index * n + j] = data

            else:
                raise NotImplementedError

        else:
            raise KeyError

    # ==========================================================================
    # helpers
    # ==========================================================================

    # rename to "flatdata"
    def flatten(self):
        return self._data.tolist()

    def transpose(self):
        m, n = self.shape
        if not n:
            n = 1
        return Array([self._data[i + j * n] for i in range(n) for j in range(m)], (n, m), self.dtype)

    # ==========================================================================
    # linalg
    # ==========================================================================

    def add(self, other):
        m, n = self.shape
        o, p = other.shape
        if m != o or n != p:
            raise ArrayError('Incompatible matrix dimensions.')
        data = [a + b for a, b in zip(self._data, other._data)]
        return Array(data, (m, n), dtype=self.dtype)

    def subtract(self, other):
        m, n = self.shape
        o, p = other.shape
        if m != o or n != p:
            raise ArrayError('Incompatible matrix dimensions.')
        data = [a - b for a, b in zip(self._data, other._data)]
        return Array(data, (m, n), dtype=self.dtype)

    def multiply(self, factor):
        pass

    def emultiply(self, other):
        pass

    def _dot(self, other):
        a, b = self.shape
        c, d = other.shape
        if b != c:
            raise ArrayError('Incompatible shapes for dot product.')

        rows = self.rows
        cols = other.cols
        m, n = a, d
        data = [None] * (m * n)
        for i in range(m):
            for j in range(n):
                data[i * n + j] = sum(x * y for x, y in zip(rows[i], cols[j]))
        return Array(data, (m, n), self.dtype)

    def dot(self, other):
        try:
            xalglib
        except NameError:
            return self._dot(other)

        m, k = self.shape
        k, n = other.shape

        data = xalglib.rmatrixgemm(
            m, n, k,
            1.0, self.data, 0, 0, 0,
            other.data, 0, 0, 0,
            0, Zeros((m, n)).data, 0, 0
        )
        return Array(data, (m, n), self.dtype)

    def tdot(self, other):
        try:
            xalglib
        except NameError:
            return self.transpose()._dot(other)

        k, m = self.shape
        k, n = other.shape

        data = xalglib.rmatrixgemm(
            m, n, k,
            1.0, self.data, 0, 0, 1,
            other.data, 0, 0, 0,
            0, Zeros((m, n)).data, 0, 0
        )
        return Array(data, (m, n), self.dtype)

    def xdot(self, B, C, a=1.0, c=1.0):
        A = self
        try:
            xalglib
        except NameError:
            return A.multiply(a)._dot(B).add(C.multiply(c))

        m, k = A.shape
        k, n = B.shape

        data = xalglib.rmatrixgemm(
            m, n, k,
            a, A.data, 0, 0, 0,
            B.data, 0, 0, 0,
            c, C.data, 0, 0
        )

        return Array(data, (m, n), self.dtype)


# ==============================================================================
# Special
# ==============================================================================


class Zeros(Array):

    def __init__(self, shape, dtype='f'):
        m, n = shape
        if not n:
            n = 1
        data = [0.0] * (m * n)
        super(Zeros, self).__init__(data, shape, dtype)


class Ones(Array):

    def __init__(self, shape, dtype='f'):
        m, n = shape
        if not n:
            n = 1
        data = [1.0] * (m * n)
        super(Ones, self).__init__(data, shape, dtype)


class Diagonal(Zeros):

    def __init__(self, data, dtype='f'):
        m = len(data)
        super(Diagonal, self).__init__((m, m), dtype)
        for i in range(m):
            self._data[i * (m + 1)] = data[i]


class Eye(Diagonal):

    def __init__(self, shape, dtype='f'):
        data = [1.0] * shape
        super(Eye, self).__init__(data, dtype)


class ZerosLike(Array):

    def __init__(self, array):
        m, n = array.shape
        data = [0.0] * (m * n)
        super(ZerosLike, self).__init__(data, array.shape, array.dtype)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    data = range(9)

    a = Array(data, (3, 3), dtype='i')

    for row in a:
        print(row)

    print(a)
    print(a[0, :])
    print(a[:, 0])

    print(a[[0, 1]])
    print(a[:, [0, 1]])

    a[[1, 2], 0] = [1, 1]
    print(a)