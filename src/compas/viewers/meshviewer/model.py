from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


from compas.utilities import pairwise


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'vanmelet@ethz.ch'


__all__ = ['MeshViewModel', ]


class MeshViewModel(object):
    
    def __init__(self, mesh):
        self._mesh = None
        self._xyz = None
        self._vertices = None
        self._faces = None
        self.mesh = mesh

    @property
    def xyz(self):
        return self._xyz

    @property
    def vertices(self):
        return self.mesh.vertices()

    @property
    def faces(self):
        return self._faces

    @property
    def edges(self):
        return self.mesh.edges()

    @property
    def mesh(self):
        return self._mesh

    @mesh.setter
    def mesh(self, mesh):
        self._mesh = mesh

        xyz = mesh.get_vertices_attributes('xyz')
        faces = []
        for fkey in mesh.faces():
            fvertices = mesh.face_vertices(fkey)
            f = len(fvertices)
            if f < 3:
                pass
            elif f == 3:
                faces.append(fvertices)
            elif f == 4:
                a, b, c, d = fvertices
                faces.append([a, b, c])
                faces.append([c, d, a])
            else:
                o = mesh.face_centroid(fkey)
                v = len(xyz)
                xyz.append(o)
                for a, b in pairwise(fvertices + fvertices[0:1]):
                    faces.append([a, b, v])

        self._xyz = xyz
        self._faces = faces


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
