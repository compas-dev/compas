"""Mesh subdivision in Grasshopper using the catmull clark algorithm.
    Inputs:
        is_fixed: list of boolean
            A list of booleans relating to the vertex keys (index = key).
        k: int
            The number of levels of subdivision.
    Output:
        P: Rhino points (vertices) of the control mesh
        L: Rhino lines (edges) of the control mesh 
        M: The resulting Rhino mesh
"""

from __future__ import print_function
from __future__ import division

from compas.datastructures import Mesh
from compas.datastructures import mesh_subdivide

from compas_ghpython.artists import MeshArtist

# make a control mesh
mesh = Mesh.from_polyhedron(6)

# set default vertex attributes
mesh.update_default_vertex_attributes({'is_fixed': False})

# make an artist for drawing
artist = MeshArtist(mesh)

# draw the control mesh into outputs P, L 
P = artist.draw_vertices()
L = artist.draw_edges()

# keep some of the vertices fixed and make a subd mesh (using catmullclark)
for key, value in zip(range(len(is_fixed)), is_fixed):
    mesh.set_vertex_attribute(key, 'is_fixed', value)
            
fixed = mesh.vertices_where({'is_fixed': True})
subd = mesh_subdivide(mesh, scheme='catmullclark', k=k, fixed=fixed)

# pass the new mesh to the artist
artist.mesh = subd

# draw the result into output M
M = artist.draw_mesh()
