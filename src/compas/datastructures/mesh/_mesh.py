from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.datastructures.mesh.__mesh import _Mesh
from compas.datastructures.mesh.transformations import mesh_transform
from compas.datastructures.mesh.transformations import mesh_transformed

__all__ = ['Mesh']


class Mesh(_Mesh):
    
    transform = mesh_transform
    transformed = mesh_transformed


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    pass
