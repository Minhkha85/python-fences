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

# Thiết lập logging chi tiết hơn
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('debug.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

def main():
    try:
        # Xử lý tham số --register-context-menu
        if "--register-context-menu" in sys.argv:
            app = QApplication(sys.argv)
            window = MainWindow()
            window.register_context_menu()
            return 0

        # Tạo mutex để kiểm tra instance
        mutex = win32event.CreateMutex(None, 1, "PythonFences_Mutex")
        last_error = win32api.GetLastError()
        
        # Nếu đã có instance và có tham số --new-fence
        if last_error == winerror.ERROR_ALREADY_EXISTS and "--new-fence" in sys.argv:
            # Cho phép tạo fence mới
            app = QApplication(sys.argv)
            window = MainWindow()
            window.handle_command_line()
            return 0
            
        # Nếu đã có instance và không có tham số đặc biệt
        elif last_error == winerror.ERROR_ALREADY_EXISTS:
            logging.warning("Application is already running!")
            return 1

        # Instance đầu tiên
        app = QApplication(sys.argv)
        app.setQuitOnLastWindowClosed(False)
        
        window = MainWindow()
        window.show()
        window.lower()
        
        return app.exec()

    except Exception as e:
        logging.exception("Application error:")
        return 1
    finally:
        if 'mutex' in locals() and mutex:
            win32api.CloseHandle(mutex)

if __name__ == "__main__":
    sys.exit(main())