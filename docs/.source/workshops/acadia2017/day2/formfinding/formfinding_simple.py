""""""

import compas

from compas.datastructures import Mesh
from compas.numerical import fd


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


def main():

    mesh = Mesh.from_obj(compas.get('faces.obj'))

    # fd(vertices, edges, fixed, q, loads, rtype='list')


# ==============================================================================
# Debugging
# ==============================================================================

if __name__ == "__main__":
    
    main()
