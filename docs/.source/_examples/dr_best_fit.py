"""An example of l0 best-fitting with dynamic relaxation."""

from compas_blender.helpers import network_from_bmesh
from compas_blender.helpers import draw_network
from compas_blender.utilities import draw_plane
from compas_blender.utilities import clear_layers

from compas.numerical.linalg import normrow
from compas.numerical.hpc.numba.dynamic_relaxation import numba_dr_run
from compas.numerical.solvers.evolutionary.differential_evolution import de_solver

from numpy import isinf
from numpy import isnan
from numpy import mean
from numpy import zeros


__author__     = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2017, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'liew@arch.ethz.ch'


# Objective function

def fn(l0, *args):
    tol, Xt, edges = args
    for c, uv in enumerate(edges):
        network.set_edge_attribute(uv[0], uv[1], 'l0', l0[c])
    X, f, l = numba_dr_run(network, tol=tol)
    X[:, 2] /= max(X[:, 2])
    norm = mean(normrow(X - Xt))
    if isnan(norm) or isinf(norm):
        return 10**6
    return norm


# Network

ds = 0.1
network = network_from_bmesh(draw_plane(Lx=1, Ly=1, dx=ds, dy=ds))
vertices = list(network.vertices())
edges = list(network.edges())
n = len(vertices)
m = len(edges)
Xt = zeros((n, 3))
network.set_vertices_attributes(vertices, {'B': [0, 0, 1], 'P': [0, 0, 1 / n]})
for c, key in enumerate(vertices):
    x, y, z = network.vertex_coordinates(key)
    if (x == 1) and (y == 1):
        network.set_vertex_attribute(key, 'B', [0, 0, 0])
    zt = 1 - 0.5 * (x**2 + y**2)
    Xt[c, :] = [x, y, zt]
network.set_edges_attributes(edges, {'E': 1, 'A': 1, 'ct': 't'})

clear_layers([0])

# Run optimisation

tol = 0.001 / n
bounds = [[0.7 * ds, 1.3 * ds]] * m
fopt, uopt = de_solver(fn, bounds, population=20, iterations=10**4, args=(tol, Xt, edges), limit=0.002)

# Update Network and plot

for c, uv in enumerate(edges):
    dl0 = ds - uopt[c]
    color = 'red' if dl0 < 0 else 'blue'
    network.set_edge_attributes(uv[0], uv[1], {'l0': uopt[c], 'color': color, 'radius': dl0})
X, f, l = numba_dr_run(network, tol=tol, update=True)
draw_network(network, type='lines', show_vertices=0)
