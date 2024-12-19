from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
    QMenu, QInputDialog, QApplication, QSystemTrayIcon, QStyle)
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QAction, QScreen, QIcon, QPixmap, QCursor
from .fence_widget import FenceWidget
from models.fence import Fence
from utils.admin_utils import is_admin, run_as_admin  # Thay đổi import
from uuid import uuid4
import winreg
import os
import sys
import logging
import json
import shutil
import argparse
from utils.color_utils import color_from_string

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Đặt working directory về thư mục gốc của ứng dụng
        app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        os.chdir(app_dir)
        
        # Tạo thư mục shortcuts nếu chưa tồn tại
        os.makedirs(os.path.join(app_dir, "shortcuts"), exist_ok=True)
        
        self.setWindowTitle("Python Fences")
        
        # Đặt cửa sổ toàn màn hình và trong suốt
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Lấy kích thước màn hình
        screen = QApplication.primaryScreen().geometry()
        self.setGeometry(screen)
        
        # Main widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Layout
        self.layout = QVBoxLayout(self.central_widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        # Initialize fences list
        self.fences = []
        
        # Thiết lập system tray
        self.setup_system_tray()
        
        # Đăng ký context menu cho desktop
        self.register_context_menu()
        
        # Load existing fences
        self.load_fences()
        
        # Show the window
        self.show()

    def create_new_fence_at_cursor(self):
        try:
            cursor_pos = QCursor.pos()
            logging.info(f"Creating new fence at position: {cursor_pos.x()}, {cursor_pos.y()}")
            
            # Tạo fence mới với danh sách items rỗng
            new_fence = Fence(
                id=str(uuid4()),
                title="New Fence",
                position=(cursor_pos.x() - 150, cursor_pos.y() - 200),  # Điều chỉnh vị trí để fence không bị che con trỏ
                size=(300, 400),
                items=[]
            )
            
            # Tạo widget cho fence
            fence_widget = FenceWidget(new_fence, self.central_widget)
            fence_widget.move(new_fence.position[0], new_fence.position[1])
            fence_widget.show()
            fence_widget.raise_()
            
            # Thêm vào danh sách
            self.fences.append(fence_widget)
            
            # Lưu cấu hình
            self.save_fences()
            
            logging.info("New fence created successfully")
            
        except Exception as e:
            logging.error(f"Error creating new fence: {e}", exc_info=True)

    def setup_system_tray(self):
        """Thiết lập system tray icon và menu"""
        # Thêm đoạn code load icon từ file
        icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "fence_icon.ico")
        if os.path.exists(icon_path):
            self.tray_icon = QSystemTrayIcon(QIcon(icon_path), self)
        else:
            # Fallback to default icon
            self.tray_icon = QSystemTrayIcon(self)
            self.tray_icon.setIcon(QApplication.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon))
        
        # Tạo menu cho system tray
        tray_menu = QMenu()
        
        # Action tạo fence mới
        new_fence_action = QAction("New Fence", self)
        new_fence_action.triggered.connect(self.create_new_fence_at_cursor)
        tray_menu.addAction(new_fence_action)
        
        # Show All Fences action
        show_all_action = QAction("Show All Fences", self)
        show_all_action.triggered.connect(self.show_all_fences)
        tray_menu.addAction(show_all_action)
        
        # Separator
        tray_menu.addSeparator()
        
        # Thêm About vào menu
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        tray_menu.addAction(about_action)
        
        # Action thoát
        quit_action = QAction("Exit", self)
        quit_action.triggered.connect(QApplication.quit)
        tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        
        # Kiểm tra cập nhật khi khởi động
        self.check_updates_on_startup()
        
        logging.info("System tray setup completed")

    def handle_tray_activation(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.create_new_fence_at_cursor()

    def register_context_menu(self):
        """Đăng ký context menu cho desktop"""
        try:
            if not is_admin():
                logging.warning("Skipping context menu registration - not running as admin")
                return False
            
            key_path = r"Directory\Background\shell\PythonFences"
            command_path = os.path.join(key_path, "command")
            
            try:
                # Xóa key cũ nếu tồn tại
                try:
                    winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, command_path)
                    winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, key_path)
                except WindowsError:
                    pass
                
                # Tạo key cho menu item
                winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, key_path)
                key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, key_path, 0, 
                                   winreg.KEY_WRITE)
                winreg.SetValueEx(key, "", 0, winreg.REG_SZ, "New Fence Here")
                
                # Thay đổi icon - sử dụng icon của bạn
                icon_path = os.path.abspath("assets/fence_icon.ico")  # Đặt icon của bạn trong thư mục assets
                winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, icon_path)
                winreg.CloseKey(key)
                
                # Tạo key cho command
                winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, command_path)
                key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, command_path, 0, 
                                   winreg.KEY_WRITE)
                
                # Sử dụng pythonw.exe để tránh hiển thị terminal
                pythonw_path = os.path.join(os.path.dirname(sys.executable), "pythonw.exe")
                cmd = f'"{pythonw_path}" "{os.path.abspath(sys.argv[0])}" --new-fence'
                winreg.SetValueEx(key, "", 0, winreg.REG_SZ, cmd)
                winreg.CloseKey(key)
                
                logging.info("Context menu registered successfully")
                return True
                
            except Exception as e:
                logging.error(f"Error creating registry keys: {e}")
                return False
                
        except Exception as e:
            logging.error(f"Error registering context menu: {e}")
            return False

    def handle_command_line(self):
        """Xử lý các tham số dòng lệnh"""
        parser = argparse.ArgumentParser()
        parser.add_argument('--new-fence', help='Create new fence at specified location')
        args = parser.parse_args()
        
        if args.new_fence:
            # Lấy vị trí chuột hiện tại
            cursor_pos = QCursor.pos()
            self.create_new_fence_at_cursor()

    def closeEvent(self, event):
        self.cleanup_registry()
        self.tray_icon.hide()
        super().closeEvent(event)

    def save_fences(self):
        try:
            fences_data = []
            for fence in self.fences:
                if isinstance(fence, FenceWidget):
                    fences_data.append({
                        'id': fence.fence.id,
                        'title': fence.fence.title,
                        'position': (fence.x(), fence.y()),
                        'size': (fence.width(), fence.height()),
                        'items': fence.fence.items,
                        'is_visible': fence.isVisible(),
                        'is_rolled_up': fence.fence.is_rolled_up
                    })
            
            with open("fences_config.json", "w", encoding='utf-8') as f:
                json.dump(fences_data, f, indent=4, ensure_ascii=False)
            logging.info("Fences saved successfully")
        except Exception as e:
            logging.error(f"Error saving fences: {e}", exc_info=True)

    def load_fences(self):
        try:
            # Kiểm tra file tồn tại
            if not os.path.exists("fences_config.json"):
                # Tạo file mới với mảng rỗng
                with open("fences_config.json", "w", encoding='utf-8') as f:
                    json.dump([], f, indent=4)
                return

            # Đọc file
            with open("fences_config.json", "r", encoding='utf-8') as f:
                content = f.read().strip()
                if not content:  # Nếu file rỗng
                    with open("fences_config.json", "w", encoding='utf-8') as f:
                        json.dump([], f, indent=4)
                    return

                fences_data = json.loads(content)
                if fences_data:  # Nếu có dữ liệu
                    for fence_data in fences_data:
                        fence = Fence.from_dict(fence_data)
                        self.add_fence(fence)
                    logging.info("Fences loaded successfully")

        except Exception as e:
            logging.error(f"Error loading fences: {e}", exc_info=True)
            # Nếu có lỗi, tạo file mới
            with open("fences_config.json", "w", encoding='utf-8') as f:
                json.dump([], f, indent=4)

    def add_fence(self, fence):
        fence_widget = FenceWidget(fence)
        fence_widget.move(fence.position[0], fence.position[1])
        fence_widget.resize(fence.size[0], fence.size[1])
        self.fences.append(fence_widget)
        fence_widget.setParent(self.centralWidget())
        fence_widget.show()

    def delete_fence(self, fence_widget):
        """Xóa fence và di chuyển các shortcut ra desktop"""
        try:
            # Di chuyển tất cả shortcut ra desktop
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            for item in fence_widget.fence.items:
                if item["path"].lower().endswith('.lnk'):
                    try:
                        new_path = os.path.join(desktop_path, os.path.basename(item["path"]))
                        shutil.move(item["path"], new_path)
                        logging.debug(f"Moved shortcut back to desktop: {new_path}")
                    except Exception as e:
                        logging.error(f"Error moving shortcut: {e}")
            
            # Xóa fence
            self.fences.remove(fence_widget)
            fence_widget.deleteLater()
            self.save_fences()
            logging.info("Fence deleted successfully")
        except Exception as e:
            logging.error(f"Error deleting fence: {e}")

    def show_all_fences(self):
        """Hiện tất cả các fences đã bị ẩn"""
        for fence in self.fences:
            fence.show()

    def try_register_context_menu(self):
        """Thử đăng ký context menu với xử lý quyền admin"""
        try:
            # Kiểm tra quyền admin
            if not self.is_admin():
                logging.warning("Application needs admin rights to register context menu")
                return

            key_path = r"Directory\\Background\\shell\\NewFence"
            try:
                # Thử mở key trước để kiểm tra xem đã tồn tại chưa
                winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, key_path, 0, 
                             winreg.KEY_READ | winreg.KEY_WRITE)
            except WindowsError:
                # Key chưa tồn tại, tạo mới
                key = winreg.CreateKeyEx(winreg.HKEY_CLASSES_ROOT, key_path, 0, 
                                       winreg.KEY_WRITE)
                winreg.SetValueEx(key, "", 0, winreg.REG_SZ, "New Fence Here")
                winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, 
                                sys.executable)
                
                # Tạo command key
                command_key = winreg.CreateKeyEx(key, "command", 0, 
                                               winreg.KEY_WRITE)
                winreg.SetValueEx(command_key, "", 0, winreg.REG_SZ, 
                                f'"{sys.executable}" "%V"')
                
                winreg.CloseKey(command_key)
                winreg.CloseKey(key)
                logging.info("Context menu registered successfully")
                
        except Exception as e:
            logging.error(f"Error registering context menu: {e}")

    @staticmethod
    def is_admin():
        """Kiểm tra xem ứng dụng có đang chạy với quyền admin không"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    @staticmethod
    def run_as_admin():
        """Chạy lại ứng dụng với quyền admin"""
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1)

    def cleanup_registry(self):
        """Dọn dẹp registry khi đóng ứng dụng"""
        try:
            # Xóa context menu registration nếu có
            if hasattr(self, 'context_menu_registered'):
                # Code xóa registry ở đây
                pass
        except Exception as e:
            logging.error(f"Error cleaning up registry: {e}")

    def register_context_menu_as_admin(self):
        """Đăng ký context menu với quyền admin"""
        if not is_admin():
            run_as_admin(sys.executable, os.path.abspath(sys.argv[0]))
        else:
            self.register_context_menu()

    def show_about(self):
        """Hiển thị dialog About"""
        from views.about_dialog import AboutDialog
        dialog = AboutDialog(self)
        dialog.exec()

    def check_updates_on_startup(self):
        """Kiểm tra cập nhật khi khởi động"""
        # Tạm thời comment lại để test
        # self.update_checker = UpdateChecker()
        # self.update_checker.update_available.connect(self.show_update_dialog)
        # self.update_checker.start()
        pass