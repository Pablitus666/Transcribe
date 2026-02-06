import os
import sys

def resource_path(relative_path: str) -> str:
    """
    Get absolute path to resource, works for dev and for PyInstaller.
    'relative_path' should be relative to the project root.
    """
    print(f"DEBUG resource_path: Called with relative_path='{relative_path}'")
    if hasattr(sys, '_MEIPASS'):
        print(f"DEBUG resource_path: sys._MEIPASS detected: {sys._MEIPASS}")
        full_path = os.path.join(sys._MEIPASS, relative_path)
        print(f"DEBUG resource_path: Returning MEIPASS path: {full_path}")
        return full_path
    
    # En modo desarrollo, necesitamos encontrar la raíz del proyecto.
    current_dir = os.path.abspath(os.path.dirname(__file__))
    project_root = current_dir
    
    root_markers = ['.git', 'ui_main.py', 'config', 'images'] 
    
    temp_dir = current_dir
    while temp_dir != os.path.dirname(temp_dir):
        if any(os.path.exists(os.path.join(temp_dir, marker)) for marker in root_markers):
            project_root = temp_dir
            break
        temp_dir = os.path.dirname(temp_dir)
    
    full_path = os.path.join(project_root, relative_path)
    print(f"DEBUG resource_path: Returning DEV path: {full_path}")
    return full_path