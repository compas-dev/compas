from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas

from compas.viewers.core import App

from compas.viewers.meshviewer.view import View
from compas.viewers.meshviewer.controller import Controller

from compas.viewers.meshviewer import CONFIG
from compas.viewers.meshviewer import STYLE


__author__     = ['Tom Van Mele', ]
__copyright__  = 'Copyright 2014, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'vanmelet@ethz.ch'


__all__ = ['MeshViewer', ]


class MeshViewer(App):
    """"""

    def __init__(self):
        super(MeshViewer, self).__init__(CONFIG, STYLE)
        self.controller = Controller(self)
        self.view = View(self.controller)
        self.setup()
        self.init()

    def show(self):
        super(MeshViewer, self).show()

        # self.controller.mesh = mesh

        # self.controller.center_mesh()
        # self.controller.view.make_buffers()
        # self.controller.view.update()

    # @property
    # def mesh(self):
    #     return self.controller.mesh

    # @mesh.setter
    # def mesh(self, mesh):
    #     self.controller.mesh = mesh


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    import compas
    from compas.datastructures import Mesh

    # mesh = Mesh.from_polyhedron(6)
    # print(mesh)

    MeshViewer().show()

    # viewer.controller.mesh = Mesh.from_polyhedron(6)
    # viewer.controller.center_mesh()
    # viewer.controller.view.make_buffers()
    # viewer.controller.view.update()
