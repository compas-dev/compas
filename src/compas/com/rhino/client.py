from __future__ import print_function

import time

try:
    from comtypes.client import CreateObject
    from comtypes.client import GetModule
except ImportError:
    import platform
    if platform.python_implementation() == 'IronPython':
        raise


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = '<vanmelet@ethz.ch>'


__all__ = ['RhinoClient', ]


class RhinoClientError(Exception):
    pass


class RhinoClient(object):
    """Communicate with Rhino through Window's COM interface.

    Warning:
        This only works on Windows!

    Parameters:
        delay_start (bool, optional) : Delay the creation of a COM interface.
            Default is ``False``.

    Examples:
        >>> r = RhinoApp()
        >>> r.AddPoint(0, 0, 0)
        <guid>

    """

    def __init__(self, delay_start=False):
        self.app = None
        self.rsm = None
        self.rsi = None
        if not delay_start:
            self.start()
            self.wait()

    def __getattr__(self, name):
        if self.rsi:
            method = getattr(self.rsi, name)

            def wrapper(*args, **kwargs):
                return method(*args, **kwargs)

            return wrapper
        else:
            raise RhinoClientError()

    def start(self):
        self.app = CreateObject('Rhino5.Application')
        self.rsm = GetModule(['{75B1E1B4-8CAA-43C3-975E-373504024FDB}', 1, 0])
        print('loading script interface...')
        attempts = 20
        while attempts:
            try:
                print('attempt %s' % attempts)
                self.rsi = self.app.GetScriptObject.QueryInterface(self.rsm.IRhinoScript)
                break
            except Exception:
                time.sleep(0.5)
            attempts -= 1
        if self.rsi is None:
            raise Exception('error loading script interface...')
        print('script interface loaded!')

    def stop(self):
        raise NotImplementedError

    def show(self, flag=1):
        self.app.Visible = flag

    def wait(self):
        self.rsi.GetString('Press enter to exit...', 'exit')
        self.rsi.Command('_Exit')


# ==============================================================================
# Testing
# ==============================================================================

if __name__ == "__main__":
    pass
