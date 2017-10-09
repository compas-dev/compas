import compas
import compas_rhino

from compas.files.ply import PLYreader
from compas.datastructures.mesh import Mesh


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'van.mele@arch.ethz.ch'


filename = compas.get_data('stanford/Armadillo.ply')

reader = PLYreader(filename)

reader.read()

for line in reader.header:
    print(line)

vertices = [(vertex['x'], vertex['y'], vertex['z']) for vertex in reader.vertices]
faces = [face['vertex_indices'] for face in reader.faces]

mesh = Mesh.from_vertices_and_faces(vertices, faces)

compas_rhino.draw_mesh(mesh)
