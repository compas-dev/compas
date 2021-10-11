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
