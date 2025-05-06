from src.backend.schemas.schemas_graph import (NodeSchema, EdgeSchema,
                                               GraphSchema, ResponseGraphSchema,
                                               ListGraphsSchema)


def test_create_node_schema_with_valid_name():
    node_name = "test_node"
    node = NodeSchema(name=node_name)

    assert node.name == node_name
    assert isinstance(node, NodeSchema)


def test_create_edge_schema_with_valid_strings(self):
    edge = EdgeSchema(source="node1", target="node2")

    assert edge.source == "node1"
    assert edge.target == "node2"

def test_create_valid_graph_schema():
        nodes = [
            NodeSchema(name="node1"),
            NodeSchema(name="node2"),
            NodeSchema(name="node3")
        ]

        edges = [
            EdgeSchema(source="node1", target="node2"),
            EdgeSchema(source="node2", target="node3")
        ]

        graph = GraphSchema(nodes=nodes, edges=edges)

        assert len(graph.nodes) == 3
        assert len(graph.edges) == 2
        assert graph.nodes[0].name == "node1"
        assert graph.edges[0].source == "node1"
        assert graph.edges[0].target == "node2"


def test_create_valid_response_graph_schema():
    nodes = [NodeSchema(name="node1"), NodeSchema(name="node2")]
    edges = [EdgeSchema(source="node1", target="node2")]
    graph = GraphSchema(nodes=nodes, edges=edges)

    response = ResponseGraphSchema(graph_id=1, graph=graph)

    assert response.graph_id == 1
    assert len(response.graph.nodes) == 2
    assert len(response.graph.edges) == 1
    assert response.graph.nodes[0].name == "node1"
    assert response.graph.edges[0].source == "node1"
    assert response.graph.edges[0].target == "node2"


def test_valid_adjacency_list():
        adjacency_list = {
            "A": ["B", "C"],
            "B": ["A", "D"],
            "C": ["A"],
            "D": ["B"]
        }

        graph_schema = ListGraphsSchema(adjacency_list=adjacency_list)

        assert graph_schema.adjacency_list == adjacency_list
        assert graph_schema.adjacency_list["A"] == ["B", "C"]
        assert graph_schema.adjacency_list["B"] == ["A", "D"]
        assert graph_schema.adjacency_list["C"] == ["A"]
        assert graph_schema.adjacency_list["D"] == ["B"]