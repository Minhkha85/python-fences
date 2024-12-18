from PyQt6.QtCore import Qt
from win32gui import GetWindowText, GetForegroundWindow
import win32gui
import win32con
import logging

class DesktopController:
    @staticmethod
    def is_on_desktop():
        """Kiểm tra xem cửa sổ hiện tại có phải là desktop không"""
        try:
            foreground_window = win32gui.GetForegroundWindow()
            
            # Kiểm tra xem có phải là desktop hoặc Program Manager không
            progman = win32gui.FindWindow("Progman", None)
            if foreground_window == progman:
                return True
            
            # Kiểm tra WorkerW (desktop window)
            def enum_windows(hwnd, results):
                if win32gui.IsWindowVisible(hwnd):
                    if "WorkerW" == win32gui.GetClassName(hwnd):
                        results.append(hwnd)
            
            results = []
            win32gui.EnumWindows(enum_windows, results)
            
            # Kiểm tra xem foreground window có phải là một trong các WorkerW không
            for worker_w in results:
                if foreground_window == worker_w:
                    return True
                
            # Kiểm tra tên cửa sổ
            window_text = win32gui.GetWindowText(foreground_window)
            if not window_text or "Program Manager" in window_text:
                return True
            
            return False
            
        except Exception as e:
            logging.error(f"Error checking desktop state: {e}")
            return False

    @staticmethod
    def set_window_always_on_desktop(hwnd):
        """Đặt cửa sổ luôn hiển thị trên desktop"""
        try:
            # Tìm handle của Program Manager
            progman = win32gui.FindWindow("Progman", None)
            if progman:
                # Set parent cho cửa sổ thành Program Manager
                win32gui.SetParent(hwnd, progman)
                win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
                return True
            return False
        except Exception as e:
            logging.error(f"Error setting window on desktop: {e}")
            return False
