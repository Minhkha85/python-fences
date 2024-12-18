from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class Fence:
    id: str
    title: str
    position: Tuple[int, int]
    size: Tuple[int, int]
    items: List[str]
    is_visible: bool = True
    is_rolled_up: bool = False
    
    def add_item(self, item_path: str):
        if item_path not in self.items:
            self.items.append(item_path)
            
    def remove_item(self, item_path: str):
        if item_path in self.items:
            self.items.remove(item_path)
            
    def toggle_rollup(self):
        self.is_rolled_up = not self.is_rolled_up

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "position": self.position,
            "size": self.size,
            "items": [{"path": item["path"], "name": item["name"]} for item in self.items]
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get("id"),
            title=data.get("title"),
            position=tuple(data.get("position", (0, 0))),
            size=tuple(data.get("size", (300, 400))),
            items=data.get("items", [])
        )