"""Collapse a mesh to a single vertex."""

from __future__ import print_function

import compas

from compas.datastructures.mesh import Mesh
from compas.datastructures.mesh.operations import split_face_mesh
from compas.datastructures.mesh.operations import collapse_edge_trimesh
from compas.visualization.plotters.meshplotter import MeshPlotter


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'van.mele@arch.ethz.ch'


mesh = Mesh.from_obj(compas.get_data('faces.obj'))

plotter = MeshPlotter(mesh)

plotter.defaults['face.facecolor'] = '#eeeeee'
plotter.defaults['face.edgecolor'] = '#cccccc'

plotter.draw_vertices()
plotter.draw_faces()

for fkey in list(mesh.faces()):
    vertices = mesh.face_vertices(fkey, ordered=True)
    split_face_mesh(mesh, fkey, vertices[0], vertices[2])

u = 18
vertices = [3, 29, 24, 1, 21, 23, 2, 12, 28, 34, 0, 20, 4, 26, 7, 32, 5, 15, 25, 17, 22, 11, 8, 31, 19, 9, 30, 16, 13, 14, 6, 33, 27, 35]

for v in vertices:
    collapse_edge_trimesh(mesh, u, v, t=0.0, allow_boundary=True)

    plotter.update_vertices()
    plotter.update_faces()
    plotter.update(0.1)

plotter.show()
