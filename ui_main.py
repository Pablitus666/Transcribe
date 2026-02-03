# ui_main.py
import sys
import tkinter as tk
import subprocess
import time
import logging
import ctypes
import os # Add this import
from multiprocessing.connection import Client
import threading
import queue

from tkinterdnd2 import TkinterDnD
from gui.main_window import MainWindow
from core.dpi import enable_dpi_awareness, get_tkinter_scalefactor
from gui.i18n import tr # Add this import

# --- Configuración (debe coincidir con hotkey_server.py) ---
ADDRESS = 'localhost'
PORT = 6000
AUTH_KEY = b'transcribe_secret_key'
LOG_FORMAT = '%(asctime)s - [%(levelname)s] - (UI_Client): %(message)s'

# --- Configuración de Logging ---
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

def launch_server_as_admin():
    """
    Intenta lanzar el hotkey_server.py con privilegios de administrador
    y devuelve el proceso. Muestra un diálogo de UAC.
    """
    if sys.platform != 'win32':
        logging.error(tr("privilege_elevation_windows_only"))
        return None

    try:
        # Usamos ShellExecuteW para invocar el verbo 'runas' que eleva a admin
        python_executable = sys.executable.replace("python.exe", "pythonw.exe") # Usar pythonw para no abrir consola
        script_path = 'hotkey_server.py'
        script_dir = os.path.dirname(os.path.abspath(__file__)) # Get the directory of ui_main.py
        
        ret = ctypes.windll.shell32.ShellExecuteW(
            None,           # handle to parent window
            "runas",        # verb
            python_executable, # file
            script_path,    # parameters
            script_dir,     # working directory
            1               # show command (SW_SHOWNORMAL)
        )
        
        if ret > 32:
            logging.info(tr("ui_hotkey_elevation_request"))
            return True
        else:
            logging.error(tr("ui_hotkey_elevation_failed", error_code=ret))
            return False

    except Exception as e:
        logging.critical(tr("ui_hotkey_launch_fatal_error", error_message=e), exc_info=True)
        return False

def main():
    """
    Punto de entrada principal de la aplicación de UI.
    Lanza el servidor de hotkeys y luego inicia la interfaz de usuario.
    """
    # 1. Lanzar el servidor de hotkeys en un proceso separado y elevado
    if not launch_server_as_admin():
        # Aquí podrías mostrar un messagebox de error en Tkinter
        logging.error(tr("hotkey_server_failed_start"))
        # Decidimos no continuar si el servidor no se puede lanzar.
        # El usuario puede cancelar el UAC.
        return

    # 2. Intentar conectarse al servidor
    conn = None
    max_retries = 5
    retry_delay = 0.1
    for i in range(max_retries):
        try:
            logging.info(tr("ui_connecting_to_hotkey_server", attempt=i+1, max_attempts=max_retries))
            conn = Client((ADDRESS, PORT), authkey=AUTH_KEY)
            logging.info(tr("ui_hotkey_server_connected"))
            break
        except Exception as e:
            if i == max_retries - 1:
                logging.error(tr("hotkey_server_failed_connect"))
                # Aquí también se podría mostrar un error en la UI.
            time.sleep(retry_delay)

    # 3. Iniciar la interfaz gráfica
    # Forzar el AppUserModelID en Windows para asegurar el ícono en la barra de tareas
    if sys.platform == 'win32':
        my_app_id = 'Pablitus.Transcribe.1.0' 
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(my_app_id)

    # Usamos TkinterDnD.Tk como la ventana raíz para habilitar el Drag & Drop
    root = TkinterDnD.Tk()
    
    # Obtener el factor de escala y aplicarlo a Tkinter
    scale_factor = get_tkinter_scalefactor(root)
    root.tk.call('tk', 'scaling', scale_factor)
    logging.info(tr("ui_scale_factor_set", scale_factor=scale_factor))

    # Instanciamos nuestra ventana principal, pasándole la conexión y otros parámetros
    app = MainWindow(root, scale_factor=scale_factor, ipc_connection=conn)
    
    # Iniciamos el bucle principal de la aplicación
    root.mainloop()

if __name__ == "__main__":
    main()
