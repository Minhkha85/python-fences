import os
import winreg
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path

class DesktopWatcher:
    def __init__(self, callback):
        self.callback = callback
        self.observer = Observer()
        
    def get_desktop_path(self):
        """Get the correct desktop path using Windows Registry"""
        try:
            # Try to get path from registry
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders') as key:
                desktop_path = winreg.QueryValueEx(key, 'Desktop')[0]
                if os.path.exists(desktop_path):
                    return desktop_path
        except:
            pass
        
        # Fallback methods
        paths_to_try = [
            os.path.join(os.environ['USERPROFILE'], 'OneDrive', 'Desktop'),
            os.path.join(os.environ['USERPROFILE'], 'Desktop'),
            str(Path.home() / "Desktop"),
            str(Path.home() / "OneDrive" / "Desktop")
        ]
        
        for path in paths_to_try:
            if os.path.exists(path):
                return path
                
        raise FileNotFoundError("Could not find Desktop folder in any standard location")
        
    def start(self):
        desktop_path = self.get_desktop_path()
        print(f"Watching desktop at: {desktop_path}")
        
        event_handler = DesktopEventHandler(self.callback)
        self.observer.schedule(event_handler, desktop_path, recursive=False)
        self.observer.start()
        
    def stop(self):
        self.observer.stop()
        self.observer.join()

class DesktopEventHandler(FileSystemEventHandler):
    def __init__(self, callback):
        self.callback = callback
        
    def on_created(self, event):
        if not event.is_directory:
            self.callback('created', event.src_path)
            
    def on_deleted(self, event):
        if not event.is_directory:
            self.callback('deleted', event.src_path)