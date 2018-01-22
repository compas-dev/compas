
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.datastructures import Network


__author__    = ['Andrew Liew <liew@arch.ethz.ch>', 'Jef Rombouts <jef.rombouts@kuleuven.be>']
__copyright__ = 'Copyright 2018, BLOCK Research Group - ETH Zurich'
__license__   = 'MIT License'
__email__     = 'liew@arch.ethz.ch'


__all__ = [
    'dr_6dof_numpy',
]


def dr_6dof_numpy(network):
    """Run dynamic relaxation analysis, 6 DoF per node.

    Parameters
    ----------
    network : Network
        Network to analyse.

    Returns
    -------
    None

    """

    return


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

    from compas.viewers import NetworkViewer

    L = 20
    m = 10
    dx = L / m

    network = Network()
    for i in range(m + 1):
        x = i * dx
        network.add_vertex(key=i, x=x)
        if i < m:
            network.add_edge(key=i, u=i, v=i+1)

    viewer = NetworkViewer(network=network, width=1000, height=800)
    viewer.setup()
    viewer.show()
