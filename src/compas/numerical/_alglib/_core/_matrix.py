from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


__all__ = ['Matrix']


class MatrixError(Exception):
    pass


class Matrix(object):
    """"""

    dtypes = {
        'i'    : int,
        'int'  : int,
        'f'    : float,
        'float': float,
    }

    __slots__ = ['_data', '_dtype']

    def __init__(self, data, dtype=None):
        self._data = None
        self._dtype = None
        self.dtype = dtype
        self.data = data

    @property
    def data(self):
        """"""
        return self._data

    @data.setter
    def data(self, data):
        self._data = []

        dtype = self.dtypes[self.dtype]

        if isinstance(data, list):
            cols = None

            for row in data:
                if isinstance(row, (list, tuple)):
                    if not cols:
                        cols = len(row)
                    if len(row) != cols:
                        raise MatrixError('The shape of the data is not rectangular.')
                    self._data.append([dtype(value) for value in row])
                else:
                    raise MatrixError('The data is not two-dimensional.')

    @property
    def dtype(self):
        """"""
        return self._dtype

    @dtype.setter
    def dtype(self, dtype):
        if not dtype:
            dtype = 'float'
        dtype = str(dtype)
        if dtype not in Matrix.dtypes:
            raise MatrixError('Data type not supported.')
        self._dtype = dtype

    @property
    def shape(self):
        """"""
        return len(self._data), len(self._data[0])

    @property
    def size(self):
        """"""
        m, n = self.shape
        return m * n

    def __str__(self):
        """"""
        return "Matrix({})".format(self._data)

    def __getitem__(self, key):
        """"""
        if isinstance(key, slice):
            return Matrix([self._data[i] for i in range(* key.indices(self.shape[0]))])

        if isinstance(key, list):
            return Matrix([self._data[i] for i in key])

        if isinstance(key, int):
            return Matrix([self._data[key]])

        if isinstance(key, tuple):
            i, j = key
            if isinstance(i, int) and isinstance(j, int):
                return self._data[i][j]
            return self[key[0]].transpose()[key[1]].transpose()

        raise KeyError

    def transpose(self):
        """"""
        return Matrix(zip(*self._data))

    def to_list(self):
        """"""
        pass

    def to_array(self):
        """"""
        pass

    def reshape(self, shape, order):
        """"""
        pass


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    m = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

    print(m[0])
    print(m[0, 1])
    print(m[[0, 1]])
    print(m[0:2])
    print(m[0, 0:2])
    print(m[0:2, 0])
    print(m[0:2, 0:2])
