import PyInstaller.__main__
import os
import shutil
import sys
from utils.version import VERSION

def build():
    try:
        # Xóa thư mục dist và build cũ
        for dir in ['dist', 'build']:
            if os.path.exists(dir):
                shutil.rmtree(dir)
                print(f"Deleted {dir} directory")

        # Tạo thư mục dist và dist/assets
        os.makedirs('dist', exist_ok=True)
        os.makedirs(os.path.join('dist', 'assets'), exist_ok=True)
        print("Created dist directories")

        # Copy assets
        assets_src = 'assets'
        assets_dst = os.path.join('dist', 'assets')
        if os.path.exists(assets_src):
            if os.path.exists(assets_dst):
                shutil.rmtree(assets_dst)
            shutil.copytree(assets_src, assets_dst)
            print("Copied assets")
        else:
            print("Warning: assets directory not found!")

        # Kiểm tra icon
        icon_path = os.path.abspath(os.path.join("assets", "kha.ico"))
        if not os.path.exists(icon_path):
            print(f"Warning: Icon file not found at {icon_path}")
            sys.exit(1)

        # Tạo version.txt
        version_file = os.path.join('dist', 'version.txt')
        with open(version_file, 'w') as f:
            f.write(VERSION)
        print("Created version.txt")

        print("Starting PyInstaller build...")
        PyInstaller.__main__.run([
            'main.py',
            '--name=PythonFences',
            '--onefile',
            f'--icon={icon_path}',
            '--noconsole',
            '--add-data=assets;assets',
            '--add-data=version.txt;.',
            '--hidden-import=win32com.shell.shell',
            '--hidden-import=win32com.client',
            '--hidden-import=win32gui',
            '--hidden-import=win32con',
            '--hidden-import=win32api',
            '--hidden-import=pythoncom',
            '--hidden-import=PyQt6',
            '--hidden-import=watchdog',
            '--hidden-import=requests',
            '--debug=all'
        ])

        # Kiểm tra kết quả
        exe_path = os.path.join('dist', 'PythonFences.exe')
        if os.path.exists(exe_path):
            print(f"Build successful! EXE created at: {exe_path}")
        else:
            print("Build failed: EXE not created")
            sys.exit(1)

    except Exception as e:
        print(f"Build failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    build() 