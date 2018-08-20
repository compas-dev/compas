"""A dynamic relaxation example for controlling beam elements."""

from compas.datastructures import Network

from compas_blender.geometry import BlenderCurve
from compas_blender.utilities import clear_layer
from compas_blender.utilities import get_objects
from compas_blender.utilities import xdraw_mesh

from compas.hpc import drx_numba

from compas.numerical import devo_numpy
from compas.numerical import normrow

from numpy import array
from numpy import arctan2
from numpy import argmin
from numpy import cos
from numpy import mean
from numpy import pi
from numpy import sin
from numpy import vstack

from scipy.spatial.distance import cdist

from compas.plotters.evoplotter import EvoPlotter


__author__     = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__  = 'Copyright 2017, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'liew@arch.ethz.ch'


def update(dofs, network, tol, plot, Xt, ds):
    x1, z1, r1, x2, z2, r2 = dofs
    dx1 = ds * cos(r1)
    dx2 = ds * cos(r2)
    dz1 = ds * sin(r1)
    dz2 = ds * sin(r2)
    sp, ep = network.leaves()
    network.set_vertex_attributes(sp, {'x': x1, 'z': z1})
    network.set_vertex_attributes(ep, {'x': x2, 'z': z2})
    network.set_vertex_attributes(sp + 1, {'x': dx1 + x1, 'z': dz1 + z1})
    network.set_vertex_attributes(ep - 1, {'x': dx2 + x2, 'z': dz2 + z2})
    X, f, l = drx_numba(network=network, factor=1, tol=tol)
    if plot:
        ind = argmin(cdist(X, Xt), axis=1)
        vertices = vstack([X, Xt[ind, :]])
        n = X.shape[0]
        edges = [[i, i + n] for i in range(n)] + list(network.edges())
        xdraw_mesh(name='norms', vertices=vertices, edges=edges)
    return X


def fn(dofs, *args):
    network, Xt, tol, ds = args
    X = update(dofs=dofs, network=network, tol=tol, plot=False, Xt=Xt, ds=ds)
    ind = argmin(cdist(X, Xt), axis=1)
    return 1000 * mean(normrow(X - Xt[ind, :]))


def callback(ts, f, evoplotter):
    evoplotter.update_points(generation=ts, values=f)
    evoplotter.update_lines(generation=ts, values=f)


clear_layer(layer=0)

# Beam input

L = 0.88
m = 20
ds = L / m
div = 10
E = 5 * 10**9
I = 2 * 10**(-11)
A = 0.005**2

# Solver input

mi = div * m
tol = 0.01
du = 0.02
deg = pi / 180
dr = 15 * deg

# Target

curve = get_objects(layer=1)[0]
blendercurve = BlenderCurve(object=curve)
Xt = array(blendercurve.divide(number_of_segments=mi))

# Network

vertices = [list(Xi) for Xi in list(Xt[:mi:div, :])]
edges = [[i, i + 1] for i in range(m)]
network = Network.from_vertices_and_edges(vertices=vertices, edges=edges)
network.update_default_vertex_attributes({'EIx': E * I, 'EIy': E * I})
network.update_default_edge_attributes({'E': E, 'A': A, 'l0': ds})
network.set_vertices_attributes([0, 1, m - 1, m], {'B': [0, 0, 0]})
network.beams = {'beam': {'nodes': list(range(network.number_of_vertices()))}}

# Manual

# dofs = 0, 0, 45 * deg, 0.6, 0, 155 * deg
# Xs = update(dofs=dofs, network=network, tol=tol, plot=True, Xt=Xt, ds=ds)

# Optimise

generations = 30

xa, za = Xt[+0, [0, 2]]
xb, zb = Xt[+1, [0, 2]]
xc, zc = Xt[-2, [0, 2]]
xd, zd = Xt[-1, [0, 2]]
r1 = arctan2(zb - za, xb - xa)
r2 = arctan2(zc - zd, xc - xd)
bounds = [(xa - du, xa + du), (za - du, za + du), (r1 - dr, r1 + dr),
          (xd - du, xd + du), (zd - du, zd + du), (r2 - dr, r2 + dr)]
args = network, Xt, tol, ds


evoplotter = EvoPlotter(generations=generations,
                        fmax=20,
                        xaxis_div=generations,
                        yaxis_div=10,
                        pointsize=0.1)

fopt, uopt = devo_numpy(fn=fn,
                        bounds=bounds,
                        population=20,
                        generations=generations,
                        args=args,
                        callback=callback,
                        evoplotter=evoplotter)

# Plot

update(dofs=uopt, network=network, tol=tol, plot=True, Xt=Xt, ds=ds)
