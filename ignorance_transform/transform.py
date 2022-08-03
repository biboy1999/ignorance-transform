from ignorance_transform.edge import Edge
from ignorance_transform.node import Node

schema = {
    "$schema": "https://json-schema.org/draft/2020-12",

    "type": "object",
    "properties": {
        "nodes": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "data": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"}
                        },
                        "required": ["id"]
                    },
                    "position": {
                        "type": "object",
                        "properties": {
                            "x": {"type": "number"},
                            "y": {"type": "number"},
                        },
                        "required": ["x", "y"]
                    },
                },
                "required": ["data"]
            }
        },
        "edges": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "source": {"type": "string"},
                    "target": {"type": "string"},
                    "id": {"type": "string"}
                },
                "required": ["source", "target", "id"]
            }
        },
        "parameter ": {
            "type": "object",
            "properties": {}
        },
    }
}


class Transform():

    def __init__(self, json: dict) -> None:
        self.nodes: "list[Node]" = []
        self.edges: "list[Edge]" = []
        self.parameter = {}

        self.added_nodes: "list[Node]" = []
        self.added_edges: "list[Edge]" = []

        cache: dict[str, "Node"] = {}
        for node_json in json.get("nodes", []):
            node = Node(node_json)
            self.nodes.append(node)
            cache[node.id] = node
        for edge_json in json.get("edges", []):
            edge = Edge(edge_json)
            source_node = cache[edge.source_id]
            target_node = cache[edge.target_id]
            edge.source = source_node
            edge.target = target_node
            self.edges.append(edge)

            source_node.outgoing_edge.append(edge)
            target_node.incoming_edge.append(edge)

            edge.modified = False

        self.parameter = json.get("parameter", {})

    def add_node(self, node: "Node") -> None:
        self.added_nodes.append(node)

    def add_edge(self, edge: "Edge") -> None:
        self.added_edges.append(edge)

    def to_dict(self) -> str:
        change = {
            "nodes": [],
            "edges": [],
            "removeIds": [],
            "relation": [],
        }
        for node in self.nodes:
            if node.excluded or not node.modified:
                continue
            change["nodes"].append(node.to_dict())
        for node in self.added_nodes:
            change["nodes"].append(node.to_dict())

        for edge in self.edges:
            if edge.excluded or not edge.modified:
                continue
            change["edges"].append(edge.to_dict())
        for edge in self.added_edges:
            change["edges"].append(edge.to_dict())

        return change
