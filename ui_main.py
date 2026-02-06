# ui_main.py
import sys
import tkinter as tk
import subprocess
import time
import logging
import ctypes
import os 
from multiprocessing.connection import Client
import threading
import queue
import tkinter.messagebox # Importar messagebox

from tkinterdnd2 import TkinterDnD
from gui.main_window import MainWindow
from core.dpi import enable_dpi_awareness, get_tkinter_scalefactor
from gui.i18n import tr
from core.utils import resource_path
from hotkey_server import main_hotkey_server  # Importar el punto de entrada del hotkey_server

# --- Configuración (debe coincidir con hotkey_server.py) ---
ADDRESS = 'localhost'
PORT = 6000
AUTH_KEY = b'transcribe_secret_key'
LOG_FORMAT = '%(asctime)s - [%(levelname)s] - (UI_Client): %(message)s'

# --- Configuración de Logging ---
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

def launch_server_as_admin():
    """
    Intenta lanzar el hotkey_server como un subproceso elevado,
    pasando un argumento para que sepa ejecutar su lógica de servidor.
    """
    if sys.platform != 'win32':
        logging.error(tr("privilege_elevation_windows_only"))
        return None

    try:
        executable_path = sys.executable # sys.executable ya es el .exe principal
        command_args = f'--hotkey-server'
        
        ret = ctypes.windll.shell32.ShellExecuteW(
            None,           # handle to parent window
            "runas",        # verb
            executable_path, # file (el propio Transcribe.exe)
            command_args,   # parameters (--hotkey-server)
            None,           # working directory
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

def main_ui():
    """
    Punto de entrada principal de la aplicación de UI.
    Lanza el servidor de hotkeys y luego inicia la interfaz de usuario.
    """
    # 1. Lanzar el servidor de hotkeys en un proceso separado y elevado
    if not launch_server_as_admin():
        logging.error(tr("hotkey_server_failed_start"))
        return

    # 2. Intentar conectarse al servidor
    conn = None
    max_retries = 5
    retry_delay = 0.5 # Aumentado el retardo para dar más tiempo al servidor a iniciarse
    for i in range(max_retries):
        try:
            logging.info(tr("ui_connecting_to_hotkey_server", attempt=i+1, max_attempts=max_retries))
            conn = Client((ADDRESS, PORT), authkey=AUTH_KEY)
            logging.info(tr("ui_hotkey_server_connected"))
            break
        except Exception as e:
            if i == max_retries - 1:
                logging.error(tr("hotkey_server_failed_connect", error_message=e))
                tk.messagebox.showerror(tr("error_title"), tr("hotkey_server_conn_fail_message"))
                sys.exit(1) # Salir si no se puede conectar al hotkey server
            time.sleep(retry_delay)

    # 3. Iniciar la interfaz gráfica
    if sys.platform == 'win32':
        my_app_id = 'Pablitus.Transcribe.1.0' 
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(my_app_id)

    root = TkinterDnD.Tk()
    
    scale_factor = get_tkinter_scalefactor(root)
    root.tk.call('tk', 'scaling', scale_factor)
    logging.info(tr("ui_scale_factor_set", scale_factor=scale_factor))

    app = MainWindow(root, scale_factor=scale_factor, ipc_connection=conn)
    
    root.mainloop()

if __name__ == "__main__":
    enable_dpi_awareness() # Asegúrate de que DPI awareness se active al inicio.

    if "--hotkey-server" in sys.argv:
        # Si se ejecuta con el argumento --hotkey-server, iniciar la lógica del servidor.
        # Esto ocurre cuando ui_main.py lo lanza como subproceso elevado.
        main_hotkey_server()
    else:
        # Si no hay argumentos especiales, iniciar la UI principal.
        main_ui()
