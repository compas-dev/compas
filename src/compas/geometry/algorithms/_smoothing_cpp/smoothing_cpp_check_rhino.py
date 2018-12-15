from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from ctypes import c_double
import compas
import compas_rhino

from compas.datastructures import Mesh
from compas.geometry import smooth_centroid_cpp

from compas_rhino.artists import MeshArtist
from compas_rhino.conduits import PointsConduit
from compas_rhino.conduits import LinesConduit

kmax = 50

# make a mesh
# and set the default vertex and edge attributes

mesh = Mesh.from_obj(compas.get('faces.obj'))

edges = list(mesh.edges())

# extract numerical data from the datastructure

vertices  = mesh.get_vertices_attributes(('x', 'y', 'z'))
adjacency = [mesh.vertex_neighbors(key) for key in mesh.vertices()]
fixed     = [int(mesh.vertex_degree(key) == 2) for key in mesh.vertices()]

# make a artist for (dynamic) visualization
# and define a callback function
# for plotting the intermediate configurations

slider = list(mesh.vertices_where({'x': (-0.1, 0.1), 'y': (9.9, 10.1)}))[0]

artist = MeshArtist(mesh, layer='SmoothMesh')
artist.clear_layer()


def callback(k, xyz):
    compas_rhino.wait()

    print(k)

    if k < kmax - 1:
        xyz[slider][0] = c_double(0.1 * (k + 1))

    pointsconduit.points = [mesh.vertex_coordinates(key) for key in mesh.vertices()]
    linesconduit.lines = [mesh.edge_coordinates(u, v) for u, v in edges]

    pointsconduit.redraw(k)
    linesconduit.redraw(k)

    for key, attr in mesh.vertices(True):
        attr['x'] = float(xyz[key][0])
        attr['y'] = float(xyz[key][1])
        attr['z'] = float(xyz[key][2])


pointsconduit = PointsConduit(radius=10, refreshrate=5)
linesconduit = LinesConduit(refreshrate=5)


with pointsconduit.enabled():
    with linesconduit.enabled():
        xyz = smooth_centroid_cpp(vertices, adjacency, fixed, kmax=kmax, callback=callback)


for key, attr in mesh.vertices(True):
    attr['x'] = xyz[key][0]
    attr['y'] = xyz[key][1]
    attr['z'] = xyz[key][2]

artist.clear_edges()
artist.draw_vertices()
artist.draw_edges()
artist.redraw()
