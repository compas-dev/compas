import pytest

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
    graph.validate_data()


def graph_json_schema(graph):
    graph.validate_json()
