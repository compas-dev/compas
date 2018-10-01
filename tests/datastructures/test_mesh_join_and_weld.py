import copy

from compas.datastructures import Mesh
from compas.datastructures.mesh.operations.weld import join_meshes
from compas.datastructures.mesh.operations.weld import weld_mesh
from compas.datastructures.mesh.operations.weld import join_and_weld_meshes

__author__     = ['Robin Oval']
__copyright__  = 'Copyright 2018, Block Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'oval@arch.ethz.ch'

mesh_1 = Mesh.from_obj(compas.get('faces.obj'))

mesh_2 = copy.copy(mesh)
for vkey in mesh_2.vertices():
    mesh_2.vertex[vkey]['y'] += 10.

mesh_3 = join_meshes([mesh_1, mesh_2])
print('joining: nb vertices:', mesh_3.number_of_vertices(), '; nb faces:', mesh_3.number_of_faces())

mesh_4 = weld_mesh(mesh_3)
print('welding: nb vertices:', mesh_4.number_of_vertices(), '; nb faces:', mesh_4.number_of_faces())

mesh_5 = join_and_weld_meshes([mesh_1, mesh_2])
print('joining and welding: nb vertices:', mesh_5.number_of_vertices(), '; nb faces:', mesh_5.number_of_faces())

