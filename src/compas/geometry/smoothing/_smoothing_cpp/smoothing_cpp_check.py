import compas
from compas.datastructures import Mesh
from compas.plotters import MeshPlotter
from compas.geometry import smooth_centroid_cpp

kmax = 50

# make a mesh
# and set the default vertex and edge attributes

mesh = Mesh.from_obj(compas.get('faces.obj'))

# extract numerical data from the datastructure

vertices  = mesh.get_vertices_attributes(('x', 'y', 'z'))
adjacency = [mesh.vertex_neighbors(key) for key in mesh.vertices()]
fixed     = [int(mesh.vertex_degree(key) == 2) for key in mesh.vertices()]

slider = list(mesh.vertices_where({'x': (-0.1, 0.1), 'y': (9.9, 10.1)}))[0]

# make a plotter for (dynamic) visualization
# and define a callback function
# for plotting the intermediate configurations

plotter = MeshPlotter(mesh, figsize=(10, 7))

def callback(k, xyz):
    print(k)

    if k < kmax - 1:
        xyz[slider][0] = 0.1 * (k + 1)

    plotter.update_vertices()
    plotter.update_edges()
    plotter.update(pause=0.001)

    for key, attr in mesh.vertices(True):
        attr['x'] = xyz[key][0]
        attr['y'] = xyz[key][1]
        attr['z'] = xyz[key][2]

# plot the lines of the original configuration of the mesh
# as a reference

lines = []
for u, v in mesh.edges():
    lines.append({
        'start': mesh.vertex_coordinates(u, 'xy'),
        'end'  : mesh.vertex_coordinates(v, 'xy'),
        'color': '#cccccc',
        'width': 0.5
    })

plotter.draw_lines(lines)

# draw the vertices and edges in the starting configuration
# and pause for a second before starting the dynamic visualization

plotter.draw_vertices(facecolor={key: '#000000' for key in mesh.vertices() if mesh.vertex_degree(key) == 2})
plotter.draw_edges()

plotter.update(pause=0.5)

# run the smoother

xyz = smooth_centroid_cpp(vertices, adjacency, fixed, kmax=kmax, callback=callback)

# keep the plot alive

plotter.show()
