"""A dynamic relaxation example for controlling beam elements."""

from compas.datastructures.network import Network

from compas_blender.geometry import bezier_curve_interpolate
from compas_blender.utilities import draw_bmesh
from compas_blender.utilities import clear_layers
from compas_blender.utilities import get_objects

from compas.numerical.hpc.numba.dynamic_relaxation import numba_dr_run
from compas.numerical.linalg import normrow
from compas.numerical.spatial import closest_points_points
from compas.numerical.solvers.evolutionary.differential_evolution import de_solver

from numpy import array
from numpy import arctan2
from numpy import cos
from numpy import mean
from numpy import pi
from numpy import sin
from numpy import vstack


__author__     = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2017, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'liew@arch.ethz.ch'


def update(dofs, network, Xt, div, factor, tol, steps, ds, refresh, bmesh, plot):
    x1, z1, r1, x2, z2, r2 = dofs
    for c, Xi in enumerate(Xt[::div]):
       network.set_vertex_attributes(c, {'x': Xi[0], 'y': Xi[1], 'z': Xi[2]})
    sp, ep = network.leaves()
    network.set_vertex_attributes(sp, {'x': x1, 'z': z1})
    network.set_vertex_attributes(ep, {'x': x2, 'z': z2})
    network.set_vertex_attributes(sp + 1, {'x': ds * cos(r1) + x1, 'z': ds * sin(r1) + z1})
    network.set_vertex_attributes(ep - 1, {'x': ds * cos(r2) + x2, 'z': ds * sin(r2) + z2})
    X, f, l = numba_dr_run(network, factor, tol, steps, refresh, bmesh, scale=0)
    if plot:
        ind = closest_points_points(X, Xt, distances=False)
        points = vstack([X, Xt[ind, :]])
        n = X.shape[0]
        lines = [[i, i + n] for i in range(n)]
        bmesh = draw_bmesh('norms', vertices=points, edges=lines, layer=19)
    return X


def fn(dofs, *args):
    network, Xt, div, factor, tol, steps, ds = args
    X = update(dofs, network, Xt, div, factor, tol, steps, ds, refresh=0, bmesh=0, plot=0)
    ind = closest_points_points(X, Xt, distances=False)
    return 1000 * mean(normrow(X - Xt[ind, :]))


clear_layers([19])

# Geometry input

L = 0.88
m = 20
n = m + 1
E = 5 * 10**9
I = 2 * 10**(-11)
A = 0.005**2

# Solver input

div = 10
factor = 1.0
tol = 0.01
steps = 10000
deg = pi / 180
du = 0.02
dr = 15 * deg
target = get_objects(0)[0]
Xt = array(bezier_curve_interpolate(target, div * n))

# Network

ds = L / m
xyz = [[i * ds, 0, 0] for i in range(n)]
uv = [[i, i + 1] for i in range(m)]
network = Network.from_vertices_and_edges(xyz, uv)
vertices = network.vertices()
edges = network.edges()
network.set_vertices_attributes(vertices, {'EIx': E * I, 'EIy': E * I})
network.set_edges_attributes(edges, {'E': E, 'A': A, 'l0': ds})
network.set_vertices_attributes([0, 1, m - 1, m], {'B': [0, 0, 0]})
network.beams = {'beam': {'nodes': list(range(n))}}

# Manual

dofs = 0, 0, 65 * deg, 0.6, 0, 135 * deg
#Xs = update(dofs, network, Xt, div, factor, tol, steps, ds, refresh=100, bmesh=True, plot=True)

# Optimise

xa, za = Xt[0, 0], Xt[0, 2]
xb, zb = Xt[1, 0], Xt[1, 2]
xc, zc = Xt[-2, 0], Xt[-2, 2]
xd, zd = Xt[-1, 0], Xt[-1, 2]
r1 = arctan2(zb - za, xb - xa)
r2 = arctan2(zc - zd, xc - xd)
bounds = [(xa - du, xa + du), (za - du, za + du), (r1 - dr, r1 + dr),
          (xd - du, xd + du), (zd - du, zd + du), (r2 - dr, r2 + dr)]
args = network, Xt, div, factor, tol, steps, ds
fopt, uopt = de_solver(fn, bounds, population=20, iterations=50, args=args)

# Plot

update(uopt, network, Xt, div, factor, tol, steps, ds, refresh=0, bmesh=1, plot=1)
