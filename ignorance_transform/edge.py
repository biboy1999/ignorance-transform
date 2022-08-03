from uuid import uuid4
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ignorance_transform.node import Node
from ignorance_transform.logger import warning


schema = {
    "$schema": "https://json-schema.org/draft/2020-12",
    "type": "object",
    "properties": {
        "source": {"type": "string"},
        "target": {"type": "string"},
        "id": {"type": "string"}
    },
    "required": ["source", "target", "id"]
}


class Edge():

    def __init__(self, json={}) -> None:
        self.data = {}
        self._target: "Node" = None
        self._source: "Node" = None

        self.modified = False
        self.excluded = False

        if json:
            self.parse(json)

    # josn data part
    @property
    def id(self):
        return self.data.get("id", None)

    @id.setter
    def id(self, value):
        self.data["id"] = value

    @property
    def source_id(self):
        return self.data.get("source", None)

    @property
    def target_id(self):
        return self.data.get("target", None)

    @property
    def label(self):
        return self.data.get("label", None)

    @label.setter
    def label(self, value):
        self.data["label"] = value

    # node for easy traversal?
    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, value: "Node"):
        self._srouce = value
        self.data["source"] = value.id

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, value: "Node"):
        self._target = value
        self.data["target"] = value.id

    def __setattr__(self, name: str, value) -> None:
        self.__dict__["modified"] = True
        super().__setattr__(name, value)

    def parse(self, json: dict) -> None:
        self.data = json
        self.modified = False

    def update_data(self, data: dict) -> None:
        if data:
            self.modified = True
            self.data.update(data)

    def to_dict(self) -> dict:
        result = {}
        result["id"] = self.id if self.id else str(uuid4)
        if not self.source_id:
            warning(f"[-] Edge \"{self.id}\" no source provided, skipping")
            return {}
        if not self.target_id:
            warning(f"[-] Edge \"{self.id}\" no target provided, skipping")
            return {}
        result["source"] = self.source_id
        result["target"] = self.target_id
        result["label"] = self.label
        result.update(self.data)
        print(result, self.label)
        return result


if __name__ == "__main__":
    edge = Edge()
    edge.parse({"target": "zxcv"})
    # edge.update_data({"source": "idk", "target": "no"})

    print(edge.to_dict(), edge.modified)
