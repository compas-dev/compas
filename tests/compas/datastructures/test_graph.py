import pytest

import compas
from compas.datastructures import Graph


# ==============================================================================
# Fixtures
# ==============================================================================


@pytest.fixture
def graph():
    edges = [[0, 1], [0, 2], [0, 3], [0, 4]]
    graph = Graph()
    for u, v in edges:
        graph.add_edge(u, v)
    return graph


# ==============================================================================
# Tests - Schema & JSONSchema
# ==============================================================================


def test_data_schema(graph):
    if compas.IPY:
        return

    graph.validate_data()


def test_graph_json_schema(graph):
    if compas.IPY:
        return

    graph.validate_json()


def test_graph_networkx_conversion():
    if compas.IPY:
        return

    g = Graph()
    g.add_node(0)
    g.add_node(1, weight=1.2, height='test')
    g.add_node(2, x=1, y=1, z=0)

    g.add_edge(0, 1, attr_value=10)
    g.add_edge(1, 2)

    nxg = g.to_networkx()

    assert set(nxg.nodes()) == set(g.nodes()), "Node sets must match"
    assert nxg.nodes[1]['weight'] == 1.2, "Node attributes must be preserved"
    assert nxg.nodes[1]['height'] == "test", "Node attributes must be preserved"
    assert nxg.nodes[2]['x'] == 1, "Node attributes must be preserved"

    assert set(nxg.edges()) == set(((0, 1), (1, 2))), "Edge sets must match"
    assert nxg.edges[0, 1]['attr_value'] == 10, "Edge attributes must be preserved"

    g2 = Graph.from_networkx(nxg)

    assert g.number_of_nodes() == g2.number_of_nodes()
    assert g.number_of_edges() == g2.number_of_edges()
    assert g2.edge_attribute((0, 1), 'attr_value') == 10
