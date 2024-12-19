import os
import sys
import win32api
import win32con
import win32gui
import win32ui
from ctypes import windll, byref, create_unicode_buffer, sizeof
from win32com.shell import shell, shellcon
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QMenu, 
                           QInputDialog, QLineEdit, QFrame, QGridLayout,
                           QApplication, QStyle, QPushButton, QHBoxLayout,
                           QFileIconProvider)
from PyQt6.QtCore import (Qt, QMimeData, QPoint, QSize, QRect, 
                         QUrl, QEvent, QFileInfo, QTimer)
from PyQt6.QtGui import (QDragEnterEvent, QDropEvent, QResizeEvent, 
                        QMouseEvent, QPainter, QColor, QPalette, QIcon,
                        QDrag, QCursor, QPixmap, QImage, QPen, QAction)
from controllers.desktop_controller import DesktopController
import logging
import win32com.client
import pythoncom
import shutil
import win32con
import win32gui
from win32com.shell import shell as shell32
from utils.color_utils import color_from_string

class FenceWidget(QWidget):
    # Định nghĩa các vùng resize
    EDGE_NONE = 0
    EDGE_TOP = 1
    EDGE_BOTTOM = 2
    EDGE_LEFT = 4
    EDGE_RIGHT = 8

    def __init__(self, fence, parent=None):
        super().__init__(parent)
        self.fence = fence
        
        # Thêm các thuộc tính cho theme
        self.themes = {
    "Crystal": {
        "bg_color": "rgba(255, 255, 255, 8)",
        "border_color": "rgba(255, 255, 255, 20)",
        "item_bg_color": "transparent",
        "item_hover_color": "rgba(255, 255, 255, 12)",
        "item_border_color": "rgba(255, 255, 255, 20)",
        "text_color": "white",
        "header_bg": "rgba(255, 255, 255, 12)",
        "opacity": 0.65
    },
    "Pearl": {
        "bg_color": "rgba(240, 240, 245, 10)",
        "border_color": "rgba(255, 255, 255, 25)",
        "item_bg_color": "transparent",
        "item_hover_color": "rgba(255, 255, 255, 15)",
        "item_border_color": "rgba(255, 255, 255, 25)",
        "text_color": "white",
        "header_bg": "rgba(245, 245, 250, 15)",
        "opacity": 0.7
    },
    "Moonlight": {
        "bg_color": "rgba(220, 225, 235, 8)",
        "border_color": "rgba(255, 255, 255, 22)",
        "item_bg_color": "transparent",
        "item_hover_color": "rgba(255, 255, 255, 12)",
        "item_border_color": "rgba(255, 255, 255, 22)",
        "text_color": "white",
        "header_bg": "rgba(225, 230, 240, 12)",
        "opacity": 0.68
    },
    "Silk": {
        "bg_color": "rgba(245, 245, 245, 6)",
        "border_color": "rgba(255, 255, 255, 18)",
        "item_bg_color": "transparent",
        "item_hover_color": "rgba(255, 255, 255, 10)",
        "item_border_color": "rgba(255, 255, 255, 18)",
        "text_color": "white",
        "header_bg": "rgba(248, 248, 248, 10)",
        "opacity": 0.62
    },
    "Night": {
        "bg_color": "rgba(20, 20, 22, 15)",
        "border_color": "rgba(255, 255, 255, 15)",
        "item_bg_color": "transparent",
        "item_hover_color": "rgba(255, 255, 255, 8)",
        "item_border_color": "rgba(255, 255, 255, 15)",
        "text_color": "white",
        "header_bg": "rgba(25, 25, 28, 20)",
        "opacity": 0.75
    },
    "Golden Glass": {  # Thêm theme mới
        "bg_color": "rgba(255, 215, 0, 6)",  # Màu vàng nhạt
        "border_color": "rgba(255, 223, 0, 20)",
        "item_bg_color": "transparent",
        "item_hover_color": "rgba(255, 223, 0, 12)",
        "item_border_color": "rgba(255, 223, 0, 20)",
        "text_color": "white",
        "header_bg": "rgba(255, 215, 0, 10)",
        "header_color": "rgba(255, 223, 0, 15)",
        "opacity": 0.55  # Độ trong suốt cao hơn
    },
    "Amber Glow": {  # Thêm theme màu vàng cam
        "bg_color": "rgba(255, 191, 0, 8)",
        "border_color": "rgba(255, 196, 0, 22)",
        "item_bg_color": "transparent",
        "item_hover_color": "rgba(255, 196, 0, 15)",
        "item_border_color": "rgba(255, 196, 0, 22)",
        "text_color": "white",
        "header_bg": "rgba(255, 191, 0, 12)",
        "opacity": 0.6
    }
}
        
        # Mặc định theme Crystal
        self.current_theme = "Golden Glass"
        
        # Thêm các thuộc tính cho layout
        self.layout_modes = ["Grid", "List", "Compact"]
        self.current_layout = "Grid"
        
        # Thêm thuộc tính cho icon size
        self.icon_sizes = {"Small": 32, "Medium": 48, "Large": 64}
        self.icon_size = self.icon_sizes["Medium"]  # Mặc định size Medium
        
        # Thêm thuộc tính layout orientation
        self.vertical_layout = True  # True: dọc, False: ngang
        
        # Khởi tạo các biến resize
        self.resize_area_size = 5  # Kích thước vùng resize
        self.resize_edge = self.EDGE_NONE
        
        # Khởi tạo các biến màu sắc
        self.background_color = QColor(0, 0, 0, 30)
        self.border_color = QColor(255, 255, 255, 30)
        self.highlight_color = QColor(255, 255, 255, 50)
        
        # Khởi tạo các biến khác
        self.original_parent = parent
        self.is_dragging = False
        self.drag_start_pos = None
        self.dragging_item = None
        self.dragging_widget = None
        self.is_rolled_up = False
        self.always_on_desktop = False
        self.normal_height = 400  # Chiều cao mặc định
        
        # Thiết lập window flags và thuộc tính
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.Tool |
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        self.setAcceptDrops(True)
        self.setMouseTracking(True)  # Để nhận các event di chuột
        
        # Khởi tạo layout chính
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(5, 5, 5, 5)
        self.layout.setSpacing(0)
        
        # Khởi tạo các thành phần UI
        self.setup_header()
        self.setup_content_area()
        
        # Áp dụng theme sau khi đã tạo UI
        self.apply_theme(self.current_theme)
        
        # Thiết lập kích thước ban đầu
        self.setGeometry(
            fence.position[0], fence.position[1],
            fence.size[0], fence.size[1]
        )
        
        # Refresh items
        self.refresh_items()

    def setup_header(self):
        self.header = QFrame()
        self.header.setFixedHeight(35)  # Tăng chiều cao header
        
        header_layout = QHBoxLayout(self.header)
        header_layout.setContentsMargins(10, 6, 10, 6)  # Tăng padding
        header_layout.setSpacing(6)
        
        # Title label với font và style mới
        self.title_label = QLabel(self.fence.title)
        self.title_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 13px;
                font-weight: 500;
                font-family: 'Segoe UI', sans-serif;
            }
        """)
        
        # Thêm các nút điều khiển
        self.btn_minimize = QPushButton("─")
        self.btn_minimize.setFixedSize(26, 26)  # Tăng kích thước nút
        self.btn_minimize.clicked.connect(self.toggle_rollup)
        self.btn_minimize.setStyleSheet("""
            QPushButton {
                color: white;
                background: transparent;
                border: none;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 15);
                border-radius: 4px;
            }
        """)
        
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.btn_minimize)
        
        self.layout.addWidget(self.header)

    def setup_content_area(self):
        """Thiết lập vùng chứa nội dung"""
        self.content_area = QFrame(self)
        self.content_area.setStyleSheet("""
            QFrame {
                background-color: transparent;
                border-radius: 5px;
            }
        """)
        
        # Sử dụng QGridLayout cho items
        self.grid_layout = QGridLayout(self.content_area)
        self.grid_layout.setSpacing(10)
        self.grid_layout.setContentsMargins(10, 10, 10, 10)
        
        self.layout.addWidget(self.content_area)

    def refresh_items(self):
        """Refresh lại items trong fence"""
        try:
            # Xóa items cũ
            while self.grid_layout.count():
                item = self.grid_layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
            
            # Tính số cột dựa trên chiều rộng của fence
            item_width = self.icon_size + 20  # Icon size + padding
            spacing = 10     # Khoảng cách giữa các items
            content_width = self.content_area.width() - 20  # Trừ đi padding
            num_columns = max(1, content_width // (item_width + spacing))
            
            # Thêm items mới theo grid
            for i, item in enumerate(self.fence.items):
                item_widget = self.create_item_widget(item)
                if self.vertical_layout:
                    row = i // num_columns
                    col = i % num_columns
                else:
                    row = i % num_columns
                    col = i // num_columns
                self.grid_layout.addWidget(item_widget, row, col)
                
            logging.info("Items refreshed successfully")
        except Exception as e:
            logging.error(f"Error refreshing items: {e}")

    def create_item_widget(self, item):
        widget = QFrame()
        widget.setFixedSize(QSize(85, 102))
        widget.setStyleSheet(f"""
            QFrame {{
                background-color: {self.item_bg_color};
                border-radius: 6px;
                padding: 4px;
            }}
            QFrame:hover {{
                background-color: {self.item_hover_color};
                border: 1px solid {self.item_border_color};
            }}
        """)
        
        # Thêm context menu cho item
        widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        widget.customContextMenuRequested.connect(lambda pos, i=item: self.show_item_context_menu(pos, i))
        
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(4, 6, 4, 4)
        layout.setSpacing(6)  # Tăng khoảng cách giữa icon và text
        
        # Icon container với style mới
        icon_container = QFrame()
        icon_container.setFixedHeight(62)  # Tăng chiều cao container
        icon_container.setStyleSheet("background: transparent;")
        icon_layout = QVBoxLayout(icon_container)
        icon_layout.setContentsMargins(0, 0, 0, 0)
        
        # Icon với kích thước lớn hơn
        icon_label = QLabel()
        icon = self.get_file_icon(item["path"])
        pixmap = icon.pixmap(48, 48)
        icon_label.setPixmap(pixmap)
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_layout.addWidget(icon_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(icon_container)
        
        # Name label với font và style mới
        name_label = QLabel()
        name = item["name"]
        if len(name) > 12:
            name = name[:12] + "..."
        name_label.setText(name)
        name_label.setStyleSheet(f"""
            QLabel {{
                color: {self.text_color};
                font-size: 11px;
                font-family: 'Segoe UI', sans-serif;
                padding: 2px 0;
            }}
        """)
        name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        name_label.setWordWrap(True)
        name_label.setToolTip(item["name"])
        layout.addWidget(name_label)
        
        return widget

    def get_file_icon(self, path):
        """Lấy icon từ file hoặc shortcut"""
        try:
            icon_provider = QFileIconProvider()
            
            if path.lower().endswith('.lnk'):
                # Xử lý shortcut
                shell = win32com.client.Dispatch("WScript.Shell")
                shortcut = shell.CreateShortCut(path)
                target_path = shortcut.TargetPath
                
                # Lấy icon từ file đích
                if os.path.exists(target_path):
                    file_info = QFileInfo(target_path)
                    return icon_provider.icon(file_info)
            
            # Lấy icon cho file thường và thư mục
            file_info = QFileInfo(path)
            if file_info.isDir():
                return icon_provider.icon(QFileIconProvider.IconType.Folder)
            return icon_provider.icon(file_info)
            
        except Exception as e:
            logging.error(f"Error getting icon for {path}: {e}")
            
        return QApplication.style().standardIcon(QStyle.StandardPixmap.SP_FileIcon)

    def remove_item(self, item):
        """Xóa item khỏi fence"""
        try:
            # Di chuyển shortcut ra desktop trước khi xóa
            if os.path.exists(item["path"]):
                desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
                new_path = os.path.join(desktop_path, os.path.basename(item["path"]))
                try:
                    shutil.move(item["path"], new_path)
                    logging.debug(f"Moved shortcut to desktop: {new_path}")
                except Exception as e:
                    logging.error(f"Error moving shortcut to desktop: {e}")
                    # Nếu không di chuyển được, thử copy
                    try:
                        shutil.copy2(item["path"], new_path)
                        os.remove(item["path"])
                    except Exception as e:
                        logging.error(f"Error copying shortcut to desktop: {e}")

            # Xóa khỏi danh sách
            if item in self.fence.items:
                self.fence.items.remove(item)
                self.refresh_items()
                
                # Lưu cấu hình
                if hasattr(self.parent(), 'parent') and hasattr(self.parent().parent(), 'save_fences'):
                    self.parent().parent().save_fences()
                
                logging.debug(f"Removed item: {item['name']}")
                
        except Exception as e:
            logging.error(f"Error removing item: {e}")

    def item_mouse_press_event(self, event, item, widget):
        """Xử lý click chuột trên item"""
        if event.button() == Qt.MouseButton.LeftButton:
            # Lưu vị trí bắt đầu kéo và item
            self.drag_start_pos = event.pos()
            self.dragging_item = item
            self.dragging_widget = widget
        elif event.button() == Qt.MouseButton.RightButton:
            self.show_item_context_menu(event.globalPosition().toPoint(), item)

    def item_mouse_move_event(self, event, item, widget):
        """Xử lý di chuyển chuột trên item"""
        if not hasattr(self, 'drag_start_pos') or not self.drag_start_pos:
            return
        
        if (event.pos() - self.drag_start_pos).manhattanLength() < QApplication.startDragDistance():
            return

        # Tạo drag object
        drag = QDrag(widget)
        mime_data = QMimeData()
        mime_data.setData("application/x-internal-move", b"1")  # Đánh dấu là internal move
        drag.setMimeData(mime_data)
        
        # Set pixmap for drag
        pixmap = widget.grab()
        drag.setPixmap(pixmap)
        drag.setHotSpot(event.pos())
        
        # Thực hiện drag
        result = drag.exec(Qt.DropAction.MoveAction)
        
        # Nếu thả ra ngoài fence, xóa item
        if result == Qt.DropAction.MoveAction and not self.geometry().contains(self.mapFromGlobal(QCursor.pos())):
            self.remove_item(item)

    def item_mouse_release_event(self, event, item):
        """Xử lý thả chuột trên item"""
        if event.button() == Qt.MouseButton.LeftButton:
            # Nếu không phải đang kéo thả, mở file/ứng dụng
            if not self.dragging_item:
                self.open_item(item["path"])
        
        self.drag_start_pos = None
        self.dragging_item = None
        self.dragging_widget = None

    def show_item_context_menu(self, pos, item):
        """Hiển thị context menu cho item"""
        try:
            menu = QMenu(self)
            
            # Action mở file
            open_action = QAction("Open", self)
            open_action.triggered.connect(lambda: self.open_item(item["path"]))
            menu.addAction(open_action)
            
            # Action xóa item
            remove_action = QAction("Remove", self)
            remove_action.triggered.connect(lambda: self.remove_item(item))
            menu.addAction(remove_action)
            
            # Lấy widget chứa item để tính toán vị trí chính xác
            sender = self.sender()
            if sender:
                # Chuyển đổi vị trí từ widget item sang tọa độ toàn cục
                global_pos = sender.mapToGlobal(pos)
                menu.exec(global_pos)
            else:
                menu.exec(self.mapToGlobal(pos))
            
        except Exception as e:
            logging.error(f"Error showing context menu: {e}")

    def mousePressEvent(self, event):
        """Xử lý click chuột"""
        if event.button() == Qt.MouseButton.LeftButton:
            # Kiểm tra xem có đang click vào vùng resize không
            self.resize_edge = self.get_resize_edge(event.pos())
            if self.resize_edge != self.EDGE_NONE:
                self.drag_start_pos = event.pos()
            else:
                # Click vào header để di chuyển
                if event.position().y() <= self.header.height() + 10:
                    self.is_dragging = True
                    self.drag_start_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
                    self.setCursor(Qt.CursorShape.ClosedHandCursor)
                    # Cập nhật giao diện khi bắt đầu kéo
                    self.update()

    def mouseMoveEvent(self, event):
        """Xử lý di chuyển chuột"""
        if not (self.is_dragging or self.resize_edge != self.EDGE_NONE):
            self.update_cursor(event.pos())
            return

        if self.resize_edge != self.EDGE_NONE:
            # Đang resize
            delta = event.pos() - self.drag_start_pos
            new_geometry = self.geometry()

            if self.resize_edge & self.EDGE_LEFT:
                new_geometry.setLeft(new_geometry.left() + delta.x())
            if self.resize_edge & self.EDGE_RIGHT:
                new_geometry.setRight(new_geometry.right() + delta.x())
            if self.resize_edge & self.EDGE_TOP:
                new_geometry.setTop(new_geometry.top() + delta.y())
            if self.resize_edge & self.EDGE_BOTTOM:
                new_geometry.setBottom(new_geometry.bottom() + delta.y())

            # Kiểm tra kích thước tối thiểu
            min_width = 200
            min_height = 100
            if new_geometry.width() >= min_width and new_geometry.height() >= min_height:
                self.setGeometry(new_geometry)
                self.drag_start_pos = event.pos()
                
                # Lưu kích thước mới
                self.fence.size = (self.width(), self.height())
                
        elif self.is_dragging:
            # Đang di chuyển
            new_pos = event.globalPosition().toPoint() - self.drag_start_pos
            self.move(new_pos)
            
            # Lưu vị trí mới
            self.fence.position = (self.x(), self.y())
            
        # Cập nhật giao diện khi di chuyển
        self.update()

    def mouseReleaseEvent(self, event):
        """Xử lý thả chuột"""
        if event.button() == Qt.MouseButton.LeftButton:
            was_dragging = self.is_dragging
            # Reset các biến
            self.is_dragging = False
            self.resize_edge = self.EDGE_NONE
            self.drag_start_pos = None
            self.setCursor(Qt.CursorShape.ArrowCursor)
            
            # Cập nhật giao diện khi kết thúc kéo
            self.update()
            
            # Lưu cấu hình nếu đã di chuyển
            if was_dragging:
                if hasattr(self.parent(), 'parent') and hasattr(self.parent().parent(), 'save_fences'):
                    self.parent().parent().save_fences()

    def get_resize_edge(self, pos):
        """Xác định cạnh resize dựa vào vị trí chuột"""
        edge = self.EDGE_NONE
        x = pos.x()
        y = pos.y()
        
        if x <= self.resize_area_size:
            edge |= self.EDGE_LEFT
        elif x >= self.width() - self.resize_area_size:
            edge |= self.EDGE_RIGHT
            
        if y <= self.resize_area_size:
            edge |= self.EDGE_TOP
        elif y >= self.height() - self.resize_area_size:
            edge |= self.EDGE_BOTTOM
            
        return edge

    def dragEnterEvent(self, event):
        """Xử lý khi bắt đầu kéo vào fence"""
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        """Xử lý khi di chuyển trong fence"""
        if event.mimeData().hasUrls():
            pos = event.position().toPoint()
            target_widget = self.childAt(pos)
            
            # Reset style của tất cả items
            self.reset_items_style()
            
            # Tìm QFrame cha nếu target_widget là QLabel
            while target_widget and not isinstance(target_widget, QFrame):
                target_widget = target_widget.parent()
            
            # Highlight target widget nếu là item frame
            if isinstance(target_widget, QFrame) and target_widget != self.content_area and target_widget != self.header:
                target_widget.setStyleSheet("""
                    QFrame {
                        background-color: rgba(255, 255, 255, 20);
                        border: 1px solid rgba(255, 255, 255, 50);
                        border-radius: 5px;
                        padding: 4px;
                    }
                """)
            event.accept()
        else:
            event.ignore()

    def reset_items_style(self):
        """Reset style của tất cả items về mặc định"""
        for frame in self.findChildren(QFrame):
            if frame != self.content_area and frame != self.header:
                frame.setStyleSheet("""
                    QFrame {
                        background-color: rgba(255, 255, 255, 10);
                        border-radius: 5px;
                        padding: 4px;
                    }
                    QFrame:hover {
                        background-color: rgba(255, 255, 255, 20);
                        border: 1px solid rgba(255, 255, 255, 30);
                    }
                """)

    def dropEvent(self, event):
        """Xử lý khi thả vào fence"""
        try:
            # Reset style của tất cả items
            self.reset_items_style()
            
            if event.mimeData().hasUrls():
                # Xử lý thêm file mới vào fence
                for url in event.mimeData().urls():
                    file_path = url.toLocalFile()
                    if os.path.exists(file_path):
                        name = os.path.splitext(os.path.basename(file_path))[0]
                        
                        # Nếu là shortcut, di chuyển nó vào fence
                        if file_path.lower().endswith('.lnk'):
                            shortcuts_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                                   "shortcuts")  # Thêm dấu )
                            os.makedirs(shortcuts_dir, exist_ok=True)
                            new_path = os.path.join(shortcuts_dir, os.path.basename(file_path))
                            
                            # Di chuyển file
                            shutil.move(file_path, new_path)
                            
                            self.fence.items.append({
                                "path": new_path,
                                "name": name
                            })
                            logging.debug(f"Moved shortcut: {name}")
                        else:
                            # Tạo shortcut cho file thường
                            shortcuts_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                                   "shortcuts")  # Thêm dấu )
                            os.makedirs(shortcuts_dir, exist_ok=True)
                            
                            shortcut_path = os.path.join(shortcuts_dir, f"{name}.lnk")
                            shell = win32com.client.Dispatch("WScript.Shell")
                            shortcut = shell.CreateShortCut(shortcut_path)
                            shortcut.TargetPath = file_path
                            shortcut.save()
                            
                            # Thêm vào fence
                            self.fence.items.append({
                                "path": shortcut_path,
                                "name": name
                            })
                            logging.debug(f"Created shortcut: {name}")
                
                self.refresh_items()
                if hasattr(self.parent(), 'parent') and hasattr(self.parent().parent(), 'save_fences'):
                    self.parent().parent().save_fences()
                
                event.accept()
            else:
                event.ignore()
            
        except Exception as e:
            logging.error(f"Error in dropEvent: {e}")
            event.ignore()

    def dragLeaveEvent(self, event):
        """Reset style khi kéo ra khỏi fence"""
        for frame in self.findChildren(QFrame):
            if frame != self.content_area and frame != self.header:
                frame.setStyleSheet("""
                    QFrame {
                        background-color: rgba(255, 255, 255, 10);
                        border-radius: 5px;
                        padding: 4px;
                    }
                    QFrame:hover {
                        background-color: rgba(255, 255, 255, 20);
                        border: 1px solid rgba(255, 255, 255, 30);
                    }
                """)

    def enterEvent(self, event):
        """Cập nhật cursor khi di chuột vào widget"""
        self.update_cursor(self.mapFromGlobal(QCursor.pos()))

    def update_cursor(self, pos):
        """Cập nhật hình dạng con trỏ dựa vào vị trí"""
        edge = self.get_resize_edge(pos)
        if edge == self.EDGE_LEFT | self.EDGE_TOP or edge == self.EDGE_RIGHT | self.EDGE_BOTTOM:
            self.setCursor(Qt.CursorShape.SizeFDiagCursor)
        elif edge == self.EDGE_RIGHT | self.EDGE_TOP or edge == self.EDGE_LEFT | self.EDGE_BOTTOM:
            self.setCursor(Qt.CursorShape.SizeBDiagCursor)
        elif edge & (self.EDGE_LEFT | self.EDGE_RIGHT):
            self.setCursor(Qt.CursorShape.SizeHorCursor)
        elif edge & (self.EDGE_TOP | self.EDGE_BOTTOM):
            self.setCursor(Qt.CursorShape.SizeVerCursor)
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Lấy theme hiện tại
        theme = self.themes[self.current_theme]
        
        # Vẽ background với độ trong suốt từ theme
        bg_color = color_from_string(theme["bg_color"])
        bg_color.setAlphaF(theme["opacity"])
        painter.setBrush(bg_color)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 8, 8)
        
        # Vẽ header với màu riêng
        header_rect = QRect(0, 0, self.width(), self.header.height())
        # Sử dụng header_bg thay vì header_color và thêm kiểm tra
        header_color = color_from_string(theme.get("header_color", theme["header_bg"]))
        header_color.setAlphaF(theme["opacity"] + 0.1)
        painter.setBrush(header_color)
        painter.drawRoundedRect(header_rect, 8, 8)
        
        # Vẽ border
        if self.is_dragging:
            border_color = QColor(255, 255, 255, 25)
        else:
            border_color = color_from_string(theme["border_color"])
        
        pen = QPen(border_color)
        pen.setWidth(1)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(self.rect(), 8, 8)

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        
        # Menu cũ
        rename_action = menu.addAction("Rename")
        roll_action = menu.addAction("Roll Up" if not self.is_rolled_up else "Roll Down")
        desktop_action = menu.addAction("Pin to Desktop" if not self.always_on_desktop else "Unpin from Desktop")
        
        # Thêm submenu Theme
        theme_menu = menu.addMenu("Theme")
        for theme_name in self.themes.keys():
            theme_action = theme_menu.addAction(theme_name)
            theme_action.setCheckable(True)
            theme_action.setChecked(theme_name == self.current_theme)
        
        # Thêm submenu Layout
        layout_menu = menu.addMenu("Layout")
        for layout_mode in self.layout_modes:
            layout_action = layout_menu.addAction(layout_mode)
            layout_action.setCheckable(True)
            layout_action.setChecked(layout_mode == self.current_layout)
        
        # Thêm submenu Icon Size
        icon_menu = menu.addMenu("Icon Size")
        for size_name, size in self.icon_sizes.items():
            size_action = icon_menu.addAction(size_name)
            size_action.setCheckable(True)
            size_action.setChecked(size == self.icon_size)
        
        menu.addSeparator()
        toggle_visibility_action = menu.addAction("Hide")
        delete_action = menu.addAction("Delete")
        
        # Xử lý action được chọn
        action = menu.exec(event.globalPos())
        if action:
            if action == rename_action:
                self.show_rename_dialog()
            elif action == roll_action:
                self.toggle_rollup()
            elif action == desktop_action:
                self.toggle_desktop_mode()
            elif action == toggle_visibility_action:
                self.hide()
            elif action == delete_action:
                self.delete_fence()
            elif action.text() in self.themes:
                self.current_theme = action.text()
                self.apply_theme(self.current_theme)
            elif action.text() in self.layout_modes:
                self.current_layout = action.text()
                self.refresh_items()
            elif action.text() in self.icon_sizes:
                self.icon_size = self.icon_sizes[action.text()]
                self.refresh_items()
                # Lưu cấu hình
                if hasattr(self.parent(), 'parent') and hasattr(self.parent().parent(), 'save_fences'):
                    self.parent().parent().save_fences()

    def show_rename_dialog(self):
        new_title, ok = QInputDialog.getText(
            self, 'Rename Fence', 
            'Enter new name:', 
            QLineEdit.EchoMode.Normal, 
            self.fence.title
        )
        if ok and new_title:
            self.fence.title = new_title
            self.title_label.setText(new_title)
            if hasattr(self.parent(), 'parent') and hasattr(self.parent().parent(), 'save_fences'):
                self.parent().parent().save_fences()

    def delete_fence(self):
        """Xóa fence và di chuyển tất cả items ra desktop"""
        try:
            # Di chuyển tất cả shortcut ra desktop
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
            for item in self.fence.items:
                if os.path.exists(item["path"]):
                    try:
                        new_path = os.path.join(desktop_path, os.path.basename(item["path"]))
                        # Thêm kiểm tra file đích đã tồn tại chưa
                        if os.path.exists(new_path):
                            # Nếu đã tồn tại, thêm số vào tên file
                            base, ext = os.path.splitext(new_path)
                            counter = 1
                            while os.path.exists(f"{base}_{counter}{ext}"):
                                counter += 1
                            new_path = f"{base}_{counter}{ext}"
                            
                        shutil.move(item["path"], new_path)
                        logging.debug(f"Moved shortcut back to desktop: {new_path}")
                    except Exception as e:
                        logging.error(f"Error moving shortcut: {e}")
                        try:
                            # Thử copy nếu không move được
                            shutil.copy2(item["path"], new_path)
                            os.remove(item["path"])
                            logging.debug(f"Copied and removed shortcut: {new_path}")
                        except Exception as e:
                            logging.error(f"Error copying shortcut: {e}")

            # Xóa fence khỏi parent
            if hasattr(self.parent(), 'parent') and hasattr(self.parent().parent(), 'delete_fence'):
                self.parent().parent().delete_fence(self)
                self.deleteLater()
                logging.info("Fence deleted successfully")
                
        except Exception as e:
            logging.error(f"Error deleting fence: {e}")

    def resizeEvent(self, event: QResizeEvent):
        super().resizeEvent(event)
        # Lưu kích thước mới
        self.fence.size = (self.width(), self.height())
        
    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # Ch toggle roll up khi double click vào header
            if event.position().y() <= self.header.height() + 10:
                self.toggle_rollup()

    def toggle_rollup(self):
        """Toggle trạng thái cuộn/mở của fence"""
        self.fence.is_rolled_up = not self.fence.is_rolled_up
        if self.fence.is_rolled_up:
            self.old_height = self.height()
            self.resize(self.width(), self.header.height())
        else:
            self.resize(self.width(), self.old_height)
        
        # Lưu cấu hình sau khi thay đổi
        if hasattr(self.parent(), 'parent') and hasattr(self.parent().parent(), 'save_fences'):
            self.parent().parent().save_fences()

    def open_item(self, path):
        """Mở file hoặc folder khi click"""
        try:
            os.startfile(path)
        except Exception as e:
            logging.error(f"Error opening item: {e}")

    def toggle_desktop_mode(self):
        """Toggle giữa chế độ desktop và normal"""
        try:
            if not self.always_on_desktop:
                # Lưu vị trí và flags hiện tại
                self.normal_pos = self.pos()
                self.normal_flags = self.windowFlags()
                
                # Pin to desktop
                self.setParent(None)
                self.setWindowFlags(
                    Qt.WindowType.FramelessWindowHint |
                    Qt.WindowType.Tool
                    # Không thêm WindowStaysOnTopHint khi pin to desktop
                )
                
                # Đặt làm con của desktop
                if DesktopController.set_window_always_on_desktop(self.winId()):
                    self.always_on_desktop = True
                    self.show()
                    self.move(self.normal_pos)
                    self.lower()  # Đảm bảo fence nằm dưới các cửa sổ khác
                    logging.debug("Successfully pinned to desktop")
                else:
                    self.unpin_from_desktop()
            else:
                self.unpin_from_desktop()
        except Exception as e:
            logging.exception("Error in toggle_desktop_mode:")
            self.unpin_from_desktop()

    def start_desktop_monitoring(self):
        """Bắt đầu theo dõi trạng thái desktop"""
        if not hasattr(self, 'desktop_timer'):
            self.desktop_timer = QTimer(self)
            self.desktop_timer.timeout.connect(self.check_desktop_state)
            self.desktop_timer.start(500)  # Kiểm tra mỗi 500ms

    def stop_desktop_monitoring(self):
        """Dừng theo dõi trạng thái desktop"""
        if hasattr(self, 'desktop_timer'):
            self.desktop_timer.stop()
            self.desktop_timer.deleteLater()
            del self.desktop_timer

    def check_desktop_state(self):
        """Kiểm tra xem có đang ở desktop không"""
        if self.always_on_desktop:
            is_on_desktop = DesktopController.is_on_desktop()
            if is_on_desktop and not self.isVisible():
                self.show()
                self.raise_()
            elif not is_on_desktop and self.isVisible():
                self.hide()

    def unpin_from_desktop(self):
        """Gỡ khỏi desktop và trở về chế độ normal"""
        try:
            # Khôi phục parent và flags
            self.setParent(self.parent())
            self.setWindowFlags(
                Qt.WindowType.FramelessWindowHint |
                Qt.WindowType.Tool |
                Qt.WindowType.WindowStaysOnTopHint  # Chỉ thêm flag này khi unpin
            )
            self.always_on_desktop = False
            self.show()
            if hasattr(self, 'normal_pos'):
                self.move(self.normal_pos)
            self.raise_()  # Đảm bảo fence hiển thị trên các cửa sổ khác khi unpin
            logging.debug("Successfully unpinned from desktop")
        except Exception as e:
            logging.exception("Error in unpin_from_desktop:")

    def eventFilter(self, obj, event):
        if obj == self:
            if event.type() == QEvent.Type.DragEnter:
                self.dragEnterEvent(event)
                return True
            elif event.type() == QEvent.Type.DragMove:
                self.dragMoveEvent(event)
                return True
            elif event.type() == QEvent.Type.Drop:
                self.dropEvent(event)
                return True
        return super().eventFilter(obj, event)

    def item_drag_enter_event(self, event, item):
        """Xử lý khi kéo item khác vào"""
        if event.source() in self.findChildren(QFrame):
            event.accept()
        else:
            event.ignore()

    def item_drop_event(self, event, target_item):
        """Xử lý khi thả item để đổi vị trí"""
        source_widget = event.source()
        if source_widget in self.findChildren(QFrame):
            # Tìm source item
            source_item = None
            for item in self.fence.items:
                if self.findChild(QFrame, str(id(item))) == source_widget:
                    source_item = item
                    break
            
            if source_item:
                # Đổi vị trí trong danh sách
                source_idx = self.fence.items.index(source_item)
                target_idx = self.fence.items.index(target_item)
                self.fence.items[source_idx], self.fence.items[target_idx] = \
                    self.fence.items[target_idx], self.fence.items[source_idx]
                
                # Cập nhật giao diện
                self.refresh_items()
                
                # Lưu cấu hình
                if hasattr(self.parent(), 'parent') and hasattr(self.parent().parent(), 'save_fences'):
                    self.parent().parent().save_fences()

    def apply_theme(self, theme_name):
        """Áp dụng theme"""
        if theme_name not in self.themes:
            theme_name = "Crystal"  # Default theme
            self.current_theme = theme_name
        
        theme = self.themes[theme_name]
        
        # Sửa lại cách tạo màu từ string
        def color_from_string(color_str):
            # Chuyển "rgba(r,g,b,a)" thành QColor
            color_str = color_str.strip('rgba()')
            r,g,b,a = map(float, color_str.split(','))
            return QColor(int(r), int(g), int(b), int(a * 255))
        
        # Cập nhật các màu sắc
        self.background_color = color_from_string(theme["bg_color"])
        self.border_color = color_from_string(theme["border_color"])
        self.item_bg_color = theme["item_bg_color"] 
        self.item_hover_color = theme["item_hover_color"]
        self.item_border_color = theme["item_border_color"]
        self.text_color = theme["text_color"]
        
        # Cập nhật style cho header
        self.header.setStyleSheet(f"""
            QFrame {{
                background-color: {theme["header_bg"]};
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
            }}
        """)
        
        # Cập nhật style cho title
        self.title_label.setStyleSheet(f"""
            QLabel {{
                color: {theme["text_color"]};
                font-size: 12px;
                font-weight: bold;
            }}
        """)
        
        # Cập nhật style cho minimize button
        self.btn_minimize.setStyleSheet(f"""
            QPushButton {{
                color: {theme["text_color"]};
                background: transparent;
                border: none;
                font-size: 14px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background: rgba(255, 255, 255, 15);
                border-radius: 4px;
            }}
        """)
        
        # Lưu theme hiện tại
        self.current_theme = theme_name
        
        # Refresh items để cập nhật style
        self.refresh_items()
        
        # Force repaint
        self.update()
        
        # Lưu cấu hình nếu có parent
        if hasattr(self.parent(), 'parent') and hasattr(self.parent().parent(), 'save_fences'):
            self.parent().parent().save_fences()
