import ctypes
import logging
import os
import sys

def is_admin():
    """Kiểm tra xem ứng dụng có đang chạy với quyền admin không"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin(executable_path, script_path):
    """Chạy ứng dụng với quyền admin"""
    try:
        if not is_admin():
            # Sử dụng pythonw.exe từ venv
            pythonw_path = os.path.join(os.path.dirname(sys.executable), "pythonw.exe")
            if not os.path.exists(pythonw_path):
                pythonw_path = os.path.join("venv", "Scripts", "pythonw.exe")
                
            ctypes.windll.shell32.ShellExecuteW(
                None, 
                "runas",
                pythonw_path,
                script_path,
                None,
                1
            )
            return True
    except Exception as e:
        logging.error(f"Error running as admin: {e}")
        return False 