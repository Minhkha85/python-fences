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
            "items": self.items,
            "is_visible": self.is_visible,
            "is_rolled_up": self.is_rolled_up
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Tạo instance từ dictionary"""
        # Validate dữ liệu đầu vào
        required_fields = ['id', 'title', 'position', 'size', 'items']
        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")
                
        return cls(
            id=data["id"],
            title=data["title"],
            position=tuple(data["position"]),
            size=tuple(data["size"]),
            items=data["items"],
            is_visible=data.get("is_visible", True),
            is_rolled_up=data.get("is_rolled_up", False)
        )