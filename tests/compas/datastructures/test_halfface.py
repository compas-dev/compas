from compas.datastructures import HalfFace


# ==============================================================================
# Fixtures
# ==============================================================================

# ==============================================================================
# Tests - Schema & jsonschema
# ==============================================================================

# ==============================================================================
# Tests - Vertex Attributes
# ==============================================================================


def test_default_vertex_attributes():
    he = HalfFace(name='test', default_vertex_attributes={'a': 1, 'b': 2})
    for vertex in he.vertices():
        assert he.vertex_attribute(vertex, name='a') == 1
        assert he.vertex_attribute(vertex, name='b') == 2
        he.vertex_attribute(vertex, name='a', value=3)
        assert he.vertex_attribute(vertex, name='a') == 3


# ==============================================================================
# Tests - Face Attributes
# ==============================================================================


def test_default_face_attributes():
    he = HalfFace(name='test', default_face_attributes={'a': 1, 'b': 2})
    for face in he.vertices():
        assert he.face_attribute(face, name='a') == 1
        assert he.face_attribute(face, name='b') == 2
        he.face_attribute(face, name='a', value=3)
        assert he.face_attribute(face, name='a') == 3


# ==============================================================================
# Tests - Edge Attributes
# ==============================================================================


def test_default_edge_attributes():
    he = HalfFace(name='test', default_edge_attributes={'a': 1, 'b': 2})
    for edge in he.vertices():
        assert he.edge_attribute(edge, name='a') == 1
        assert he.edge_attribute(edge, name='b') == 2
        he.edge_attribute(edge, name='a', value=3)
        assert he.edge_attribute(edge, name='a') == 3


# ==============================================================================
# Tests - Cell Attributes
# ==============================================================================


def test_default_cell_attributes():
    he = HalfFace(name='test', default_cell_attributes={'a': 1, 'b': 2})
    for cell in he.vertices():
        assert he.cell_attribute(cell, name='a') == 1
        assert he.cell_attribute(cell, name='b') == 2
        he.cell_attribute(cell, name='a', value=3)
        assert he.cell_attribute(cell, name='a') == 3


# ==============================================================================
# Tests - Vertex Queries
# ==============================================================================

def test_vertices_where():
    hf = HalfFace(default_vertex_attributes={'a': 1, 'b': 2})
    hf.add_vertex(0)
    hf.add_vertex(1, {'a': 5})
    hf.add_vertex(2, {'a': 5, 'b': 10})
    assert list(hf.vertices_where({'a': 5})) == [1, 2]
    assert list(hf.vertices_where({'a': 1, 'b': 2}))[0] == 0


def test_vertices_where_predicate():
    hf = HalfFace(default_vertex_attributes={'a': 1, 'b': 2})
    hf.add_vertex(0)
    hf.add_vertex(1, {'a': 5, 'b': 10})
    hf.add_vertex(2, {'a': 15, 'b': 20})
    assert list(hf.vertices_where_predicate(
        lambda v, attr: attr['b'] - attr['a'] == 5)) == [1, 2]


# ==============================================================================
# Tests - Edge Queries
# ==============================================================================

def test_edges_where():
    hf = HalfFace(default_edge_attributes={'a': 1, 'b': 2})
    for vkey in range(3):
        hf.add_vertex(vkey)
    hf.add_halfface([0, 1, 2])
    hf.edge_attribute((0, 1), 'a', 5)
    assert list(hf.edges_where({'a': 1})) == [(1, 2), (2, 0)]


def test_edges_where_predicate():
    hf = HalfFace(default_edge_attributes={'a': 1, 'b': 2})
    for vkey in range(3):
        hf.add_vertex(vkey)
    hf.add_halfface([0, 1, 2])
    hf.edge_attribute((0, 1), 'a', 5)
    assert list(hf.edges_where_predicate(
        lambda e, attr: attr['a'] - attr['b'] == 3))[0] == (0, 1)


# ==============================================================================
# Tests - Face Queries
# ==============================================================================

def test_faces_where():
    hf = HalfFace(default_face_attributes={'a': 1, 'b': 2})
    for vkey in range(4):
        hf.add_vertex(vkey)
    for i in range(3):
        hf.add_halfface([i, i + 1, i + 2])
    hf.face_attribute(1, 'a', 5)
    assert list(hf.faces_where({'a': 1})) == [0, 2]


def test_faces_where_predicate():
    hf = HalfFace(default_face_attributes={'a': 1, 'b': 2})
    for vkey in range(4):
        hf.add_vertex(vkey)
    for i in range(3):
        hf.add_halfface([i, i + 1, i + 2])
    hf.face_attribute(1, 'a', 5)
    assert list(hf.faces_where_predicate(
        lambda e, attr: attr['a'] - attr['b'] == 3))[0] == 1


# ==============================================================================
# Tests - Cell Queries
# ==============================================================================

def test_cells_where():
    hf = HalfFace(default_cell_attributes={'a': 1, 'b': 2})
    for vkey in range(5):
        hf.add_vertex(vkey)
    for i in range(3):
        hf.add_cell([[i, i + 1, i + 2],
                     [i, i + 1, i + 3],
                     [i + 1, i + 2, i + 3],
                     [i + 2, i + 3, i]])
    hf.cell_attribute(1, 'a', 5)
    assert list(hf.cells_where({'a': 1})) == [0, 2]


def test_cells_where_predicate():
    hf = HalfFace(default_cell_attributes={'a': 1, 'b': 2})
    for vkey in range(5):
        hf.add_vertex(vkey)
    for i in range(3):
        hf.add_cell([[i, i + 1, i + 2],
                     [i, i + 1, i + 3],
                     [i + 1, i + 2, i + 3],
                     [i + 2, i + 3, i]])
    hf.cell_attribute(1, 'a', 5)
    assert list(hf.cells_where_predicate(
        lambda e, attr: attr['a'] - attr['b'] == 3))[0] == 1
