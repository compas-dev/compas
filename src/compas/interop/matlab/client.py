from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas
if compas.IPY:
    import System


class MatlabClient(object):
    """Communicate with Matlab through Windows' COM interface.

    Parameters
    ----------
    verbose : bool, optional
        If True, all commands and results will be printed in the Python console.
    interactive : bool, optional
        If True, a Matlab console window will be visible.
    workspace : str, optional
        The name of the Matlab workspace.

    Notes
    -----
    This implementation uses Windows' COM interface to communicate with Matlab.
    Therefore, it is obviously only available on Windows.
    When an instance of this class is created, it automatically connects to Matlab,
    and initializes a lease that keeps the interface alive for at least 5 minutes
    such that subsequent calls can be executed immediately.
    After every call, the lease is renewed...

    Examples
    --------
    >>> matlab = MatlabClient(interactive=True)
    >>> A = matlab.matrix_from_list([[1, 0, 1, 3], [2, 3, 4, 7], [-1, -3, -3, -4]])
    >>> matlab.put('A', A)
    >>> matlab.eval('[R, jb] = rref(A);')
    >>> R = matlab.get('R')
    >>> jb = matlab.get('jb')
    >>> print(R)
    >>> print(jb)

    """

    def __init__(self, verbose=False, interactive=False, workspace='base'):
        self._type = None
        self._app = None
        self._lease = None
        self.verbose = verbose
        self.interactive = interactive
        self.workspace = workspace
        self.init()

    def init(self):
        self._create_instance()
        self._init_lease()

    def _create_instance(self):
        self._type = System.Type.GetTypeFromProgID('Matlab.Application')
        self._app = System.Activator.CreateInstance(self._type)
        self._app.Visible = self.interactive

    def _init_lease(self):
        self._lease = self._app.InitializeLifetimeService()
        self._lease.InitialLeaseTime = System.TimeSpan.FromMinutes(5.0)
        self._lease.RenewOnCallTime = System.TimeSpan.FromMinutes(5.0)

    def _renew_lease(self):
        self._lease.Renew(System.TimeSpan.FromMinutes(5.0))

    def _get_vector(self, name):
        _value = self._app.GetVariable(name, self.workspace)
        try:
            _value.Rank
        except AttributeError:
            value = _value
        else:
            value = MatlabClient.list_from_vector(_value)
        self._renew_lease()
        return value

    def _get_matrix_size(self, name):
        self._app.Execute('[m, n] = size({0});'.format(name))
        m = self._app.GetVariable('m', self.workspace)
        n = self._app.GetVariable('n', self.workspace)
        return int(m), int(n)

    # ==========================================================================
    # static methods
    # ==========================================================================

    @staticmethod
    def vector_from_list(a, dtype=float):
        """Make a Matlab-compatible vector from a list.

        Parameters
        ----------
        a : sequence[int or float]
            The input list.
        dtype : {int, float}, optional
            The constructor function of the data type.

        Returns
        -------
        System.Array
            The vector.

        Examples
        --------
        >>> vector = MatlabClient.vector_from_list([1, 2, 3], dtype=float)

        """
        n = len(a)
        vector = System.Array.CreateInstance(dtype, n)
        for i in range(n):
            vector[i] = a[i]
        return vector

    @staticmethod
    def vector_from_array(a):
        """Make a Matlab-compatible vector from a (Numpy) array.

        Parameters
        ----------
        a : ndarray
            The input array.

        Returns
        -------
        System.Array
            The vector.

        """
        raise NotImplementedError

    @staticmethod
    def matrix_from_list(A, dtype=float):
        """Make a Matlab-compatible matrix from a list of lists.

        Parameters
        ----------
        A : sequence[sequence[int or float]]
            The input list.
        dtype : {int or float}, optional
            The data type constructor function.

        Returns
        -------
        System.Array
            The matrix.

        """
        m = len(A)
        n = len(A[0])
        if not all([len(row) == n for row in A]):
            raise Exception('Matrix dimensions inconsistent.')
        matrix = System.Array.CreateInstance(dtype, m, n)
        for row in range(m):
            for col in range(n):
                matrix[row, col] = A[row][col]
        return matrix

    @staticmethod
    def matrix_from_array(a):
        """Make a Matlab-compatible matrix from a (Numpy) array.

        Parameters
        ----------
        a : ndarray
            The input array.

        Returns
        -------
        System.Array
            The matrix.

        """
        raise NotImplementedError

    @staticmethod
    def list_from_vector(a):
        """Convert a Matlab vector to a Python list.

        Parameters
        ----------
        a : System.Array
            The Matlab vector.

        Returns
        -------
        list
            The vector converted to a list.

        """
        return list(a)

    @staticmethod
    def list_from_matrix(A, m, n):
        """Convert a Matlab matrix to a Python list.

        Parameters
        ----------
        A : System.Array
            The matlab vector.
        m : int
            The number of rows of the matrix.
        n : int
            The number of columns of the matrix.

        Returns
        -------
        list[list[int or float]]
            The matrix converted to a nested list.

        """
        nlist = []
        for row in range(m):
            nlist.append([None] * n)
            for col in range(n):
                nlist[row][col] = A[row, col]
        return nlist

    @staticmethod
    def double(a):
        """Convert a Matlab vector or matrix to a Python list or nested list of floats.

        Parameters
        ----------
        a : System.Array
            The Matlab vector or matrix.

        Returns
        -------
        list[float] or list[list[float]]
            A list of float or a nested list of float, depending on the input.

        """
        try:
            len(a[0])
        except TypeError:
            return MatlabClient.vector_from_list(a, dtype=float)
        else:
            return MatlabClient.matrix_from_list(a, dtype=float)

    # ==========================================================================
    # methods
    # ==========================================================================

    def eval(self, cmd):
        """Evaluate a command from a string.

        Parameters
        ----------
        cmd : str
            The command string.

        Returns
        -------
        None

        Examples
        --------
        >>> matlab = MatlabClient(verbose=True)
        >>> matlab.eval('isprime(13);')
        True

        """
        res = self._app.Execute(cmd)
        if self.verbose:
            print(res)
        self._renew_lease()

    def put(self, name, value):
        """Put a variable in the Matlab workspace.

        Parameters
        ----------
        name : str
            The name of the variable.
        value : str or int or float or list[int or float] or list[list[int or float]]
            The value of the variable.

        Returns
        -------
        None

        Examples
        --------
        >>> m = MatlabClient(verbose=True, interactive=True)
        >>> m.put('A', m.matrix([[1, 0, 1, 3], [2, 3, 4, 7], [-1, -3, -3, -4]]))

        """
        try:
            res = self._app.PutFullMatrix(name, self.workspace, value, None)
        except Exception:
            res = self._app.PutWorkspaceData(name, self.workspace, value)
        if self.verbose:
            print(res)
        self._renew_lease()

    def get(self, name):
        """Get the value of a variable in the workspace.

        Parameters
        ----------
        name : str
            The name of the variable.

        Returns
        -------
        str or int or float or list[int or float] or list[list[int or float]]
            The value of the variable.

        Examples
        --------
        >>> m = MatlabClient(verbose=True)
        >>> m.get('A')
        [[1, 0, 1, 3], [2, 3, 4, 7], [-1, -3, -3, -4]]

        """
        _value = self._app.GetVariable(name, self.workspace)
        try:
            _value.Rank
        except AttributeError:
            value = _value
        else:
            value = []
            if _value.Rank == 1:
                value = MatlabClient.list_from_vector(_value)
            elif _value.Rank == 2:
                m, n = self._get_matrix_size(name)
                value = MatlabClient.list_from_matrix(_value, m, n)
        self._renew_lease()
        return value
