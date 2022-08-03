from uuid import uuid4

from ignorance_transform.edge import Edge

schema = {
    "$schema": "https://json-schema.org/draft/2020-12",

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


class Node():

    def __init__(self, json={}) -> None:
        self.data: dict = {}
        self.position: dict = None

        self.outgoing_edge: "list[Edge]" = []
        self.incoming_edge: "list[Edge]" = []

        self.modified = False
        self.excluded = False

        if json:
            self.parse(json)
        else:
            self.id = str(uuid4())

    @property
    def id(self):
        return self.data.get("id", None)

    @id.setter
    def id(self, value):
        if not self.data:
            self.data = {}
        self.data["id"] = value

    @property
    def label(self):
        return self.data.get("label", None)

    @label.setter
    def label(self, value):
        if not self.data:
            self.data = {}
        self.data["label"] = value

    def __setattr__(self, name: str, value) -> None:
        self.__dict__["modified"] = True
        super().__setattr__(name, value)

    def parse(self, json: dict) -> None:
        self.data = json.get("data", None)
        self.position = json.get("position", None)
        self.modified = False

    def set_position(self, x: int, y: int) -> None:
        self.position = {"x": x, "y": y}
        pass

    def update_data(self, data: dict) -> None:
        if not self.data:
            self.data = data
        elif data:
            self.modified = True
            self.data.update(data)

    def link_to(self, node: "Node", label="", id=None) -> Edge:
        edge = Edge()
        edge.id = id if id else str(uuid4())
        edge.label = label if label else ""
        edge.source = self
        edge.target = node
        self.outgoing_edge.append(edge)
        return edge

    def to_dict(self) -> dict:
        result = {}
        if self.data:
            self.data["id"] = self.id if self.id else str(uuid4())
            self.data["label"] = self.label if self.label else ""
            result["data"] = self.data
        if self.position:
            result["position"] = self.position
        return result


if __name__ == "__main__":
    node = Node()
    node.parse({"data": {"id": "a"}})
    node.update_data({"test": "test", "label": "tee"})
    # node.modified = False
    print(node.to_dict(), node.modified)
