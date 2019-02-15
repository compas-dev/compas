from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


__all__ = ['MatlabEngine']


class MatlabEngineError(Exception):

    def __init__(self, message=None):
        if not message:
            message = """
Could not start the Matlab engine.
Note that the Matlab engine is only available since R2014b.
Python 3 is only supported since R2017b...
For older versions of Matlab, use *MatlabProcess* instead.
On Windows, *MatlabClient* is also available.
See <https://ch.mathworks.com/help/matlab/matlab-engine-for-python.html?s_tid=gn_loc_drop> for instructions.
"""
        super(MatlabEngineError, self).__init__(message)


class MatlabEngine(object):
    """Communicate with Matlab through the MATLAB engine.

    Attributes
    ----------
    session_name : str
        The name of the current Matlab session.

    Notes
    -----
    For more info, see [1]_, [2]_, [3]_, [4]_, [5]_.

    References
    ----------
    .. [1] MathWorks, 2017. *MATLAB APY for Python*.
           Available at: https://ch.mathworks.com/help/matlab/matlab-engine-for-python.html
    .. [2] MathWorks, 2017. *Pass Data to MATLAB from Python*.
           Available at: https://ch.mathworks.com/help/matlab/matlab_external/pass-data-to-matlab-from-python.
    .. [3] MathWorks, 2017. *Use MATLAB Arrays in Python*.
           Available at: https://ch.mathworks.com/help/matlab/matlab_external/use-matlab-arrays-in-python.html
    .. [4] MathWorks, 2017. *Use MATLAB Engine Workspace in Python*.
           Available at: https://ch.mathworks.com/help/matlab/matlab_external/use-the-matlab-engine-workspace-in-python.html
    .. [5] MathWorks, 2017. *Call MATLAB Functions from Python*.
           Available at: https://ch.mathworks.com/help/matlab/matlab_external/call-matlab-functions-from-python.html

    Examples
    --------
    >>> matlab = MatlabEngine()
    >>> matlab.engine.isprime(37)
    True

    """

    def __init__(self):
        self._matlab = None
        self._engine = None
        self.engine  = None
        self.session_name = None
        self._init()

    def _init(self):
        """Load the Matlab API.

        Raises
        ------
        MatlabEngineError
            If the matlab API package can't be imported.

        """
        try:
            import matlab
            import matlab.engine
        except ImportError:
            raise MatlabEngineError()
        self._matlab = matlab
        self._engine = matlab.engine

    def __getattr__(self, name):
        """Provide access to Matlab array constructors and utilitiy functions.

        Parameters
        ----------
        name : str
            The name of a Matlab array constructor or utility function.

        Returns
        -------
        callable
            The matlab function or constructor handle.

        Raises
        ------
        AttributeError
            If the Matlab API has no corresponding constructor or utility function.
        MatlabEngineError
            If the Matlab API is not available.

        Examples
        --------
        >>> m = MatlabEngine()
        >>> m.double([[1, 2, 3], [4, 5, 6]])

        """
        if self._matlab:
            if hasattr(self._matlab, name):
                method = getattr(self._matlab, name)

                def wrapper(*args, **kwargs):
                    return method(*args, **kwargs)

                return wrapper
            else:
                raise AttributeError()
        else:
            raise MatlabEngineError()

    def start(self):
        """Start a new Matlab engine and related session.

        Returns
        -------
        str
            The name of the current session.

        Examples
        --------
        >>> m = MatlabEngine()
        >>> m.start()

        """
        print('starting engine. this may take a few seconds...')
        self.engine = self._engine.start_matlab()
        if self.engine:
            sessions = self._engine.find_matlab()
            self.session_name = sessions[0]
        print('engine started!')
        return self.session_name

    def stop(self):
        """Stop the running engine."""
        print('stopping engine...')
        self.engine.quit()
        print('engine stopped!')

    def connect(self, name=None):
        """Connect to an existing Matlab session, or start a new session if none exists.

        Parameters
        ----------
        name : str
            The name of the session.
            Default is ``None``.
            If ``None``, attempt to connect to an existing session, or create a new session if none exists.

        Examples
        --------
        >>> m = MatlabClient()
        >>> m.connect()

        >>> m.connect(name='test')
        """
        sessions = self._engine.find_matlab()
        if name and name in sessions:
            print('connecting to a shared session by name: {0}'.format(name))
            self.engine = self._engine.connect_matlab(name)
            if self.engine:
                self.session_name = name
        else:
            print('connecting to an existing shared session')
            print('or starting a new session (this may take a few seconds)')
            self.engine = self._engine.connect_matlab()
            if self.engine:
                sessions = self._engine.find_matlab()
                self.session_name = sessions[0]
        print('connected to: {0}!'.format(self.session_name))
        print('+' * 80)
        print()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    matlab = MatlabEngine()
    matlab.connect()

    A = matlab.double([[1, 0, 1, 3], [2, 3, 4, 7], [-1, -3, -3, -4]])
    res = matlab.engine.rref(A, nargout=2)

    print(res)
