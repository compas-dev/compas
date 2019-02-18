from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


__all__ = [
	'mesh_insert_vertex_on_edge'
]


def mesh_insert_vertex_on_edge(self, u, v, vkey=None):
	"""Insert an existing vertex on an edge.

	Parameters
	----------
	u: hashable
		The first edge vertex.
	v: hashable
		The second edge vertex.
	vkey: hashable, optional
		The vertex key to insert.
		Default is add a new vertex at mid-edge.

	"""

	# add new vertex if there is none
	if vkey is None:
		mesh.add_vertex(attr_dict = {attr: xyz for attr, xyz in zip(['x', 'y', 'z'], mesh.edge_midpoint(u, v))})

	# insert vertex
	for fkey, halfedge in zip(mesh.edge_faces(u, v), [(u, v), (v, u)]):
		if fkey is not None:
			face_vertices = mesh.face_vertices(fkey)[:]
			face_vertices.insert(face_vertices.index(halfedge[-1]), vkey)
			mesh.delete_face(fkey)
			mesh.add_face(face_vertices, fkey)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":

	import compas
	from compas.datastructures import Mesh
	from compas.plotters import MeshPlotter

	vertices = [
		[0, 0, 0],
		[1, 0, 0],
		[1, 1, 0],
		[0, 1, 0],
		[2, 2, 0],
		[2, 0, 0]
	]
	faces = [
		[0, 1, 2, 3],
		[1, 4, 2]
	]

	mesh = Mesh.from_vertices_and_faces(vertices, faces)

	mesh_insert_vertex_on_edge(mesh, 0, 1)
	mesh_insert_vertex_on_edge(mesh, 1, 4, 5)

	plotter = MeshPlotter(mesh)
	plotter.draw_vertices(text='key')
	plotter.draw_edges()
	plotter.draw_faces(text='key')
	plotter.show()
