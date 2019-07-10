import compas
import compas_rhino

from compas.datastructures import Mesh


__author__    = ['Tom Van Mele', ]
__copyright__ = 'Copyright 2016 - Block Research Group, ETH Zurich'
__license__   = 'MIT License'
__email__     = 'van.mele@arch.ethz.ch'


mesh = Mesh.from_ply(compas.get('stanford_armadillo.ply'))

compas_rhino.mesh_draw(mesh)
