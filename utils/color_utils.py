from PyQt6.QtGui import QColor

def color_from_string(color_str):
    """Chuyển chuỗi màu rgba thành QColor"""
    try:
        color_str = color_str.strip('rgba()')
        r,g,b,a = map(float, color_str.split(','))
        return QColor(int(r), int(g), int(b), int(a * 255))
    except:
        # Fallback color nếu có lỗi
        return QColor(255, 255, 255, 50) 