import requests
import logging
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import QThread, pyqtSignal
import webbrowser
from .version import VERSION, GITHUB_API, UPDATE_URL

class UpdateChecker(QThread):
    update_available = pyqtSignal(str)
    
    def run(self):
        try:
            response = requests.get(GITHUB_API)
            if response.status_code == 200:
                latest_version = response.json()['tag_name'].strip('v')
                current_version = VERSION
                
                if self._compare_versions(latest_version, current_version):
                    self.update_available.emit(latest_version)
        except Exception as e:
            logging.error(f"Error checking for updates: {e}")
    
    def _compare_versions(self, latest, current):
        """So sánh phiên bản"""
        latest_parts = list(map(int, latest.split('.')))
        current_parts = list(map(int, current.split('.')))
        
        for i in range(max(len(latest_parts), len(current_parts))):
            latest_part = latest_parts[i] if i < len(latest_parts) else 0
            current_part = current_parts[i] if i < len(current_parts) else 0
            
            if latest_part > current_part:
                return True
            elif latest_part < current_part:
                return False
        return False

def check_for_updates(parent=None):
    """Kiểm tra cập nhật và hiển thị dialog"""
    try:
        response = requests.get(GITHUB_API)
        if response.status_code == 200:
            latest_version = response.json()['tag_name'].strip('v')
            current_version = VERSION
            
            if latest_version > current_version:
                msg = QMessageBox(parent)
                msg.setWindowTitle("Update Available")
                msg.setText(f"A new version ({latest_version}) is available!")
                msg.setInformativeText("Would you like to download it now?")
                msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
                msg.setDefaultButton(QMessageBox.StandardButton.Yes)
                
                if msg.exec() == QMessageBox.StandardButton.Yes:
                    webbrowser.open(UPDATE_URL)
            else:
                if parent:
                    QMessageBox.information(parent, "No Updates", "You are using the latest version.")
    except Exception as e:
        logging.error(f"Error checking for updates: {e}")
        if parent:
            QMessageBox.warning(parent, "Error", "Could not check for updates.") 