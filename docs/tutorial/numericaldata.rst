**************
Numerical Data
**************

When working with numerical algorithms, the information stored in a data structure
needs to be converted to lists and/or arrays as input for the algorithm.
Afterwards, the result needs to be integrated back into the data structure.

Although the identifiers of mesh vertices are integers (like the indices in a list)
and identifiers are added automatically in ascending order,
the ordering is not necessarily contiguous, nor continuous after certain mesh operations.

Therefore, when converting data structure data to numerical data,
it is important that identifiers of the data in the data structure
are properly matched to the positions of the same data in the corresponding lists or arrays.

For example, the proper way to run a Force Density algorithm (:func:`compas.numerical.fd_numpy`)
on a mesh uses a ``vertex_index`` map to take care of this relationship between identifiers and indices.

.. code-block:: python

    import compas
    from compas.datastructures import Mesh
    from compas.numerical import fd_numpy

    mesh = Mesh.from_obj(compas.get('faces.obj'))

    mesh.update_default_vertex_attributes({'px': 0.0, 'py': 0.0, 'pz': 0.0})
    mesh.update_default_edge_attributes({'q': 1.0})

    xyz = mesh.vertices_attributes('xyz')
    loads = [[0, 0, 0] for _ in range(mesh.number_of_vertices())]
    q = mesh.edges_attribute('q')

    vertex_index = {vertex: index for index, vertex in enumerate(mesh.vertices())}

    fixed = [vertex_index[vertex] for vertex in mesh.vertices_where({'vertex_degree': 2})]
    edges = [(vertex_index[u], vertex_index[v]) for u, v in mesh.edges()]

    result = fd_numpy(xyz, edges, fixed, q, loads)
    xyz = result[0]

    for vertex in mesh.vertices():
        index = vertex_index[vertex]
        mesh.vertex_attributes(vertex, 'xyz', xyz[index])

In short, this example
creates a mesh from a sample file,
assignes default attributes to the vertices and the edges,
compiles the numerical data,
runs the algorithm,
and updates the data structure with the result.

The coordinates of the vertices are assembled in the list ``xyz``,
and the loads on the vertices in the list ``loads``.
The force densities in the edges are in the list ``q``.
The list ``fixed`` identifies the vertices which should stay in a fixed location during the form finding process,
and ``edges`` contains pairs of vertices that will be used by the algorithm to define a connectivity matrix.

To make sure all lists refer to each other correctly,
the `vertex_index` :obj:`dict` creates a map between the identifiers of vertices in the data structure
and the order in which they appear in lists.
The map is used in three different ways.

1.  To convert the identifiers of fixed vertices (vertices with only two neighbours => corner vertices)
    to indices into the lists ``xyz`` and ``loads``.

    .. code-block:: python

        fixed = [vertex_index[vertex] for vertex in mesh.vertices_where({'vertex_degree': 2})]

2.  To convert the pairs of vertex identifiers in ``edges`` to pairs of indices into the lists ``xyz`` and ``loads``.

    .. code-block:: python

        edges = [(vertex_index[u], vertex_index[v]) for u, v in mesh.edges()]

3.  To make sure the new vertex coordinates are assigned to the correct vertices in the data structure.

    .. code-block:: python

        for vertex in mesh.vertices():
            index = vertex_index[vertex]
            mesh.vertex_attributes(vertex, 'xyz', xyz[index])
