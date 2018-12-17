from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import sys
import array
import compas

from compas.utilities import flatten

try:
    from compas.numerical.alglib.core import Array
    from compas.numerical.alglib.core import Zeros
    from compas.numerical.alglib.core import xalglib

except ImportError:
    compas.raise_if_ironpython()


__all__ = ['SparseArray', 'SparseDiagonal']


class SparseArrayError(Exception):
    pass


class SparseArray(object):

    dtypes = {
        'f'    : float,
        'float': float,
        'i'    : int,
        'int'  : int
    }

    def __init__(self, ijk, shape, dtype='f'):
        self.__rows = None
        self.__cols = None
        self.__data = None
        self._data = None
        self._shape = None
        self._dtype = None
        self.shape = shape
        self.dtype = dtype
        self.data = ijk

    # ==========================================================================
    # descriptors
    # ==========================================================================

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, ijk):
        m, n = self.shape
        dtype = SparseArray.dtypes[self.dtype]
        rows, cols, data = ijk
        self.__rows = rows
        self.__cols = cols
        self.__data = data
        self._data = {i: {} for i in rows}
        for i, j, k in zip(rows, cols, data):
            if i >= m or j >= n:
                raise SparseArrayError('Data not compatible with shape.')
            self._data[i][j] = dtype(k)

    @property
    def matrix(self):
        m, n = self.shape
        M = xalglib.sparsecreate(m, n, len(self.__data))
        for i in self._data:
            for j in self._data[i]:
                k = self._data[i][j]
                xalglib.sparseset(M, i, j, k)
        xalglib.sparseconverttocrs(M)
        return M

    @property
    def dtype(self):
        return self._dtype

    @dtype.setter
    def dtype(self, dtype):
        if dtype not in SparseArray.dtypes:
            raise TypeError
        self._dtype = dtype

    @property
    def shape(self):
        return self._shape

    @shape.setter
    def shape(self, shape):
        m, n = shape
        self._shape = m, n

    # ==========================================================================
    # customisation
    # ==========================================================================

    def __str__(self):
        return str(self._data)

    def __getitem__(self, key):
        m, n = self.shape

        if isinstance(key, int):
            row = []
            if key >= m:
                raise KeyError
            for j in range(n):
                if key in self._data and j in self._data[key]:
                    row.append(self._data[key][j])
                else:
                    row.append(0.0)
            return row

        if isinstance(key, list):
            keys = key
            rows, cols, data = [], [], []
            for i, key in enumerate(keys):
                if key >= m:
                    raise KeyError
                if key in self._data:
                    for j in self._data[key]:
                        rows.append(i)
                        cols.append(j)
                        data.append(self._data[key][j])
            return SparseArray((rows, cols, data), (len(keys), n))

        if isinstance(key, slice):
            keys = range(* key.indices(m))
            return self[keys]

        if isinstance(key, tuple):
            i, j = key
            i_int = isinstance(i, int)
            j_int = isinstance(j, int)
            if i_int and j_int:
                if i in self._data and j in self._data[i]:
                    return self._data[i][j]
                return 0.0
            if i_int:
                return self[i][j]
            if j_int:
                return self[i].transpose()[j]
            return self[i].transpose()[j].transpose()

    def __setitem__(self, key, value):
        raise NotImplementedError

    # ==========================================================================
    # conversions
    # ==========================================================================

    def to_dense(self):
        m, n = self.shape
        data = []
        for i in range(m):
            for j in range(n):
                if i in self._data and j in self._data[i]:
                    data.append(self._data[i][j])
                else:
                    data.append(0.0)
        return Array(data, (m, n))

    def to_csc(self):
        pass

    # ==========================================================================
    # linalg
    # ==========================================================================

    def diagonal(self):
        m, n = self.shape
        if m <= n:
            return [self[i, i] for i in range(m)]
        return [self[i, i] for i in range(n)]

    def transpose(self):
        m, n = self.shape
        rows, cols, data = [], [], []
        for i in self._data:
            for j in self._data[i]:
                k = self._data[i][j]
                rows.append(j)
                cols.append(i)
                data.append(k)
        return SparseArray((rows, cols, data), (n, m))

    def _dot(self, other):
        A = self
        B = other.transpose()
        m, n = A.shape
        k, n = B.shape
        shape = m, k
        rows, cols, data = [], [], []
        Arows = {i: set(A._data[i]) for i in A._data}
        Bcols = {j: set(B._data[j]) for j in B._data}
        for i, setrow in iter(Arows.items()):
            for j, setcol in iter(Bcols.items()):
                keys = setrow & setcol
                if keys:
                    value = sum(A._data[i][key] * B._data[j][key] for key in keys)
                    rows.append(i)
                    cols.append(j)
                    data.append(value)
        return SparseArray((rows, cols, data), shape)

    def _tdot(self, other):
        A = self.transpose()
        B = other
        return A._dot(B)

    def dot(self, other):
        if isinstance(other, Array):
            m, n = self.shape
            n, k = other.shape
            A = self.matrix
            b = other.data
            data = xalglib.sparsemm(A, b, k, Zeros((m, k)).data)
            return Array(data, (m, k))
        return self._dot(other)

    def tdot(self, other):
        if isinstance(other, Array):
            m, n = self.shape
            n, k = other.shape
            A = self.matrix
            b = other.data
            data = xalglib.sparsemtm(A, b, k, Zeros((n, k)).data)
            return Array(data, (n, k))
        return self._tdot(other)

    def xdot(self, B, C, a=1.0, c=1.0):
        raise NotImplementedError


# ==============================================================================
# Special
# ==============================================================================


class SparseDiagonal(SparseArray):

    def __init__(self, data, dtype='f'):
        m = len(data)
        rows = range(m)
        super(SparseDiagonal, self).__init__((rows, rows, data), (m, m), dtype)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    import compas
    from compas.datastructures import Network

    network = Network.from_obj(compas.get('lines.obj'))

    e = network.number_of_edges()
    v = network.number_of_vertices()

    vertices = network.get_vertices_attributes('xyz')
    edges = list(network.edges())

    xyz = Array(vertices, (v, 3))

    shape = e, v

    rows, cols, data = [], [], []

    for i, (u, v) in enumerate(edges):
        rows.append(i)
        rows.append(i)
        cols.append(u)
        cols.append(v)
        data.append(-1)
        data.append(+1)

    C = SparseArray((rows, cols, data), shape)

    print(C.transpose()._dot(C).diagonal())
    print(C.transpose().dot(C).diagonal())
    print(C.tdot(C).diagonal())

    # print(C[:, 0])
    # print(Ct[0, :])

    # print(C[:, [0, 1, 2]])
    # print(Ct[[0, 1, 2], :])

    # print(C[0])
    # print(C[[0, 1, 2]])
    # print(C[0:3])
    # print(C.to_dense())
    # print(Ct.to_dense())

    # uvw = C.dot(xyz)

    # print(uvw)
