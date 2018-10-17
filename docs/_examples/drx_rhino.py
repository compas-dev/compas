
from compas.datastructures import Network
from compas.utilities import geometric_key
from compas.utilities import XFunc
from compas_rhino.artists.networkartist import NetworkArtist

import rhinoscriptsyntax as rs


__author__    = ['Andrew Liew <liew@arch.ethz.ch>']
__copyright__ = 'Copyright 2018, BLOCK Research Group - ETH Zurich'
__license__   = 'MIT License'
__email__     = 'liew@arch.ethz.ch'


# Input

s0 = 10**6
E  = 10**6
A  = 0.005**2
factor = 5.0
tol = 0.1
steps = 10000

# Network

guids   = rs.ObjectsByLayer('Lines')
lines   = [[rs.CurveStartPoint(i), rs.CurveEndPoint(i)] for i in guids if rs.IsCurve(i)]
network = Network.from_lines(lines)

# Attributes

network.update_default_edge_attributes({'E': E, 'A': A, 's0': s0})

# Pins

gkey_key = network.gkey_key()
pins = []

for i in rs.ObjectsByLayer('Pins'):
    gkey = geometric_key(rs.PointCoordinates(i))
    key = gkey_key[gkey]
    network.set_vertex_attributes(key, 'B', [[0, 0, 0]])
    pins.append(key)

# Run XFunc

X, f, l, network = XFunc('compas.numerical.drx.drx_numpy.drx_numpy')(
    structure=network, 
    factor=factor, 
    tol=tol, 
    steps=steps, 
    refresh=10, 
    update=True
)

# Draw Network

artist = NetworkArtist(network=network, layer='Plot')
artist.clear_layer()
artist.draw_edges()
