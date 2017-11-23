from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import time

try:
    from comtypes.client import CreateObject
    from comtypes.client import GetModule
except ImportError:
    import platform
    if 'windows' in platform.system().lower():
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
        # self.rsm = GetModule(['{75B1E1B4-8CAA-43C3-975E-373504024FDB}', 1, 0])
        # self.rsm = GetModule(['{1C7A3523-9A8F-4CEC-A8E0-310F580536A7}', 1, 0])
        # self.rsm = GetModule(['{814d908a-e25c-493d-97e9-ee3861957f49}', 1, 0])
        # self.rsm = GetModule(['{8ABB4303-8057-47AD-BAEB-263965E5565D}', 1, 0])
        # self.rsm = GetModule(['{75B1E1B4-8CAA-43C3-975E-373504024FDB}', 1, 0])
        R = GetModule(r"C:\Program Files\Rhinoceros 5\System\Rhino5.tlb")
        RS = GetModule(r"C:\Program Files\Rhinoceros 5\Plug-ins\RhinoScript.tlb")

        print(dir(R))
        print(dir(RS))

        print('loading script interface...')

        attempts = 20

        self.app = CreateObject('Rhino5x64.Application')

        while attempts:
            try:
                print('attempt %s' % attempts)
                # self.rsi = self.app.GetScriptObject.QueryInterface(self.rsm.IRhinoScript)
                # self.rsi = self.app.QueryInterface(self.rsm.IRhino5x64Application).GetScriptObject()
                o = self.app.QueryInterface(R.IRhino5x64Interface).GetScriptObject()
                self.rsi = o.QueryInterface(RS.IRhinoScript)
                break
            except Exception as e:
                print(e)
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
# Main
# ==============================================================================

if __name__ == "__main__":

    client = RhinoClient()
    client.rsi.AddPoint([0, 0, 0])
