import sys
import logging
import os
import ctypes
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
    try:
        app = QApplication(sys.argv)
        
        # Tạo main window
        window = MainWindow()
        window.show()
        
        # Xử lý tham số dòng lệnh
        window.handle_command_line()
        
        # Chạy ứng dụng
        sys.exit(app.exec())
        
    except Exception as e:
        logging.exception("Application error:")

if __name__ == "__main__":
    main()