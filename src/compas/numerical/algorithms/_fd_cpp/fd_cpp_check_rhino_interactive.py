from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import Rhino

from System.Drawing.Color import FromArgb

from Rhino.Geometry import Point3d
from Rhino.Geometry import Line

import compas
import compas_rhino

from compas.datastructures import Network
from compas.numerical import fd_cpp

from compas_rhino.helpers import NetworkArtist
from compas_rhino.helpers.selectors import VertexSelector
from compas_rhino.conduits import LinesConduit


network = Network.from_obj(compas.get('saddle.obj'))


vertices = network.get_vertices_attributes('xyz')
loads    = network.get_vertices_attributes(('px', 'py', 'pz'), (0.0, 0.0, 0.0))
fixed    = network.leaves()
free     = [i for i in range(len(vertices)) if i not in fixed]
edges    = list(network.edges())
q        = network.get_edges_attribute('q', 1.0)


artist = NetworkArtist(network, layer='Network')

artist.clear_layer()
artist.draw_edges(color='#cccccc')
artist.redraw()

xyz = fd_cpp(vertices, edges, fixed, q, loads)

for key, attr in network.vertices(True):
    attr['x'] = xyz[key][0]
    attr['y'] = xyz[key][1]
    attr['z'] = xyz[key][2]

artist.draw_vertices(color={key: '#ff0000' for key in network.leaves()})
artist.draw_edges(color='#000000')
artist.redraw()

# select and drag one of the anchors
# update equilibrium using *OnDynamicDraw*

move = VertexSelector.select_vertex(network)
move = int(move)

sp = network.vertex_coordinates(move)
ep = sp[:]
ep[2] += 1

vertical = Line(Point3d(*sp), Point3d(*ep))

color = FromArgb(255, 255, 255)


def OnDynamicDraw(sender, e):
    global xyz
    xyz[move] = list(e.CurrentPoint)
    xyz = fd_cpp(xyz, edges, fixed, q, loads)
    for u, v in edges:
        e.Display.DrawLine(Point3d(* xyz[u]), Point3d(* xyz[v]), color)


gp = Rhino.Input.Custom.GetPoint()
gp.SetCommandPrompt('Point to move to?')
gp.Constrain(vertical)
gp.DynamicDraw += OnDynamicDraw
gp.Get()

if gp.CommandResult() == Rhino.Commands.Result.Success:
    xyz[move] = list(gp.Point())
    xyz = fd_cpp(xyz, edges, fixed, q, loads)

    for key, attr in network.vertices(True):
        attr['x'] = xyz[key][0]
        attr['y'] = xyz[key][1]
        attr['z'] = xyz[key][2]

    artist.draw_vertices(color={key: '#ff0000' for key in network.leaves()})
    artist.draw_edges(color='#000000')
    artist.redraw()
