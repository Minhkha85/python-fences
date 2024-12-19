import sys
import logging
import os
import ctypes
import win32event
import win32api
import winerror
from PyQt6.QtWidgets import QApplication
from views.main_window import MainWindow
from utils.admin_utils import is_admin, run_as_admin

# Thiết lập logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('debug.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

def main():
    # Tạo mutex để kiểm tra instance
    mutex = win32event.CreateMutex(None, 1, "PythonFences_Mutex")
    if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
        mutex = None
        print("Application is already running!")
        sys.exit(1)

    try:
        app = QApplication(sys.argv)
        
        # Ngăn ứng dụng thoát khi đóng cửa sổ cuối cùng
        app.setQuitOnLastWindowClosed(False)
        
        window = MainWindow()
        window.show()
        window.lower()  # Đảm bảo cửa sổ ở dưới cùng
        
        # Xử lý tham số dòng lệnh
        window.handle_command_line()
        
        sys.exit(app.exec())
        
    except Exception as e:
        logging.exception("Application error:")
    finally:
        if mutex:
            win32api.CloseHandle(mutex)

if __name__ == "__main__":
    main()