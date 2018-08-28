from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import sys
import time

from subprocess import Popen
from subprocess import PIPE

try:
    from scipy.io import savemat
    from scipy.io import loadmat
except ImportError:
    if 'ironpython' not in sys.version.lower():
        raise


__all__ = ['MatlabProcess']


class MatlabProcessError(Exception):
    def __init__(self, message=None):
        if not message:
            message = """"""
        super(MatlabProcessError, self).__init__(message)


class MatlabProcess(object):
    """Communicate with Matlab through a subprocess.

    Parameters
    ----------
    matlab_exec : str, optional
        Path to the Matlab executable. Defaults to ``matlab``.
    ws_data : dict, optional
        Workspace data to be loaded at startup. Defaults to an empty dict.
    ws_filename : str, optional
        Filename for workspace storage. Defaults to ``'./workspace.mat'``.

    Examples
    --------
    >>> m = MatlabProcess()

    >>> m.start()
    >>> m.write_value('a', 37)
    >>> m.run_command('tf = isprime(a);')
    >>> m.read_workspace()
    >>> m.stop()
    >>> print(m.ws_data)

    >>> m.write_value('a', 17)
    >>> m.run_command('res = isprime(a);')
    >>> m.read_value('res')
    True

    >>> m.run_command('res = isprime(a);', ivars={'a': 17})
    >>> m.read_value('res')
    True

    >>> m.run_command('res = isprime(a);', ivars={'a': 17}, ovars={'res': None})
    {'res': True}

    """

    def __init__(self, matlab_exec=None, ws_data=None, ws_filename=None, timeout=None, verbose=True):
        """"""
        self.matlab_exec    = matlab_exec or 'matlab'
        self.matlab_options = ['-nosplash']
        self.ws_data        = ws_data or {}
        self.ws_filename    = ws_filename or './workspace.mat'
        self.timeout        = timeout or 20
        self.process        = None
        self.verbose        = verbose

    def init(self):
        pass

    def start(self, options=None):
        """Start the subprocess.

        Parameters:
            options (list, optional) : A list of command line options for the Matlab
                executable. Available options:

                    * -nosplash
                    * -wait (Windows)
                    * ...
        """
        options = options or self.matlab_options
        if self.verbose:
            print('create workspace file.')
        with open(self.ws_filename, 'wb'):
            pass
        if self.verbose:
            print('starting Matlab process...')
        pargs = [self.matlab_exec]
        pargs.extend(options)
        self.process = Popen(pargs, stdout=PIPE, stderr=PIPE, stdin=PIPE)
        self._wait_until('__READY__')
        if self.verbose:
            print('=' * 79)

    def _wait_until(self, str_to_wait_for):
        self.process.stdin.write("'{0}'\n".format(str_to_wait_for))
        t0 = time.time()
        while True:
            line = self.process.stdout.readline()
            if line.strip() == str_to_wait_for:
                return
            if time.time() - t0 > self.timeout:
                return

    def stop(self):
        if self.verbose:
            print('=' * 79)
            print('stopping Matlab process...')
        self.process.stdin.write("exit;\n")
        self.process.terminate()
        if self.verbose:
            print('closing streams...')
        self.process.stdin.close()
        self.process.stdout.close()
        self.process.stderr.close()

    def run_command(self, command, ivars=None, ovars=None):
        """Run a command in Matlab.

        Parameters:
            command (str) : The command string.
            ivars (dict, optional) : A dictionary of pairs of variable names and
                values to write to the Matlab workspace.

        """
        if self.verbose:
            print('run Matlab command: {0}'.format(command))
        if ivars:
            for name, value in ivars.items():
                self.write_value(name, value)
        command = command.strip() + '\n'
        self.process.stdin.write(command)
        self._wait_until('__COMPLETED__')
        if ovars:
            for name, value in ovars.items():
                ovars[name] = self.read_value(name, value)
            return ovars

    def write_value(self, name, value):
        if self.verbose:
            print('write Matlab value: {0} => {1}'.format(name, value))
        self.process.stdin.write("{0}={1};\n".format(name, value))

    def read_value(self, name, default=None):
        if self.verbose:
            print('read Matlab value: {0}'.format(name))
        self.process.stdin.write("save('{0}', '{1}');\n".format(self.ws_filename, name))
        self._wait_until('__SAVED__')
        loadmat(self.ws_filename, mdict=self.ws_data)
        value = self.ws_data.get(name)
        if value:
            return value[0][0]
        return default

    def write_workspace(self):
        if not self.ws_data:
            return
        if self.verbose:
            print('write Matlab workspace.')
        savemat(self.ws_filename, self.ws_data)
        self.process.stdin.write("load({0});\n".format(self.ws_filename))
        self._wait_until('__LOADED__')

    def read_workspace(self):
        if self.verbose:
            print('read Matlab workspace.')
        self.process.stdin.write("save('{0}');\n".format(self.ws_filename))
        self._wait_until('__SAVED__')
        loadmat(self.ws_filename, mdict=self.ws_data)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    m = MatlabProcess()

    m.start()

    m.write_value('a', 37)
    m.run_command('res = isprime(a);')

    print(m.read_value('res'))
    print(m.run_command('res = isprime(a);', ivars={'a': 17}, ovars={'res': None}))

    # m.read_workspace()
    m.stop()

    print(m.ws_data)
