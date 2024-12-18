import json
import os
from typing import List
from models.fence import Fence

class ConfigService:
    def __init__(self):
        self.config_file = "fences_config.json"
        # Tạo file config mặc định nếu chưa tồn tại
        if not os.path.exists(self.config_file):
            self.create_default_config()
        
    def create_default_config(self):
        """Tạo file config mặc định"""
        default_config = {
            'fences': []
        }
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=4)
            
    def save_fences(self, fences: List[Fence]):
        config = {
            'fences': [
                {
                    'id': fence.id,
                    'title': fence.title,
                    'position': fence.position,
                    'size': fence.size,
                    'items': fence.items,
                    'is_visible': fence.is_visible,
                    'is_rolled_up': fence.is_rolled_up
                }
                for fence in fences
            ]
        }
        
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4)
            
    def load_fences(self) -> List[Fence]:
        try:
            if not os.path.exists(self.config_file):
                self.create_default_config()
                return []
                
            with open(self.config_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if not content.strip():  # Nếu file rỗng
                    self.create_default_config()
                    return []
                    
                config = json.loads(content)
                return [
                    Fence(**fence_data)
                    for fence_data in config.get('fences', [])
                ]
                
        except json.JSONDecodeError:
            # Nếu file JSON không hợp lệ, tạo mới
            self.create_default_config()
            return []
        except Exception as e:
            print(f"Error loading fences: {e}")
            return []