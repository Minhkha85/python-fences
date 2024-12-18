import ctypes
import logging

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
            ctypes.windll.shell32.ShellExecuteW(
                None, 
                "runas",
                executable_path,
                f'"{script_path}"',
                None,
                1
            )
            return True
    except Exception as e:
        logging.error(f"Error running as admin: {e}")
        return False 