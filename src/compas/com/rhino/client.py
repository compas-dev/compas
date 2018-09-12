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


__all__ = ['RhinoClient']


class RhinoClientError(Exception):
    pass


class RhinoClient(object):
    """Communicate with Rhino through Window's COM interface.

    Parameters
    ----------
    delay_start : bool, optional
        Delay the creation of a COM interface. Default is ``False``.

    Examples
    --------
    >>> r = RhinoApp()
    >>> r.AddPoint(0, 0, 0)
    <guid>

    """

    def __init__(self, delay_start=False):
        self.Rhino = None
        self.rs = None
        if not delay_start:
            self.start()
            # self.wait()

    def __getattr__(self, name):
        if self.rs:
            method = getattr(self.rs, name)

            def wrapper(*args, **kwargs):
                return method(*args, **kwargs)

            return wrapper
        else:
            raise RhinoClientError()

    def start(self):
        Rhino_tlb = GetModule("C:/Program Files/Rhinoceros 5/System/Rhino5.tlb")
        RhinoScript_tlb = GetModule("C:/Program Files/Rhinoceros 5/Plug-ins/RhinoScript.tlb")
        self.Rhino = CreateObject('Rhino5x64.Application').QueryInterface(Rhino_tlb.IRhino5x64Application)
        while not self.Rhino.IsInitialized():
            print('Initialising Rhino...')
            time.sleep(0.5)
        print('Rhino initialised!')
        self.rs = self.Rhino.GetScriptObject().QueryInterface(RhinoScript_tlb.IRhinoScript)

    def stop(self):
        raise NotImplementedError

    def show(self):
        self.Rhino.Visible = True

    def hide(self):
        self.Rhino.Visible = False

    def top(self):
        self.Rhino.BringToTop()

    # def wait(self):
    #     self.rs.GetString('Press enter to exit...', 'exit')
    #     self.rs.Command('_Exit')


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    Rhino = RhinoClient()

    Rhino.show()
    Rhino.top()

    Rhino.rs.AddPoint([0, 0, 0])
