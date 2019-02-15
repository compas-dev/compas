from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import time
import compas

try:
    from comtypes.client import CreateObject
    from comtypes.client import GetModule
except ImportError:
    compas.raise_if_windows()


__all__ = ['RhinoClient']


class RhinoClientError(Exception):
    pass


class RhinoClient(object):
    """Communicate with Rhino through Window's COM interface.

    Warning
    -------
    This functionality is only available on Windows.

    Examples
    --------
    >>> rhino = RhinoClient()
    >>> rhino.start()
    >>> rhino.show()
    >>> rhino.top()
    >>> rhino.AddPoint(0, 0, 0)
    <guid>

    """

    def __init__(self):
        self.Rhino = None
        self.rs = None

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


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    Rhino = RhinoClient()

    Rhino.start()
    Rhino.show()
    Rhino.top()

    Rhino.AddPoint([0, 0, 0])
