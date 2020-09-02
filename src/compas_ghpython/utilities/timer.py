from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import Grasshopper as gh


__all__ = [
    'update_component'
]


def update_component(ghenv, delay):
    """Schedule an update of the Grasshopper component.

    After the specified delay, the GH component will be automatically updated.

    Parameters
    ----------
    ghenv : :class:`GhPython.Component.PythonEnvironment`
        The current GHPython environment.
    delay : :obj:`int`
        Time in milliseconds until the update is performed.

    Raises
    ------
    ValueError
        If the delay is less than zero.

    """
    if delay <= 0:
        raise ValueError('Delay must be greater than zero')

    ghcomp = ghenv.Component
    ghdoc = ghcomp.OnPingDocument()

    def callback(ghdoc):
        if ghdoc.SolutionState != gh.Kernel.GH_ProcessStep.Process:
            ghcomp.ExpireSolution(False)

    ghdoc.ScheduleSolution(
        delay, gh.Kernel.GH_Document.GH_ScheduleDelegate(callback))


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':
    pass
