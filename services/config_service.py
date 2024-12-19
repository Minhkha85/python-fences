import json
import os
import sys
from typing import List
from models.fence import Fence
import logging

class ConfigService:
    def __init__(self):
        # Lấy đường dẫn thư mục cài đặt
        if getattr(sys, 'frozen', False):
            # Nếu đang chạy từ file exe
            self.app_dir = os.path.dirname(sys.executable)
        else:
            # Nếu đang chạy từ source code
            self.app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
        # File config sẽ được lưu trong thư mục cài đặt
        self.config_file = os.path.join(self.app_dir, "fences_config.json")
        
        # Tạo file config mặc định nếu chưa tồn tại
        if not os.path.exists(self.config_file):
            self.create_default_config()
        
    def create_default_config(self):
        """Tạo file config mặc định"""
        default_config = {
            'fences': []
        }
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=4)
        except Exception as e:
            print(f"Error creating config file: {e}")
            
    def save_fences(self, fences: List[dict]):
        """Lưu danh sách fences"""
        config = {
            'fences': [
                {
                    'id': fence['id'],
                    'title': fence['title'],
                    'position': fence['position'],
                    'size': fence['size'],
                    'items': fence['items'],
                    'is_visible': fence['is_visible'],
                    'is_rolled_up': fence['is_rolled_up']
                }
                for fence in fences
            ]
        }
        
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4)
            
    def load_fences(self) -> List[dict]:
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
                return config.get('fences', [])
                
        except json.JSONDecodeError:
            # Nếu file JSON không hợp lệ, tạo mới
            self.create_default_config()
            return []
        except Exception as e:
            logging.error(f"Error loading fences: {e}")
            return []