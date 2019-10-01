"""Mesh subdivision in Grasshopper using the catmull clark algorithm.
    Inputs:
        fixed_keys: list of int
            The vertex keys to be set to `is_fixed` 
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

# make a subd mesh (using catmullclark) and keep some of the vertices fixed
mesh.set_vertices_attribute('is_fixed', True, fixed_keys)
subd = mesh_subdivide(mesh, scheme='catmullclark', k=5, fixed=fixed_keys)

# pass the new mesh to the artist
artist.mesh = subd

# draw the result into output M
M = artist.draw_mesh()
