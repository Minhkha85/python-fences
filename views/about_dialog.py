from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QLabel, 
                           QPushButton, QHBoxLayout)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from utils.version import VERSION
import os

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About Python Fences")
        self.setFixedSize(400, 300)
        
        layout = QVBoxLayout()
        
        # Logo
        logo_label = QLabel()
        icon_path = os.path.join("assets", "fence_icon.ico")
        if os.path.exists(icon_path):
            pixmap = QPixmap(icon_path)
            logo_label.setPixmap(pixmap.scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio))
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(logo_label)
        
        # App name and version
        title_label = QLabel("Python Fences")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        version_label = QLabel(f"Version {VERSION}")
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(version_label)
        
        # Description
        desc_label = QLabel(
            "A desktop organization tool inspired by Stardock Fences.\n"
            "Create transparent fences to organize your desktop icons."
        )
        desc_label.setWordWrap(True)
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(desc_label)
        
        # Copyright
        copyright_label = QLabel("© 2024 Your Name")
        copyright_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(copyright_label)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        check_updates_btn = QPushButton("Check for Updates")
        check_updates_btn.clicked.connect(self.check_updates)
        button_layout.addWidget(check_updates_btn)
        
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        button_layout.addWidget(ok_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def check_updates(self):
        from utils.updater import check_for_updates
        check_for_updates(self) 