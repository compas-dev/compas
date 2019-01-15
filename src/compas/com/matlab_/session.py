from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


class MatlabSessionError(Exception):
    def __init__(self, message=None):
        if not message:
            message = '''There is no active Matlab session, or could not connect to one...
Don't forget to run "matlab.engine.shareEngine" in Matlab!
Note that the Matlab engine for Python is only available since R2014b.
For older versions of Matlab, use *MatlabProcess* instead.
On Windows, *MatlabClient* is also available.
'''
        super(MatlabSessionError, self).__init__(message)


class MatlabSession(object):
    """Communicate with Matlab through a shared session.

    Parameters
    ----------
    session_name : str
        Name of a running Matlab session.

    Notes
    -----
    Note that the Matlab engine for Python is only available since R2014b.
    For earlier versions of Matlab, use ``MatlabProcess`` instead.

    For more information, see [1]_

    References
    ----------
    .. [1] MathWorks, 2017. *Connect Python to Running MATLAB Session*.
           Available at https://ch.mathworks.com/help/matlab/matlab_external/connect-python-to-running-matlab-session.html

    Examples
    --------
    >>> m = MatlabSession()
    >>> m.session_name
    'MATLAB_13404'
    >>> m.isprime(37)
    True

    Execute the following command to connect ot an existing session.

    .. code-block:: bash

        $ matlab -nosplash -r "matlab.engine.shareEngine('MATLAB_xxx')"

    >>> m = MatlabSession('MATLAB_xxx')
    >>> m.isprime(37)
    True

    """

    def __init__(self, session_name=None):
        self.matlab = None
        self.engine = None
        self.session_name = None
        self.init()
        self.connect(session_name)

    def init(self):
        """Initialise the Matlab engine."""
        import matlab.engine
        self.matlab = matlab.engine
        self.engine = None

    def __getattr__(self, name):
        if self.engine:
            method = getattr(self.engine, name)

            def wrapper(*args, **kwargs):
                return method(*args, **kwargs)

            return wrapper

    def find_sessions(self):
        """Find all available sessions.

        Returns
        -------
        list of str
            A list of available Matlab session names.

        """
        return self.matlab.find_matlab()

    def connect(self, session_name=None):
        """Connect to an existing session or start a new one if none is available.

        Parameters
        ----------
        session_name : str, optional
            The name of the session to connect to.
            Default is to start a new session.

        Notes
        -----
        If successful, the name of the session to which a connection was made is
        stored in the attribute ``session_name``.

        """
        sessions = self.find_sessions()
        if session_name and session_name in sessions:
            print('connecting to a shared session: {0}'.format(session_name))
            self.engine = self.matlab.connect_matlab(session_name)
            if self.engine:
                self.session_name = session_name
        else:
            print('starting a new matlab session. this may take a few seconds...')
            self.engine = self.matlab.connect_matlab()
            if self.engine:
                sessions = self.find_sessions()
                self.session_name = sessions[0]
        print('connected!')


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    m = MatlabSession('test')

    print(m.session_name)
    print(m.isprime(17))
