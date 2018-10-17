from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas.viewers.core import App

from compas.viewers.meshviewer.view import View
from compas.viewers.meshviewer.controller import Controller

from compas.viewers.meshviewer import CONFIG
from compas.viewers.meshviewer import STYLE


__all__ = ['MeshViewer']


class MeshViewer(App):
    """"""

    def __init__(self):
        super(MeshViewer, self).__init__(CONFIG, STYLE)
        self.controller = Controller(self)
        self.view = View(self.controller)
        self.setup()
        self.init()
        self.view.glInit()
        self.view.setup_grid()
        # self.view.setup_axes()

    @property
    def mesh(self):
        return self.controller.mesh

    @mesh.setter
    def mesh(self, mesh):
        self.controller.mesh = mesh
        self.controller.center_mesh()
        self.view.glInit()
        self.view.make_buffers()
        self.view.updateGL()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == '__main__':

    # because of current near/far settings of the camera
    # the viewer has difficulties displaying very small or very large objects
    # near/far should be set based on the size of the objects
    # user should be able to change these settings

    # camera aiming should be implemented with gluLookAt
    # zooming, rotating, panning should be implemented accordingly

    # there seems to be an issue with keeping the mesh and meshview synchronised

    # some lighting would be appropriate
    # texture mapping for appreciation of mesh quality?

    # don't auto-center the objects
    # provide zoom extents and focus functions instead
    # allow user to adjust camera settings
    # and adapt projection parameters to the size of the model

    import compas
    from compas.datastructures import Mesh
    from compas.geometry import transform_points
    from compas.geometry import matrix_from_translation


    class Mesh(Mesh):

        def apply_xform(self, M):
            key_index = self.key_index()
            points = self.get_vertices_attributes('xyz')
            points = transform_points(points, M)
            for key, attr in self.vertices(True):
                index = key_index[key]
                x, y, z = points[index]
                attr['x'] = x
                attr['y'] = y
                attr['z'] = z


    t = [3, 0, 0]
    M = matrix_from_translation(t)

    mesh = Mesh.from_polyhedron(6)
    mesh.apply_xform(M)

    viewer = MeshViewer()
    viewer.mesh = mesh
    # viewer.view.camera.target = t

    viewer.show()
