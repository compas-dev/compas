import compas
import compas_rhino
from compas.datastructures import Mesh

mesh = Mesh.from_ply(compas.get('stanford_dragon.ply'))

compas_rhino.mesh_draw(mesh)
