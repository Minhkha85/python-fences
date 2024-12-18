import PyInstaller.__main__
import os
import shutil

# Xóa thư mục dist và build cũ nếu có
for dir in ['dist', 'build']:
    if os.path.exists(dir):
        shutil.rmtree(dir)

# Đường dẫn đến icon
icon_path = os.path.abspath("assets/fence_icon.ico")

PyInstaller.__main__.run([
    'main.py',
    '--name=PythonFences',
    '--onefile',
    f'--icon={icon_path}',
    '--noconsole',
    '--add-data=assets;assets',
    '--hidden-import=win32com.shell.shell',
    '--hidden-import=win32com.client',
    '--hidden-import=win32gui',
    '--hidden-import=win32con',
    '--hidden-import=win32api',
    '--hidden-import=pythoncom',
    '--hidden-import=PyQt6',
    '--hidden-import=watchdog',
])

# Copy thư mục assets vào dist
shutil.copytree('assets', 'dist/assets', dirs_exist_ok=True) 