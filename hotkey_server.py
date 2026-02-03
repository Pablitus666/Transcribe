# hotkey_server.py
import sys
import ctypes
import logging
import os
from multiprocessing.connection import Listener
import time

from core.hotkeys import HotkeyManager
from gui.i18n import tr # Add this import

# --- Configuración ---
ADDRESS = 'localhost'
PORT = 6000
AUTH_KEY = b'transcribe_secret_key'
LOG_FORMAT = '%(asctime)s - [%(levelname)s] - (HotkeyServer): %(message)s'

# --- Configuración de Logging ---
# Crear un log en el directorio del script para poder depurar el proceso elevado.
log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hotkey_server.log')
logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler(log_file_path, mode='w'),
        logging.StreamHandler(sys.stdout)
    ]
)

def is_admin():
    """Comprueba si el script se está ejecutando con privilegios de administrador."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except AttributeError:
        return False

class HotkeyServer:
    """
    Proceso dedicado que se ejecuta como administrador para gestionar
    las hotkeys globales y enviar comandos al proceso de la UI.
    """
    def __init__(self, address, port, authkey):
        self.address = (address, port)
        self.authkey = authkey
        self.hotkey_manager = HotkeyManager()
        self.connection = None
        self.media_loaded = False

    def _get_hotkey_callbacks(self):
        """Define los callbacks para las hotkeys. Estos envían comandos a través de la conexión."""
        
        def send_command(command):
            # 'toggle_play_pause' siempre se envía si hay conexión,
            # incluso si el medio no está "cargado" (para permitir iniciar desde 0).
            if command == 'toggle_play_pause':
                if self.connection:
                    try:
                        logging.info(tr("hotkey_sending_command", command=command))
                        self.connection.send({"command": command})
                    except (BrokenPipeError, EOFError):
                        logging.error(tr("hotkey_conn_broken_reconnecting"))
                        self.connection = None
                else:
                    logging.warning(tr("hotkey_command_failed_no_conn_or_media", command=command))
            # Otros comandos respetan la flag media_loaded
            elif self.connection and self.media_loaded:
                try:
                    logging.info(tr("hotkey_sending_command", command=command))
                    self.connection.send({"command": command})
                except (BrokenPipeError, EOFError):
                    logging.error(tr("hotkey_conn_broken_reconnecting"))
                    self.connection = None
            else:
                logging.warning(tr("hotkey_command_failed_no_conn_or_media", command=command))

        press_callbacks = {
            'f1': lambda: send_command('toggle_play_pause'),
            'f2': lambda: send_command('stop_button_pressed'),
            'f3': lambda: send_command('seek_backward'),
            'f4': lambda: send_command('seek_forward'),
            'delete': lambda: send_command('delete_media'),
        }
        release_callbacks = {
            'f3': lambda: send_command('stop_seek'),
            'f4': lambda: send_command('stop_seek'),
        }
        return press_callbacks, release_callbacks

    def _handle_client_messages(self):
        """Maneja los mensajes recibidos desde el proceso de la UI."""
        while self.connection:
            try:
                msg = self.connection.recv()
                logging.info(f"Mensaje recibido de la UI: {msg}")
                
                if msg.get("status") == "media_loaded":
                    self.media_loaded = True
                    logging.info(tr("hotkey_media_loaded_activated"))
                
                elif msg.get("status") == "media_unloaded":
                    self.media_loaded = False
                    logging.info(tr("hotkey_media_unloaded_deactivated"))

                elif msg.get("status") == "ui_closing":
                    logging.info(tr("hotkey_ui_closing_server_terminating"))
                    return False # Devuelve False para salir del bucle principal

            except (EOFError, BrokenPipeError):
                logging.warning(tr("hotkey_ui_disconnected"))
                self.media_loaded = False
                break # Sale del bucle de mensajes y espera una nueva conexión
        
        return True # Continúa esperando conexiones

    def run(self):
        """Inicia el servidor, espera conexiones y gestiona los mensajes."""
        logging.info(tr("hotkey_server_starting"))
        
        # Activar hotkeys
        press_callbacks, release_callbacks = self._get_hotkey_callbacks()
        self.hotkey_manager.start(press_callbacks, release_callbacks)

        with Listener(self.address, authkey=self.authkey) as listener:
            logging.info(tr("hotkey_server_listening_on", address_ip=self.address[0], address_port=self.address[1]))
            while True:
                try:
                    logging.info(tr("hotkey_waiting_for_ui_conn"))
                    self.connection = listener.accept()
                    logging.info(tr("hotkey_ui_connected_from", last_accepted_address=listener.last_accepted))
                    
                    # Entra en un bucle para manejar los mensajes de este cliente
                    if not self._handle_client_messages():
                        break # Salir si la UI indica cierre

                except Exception as e:
                    logging.error(tr("hotkey_server_loop_error", error_message=e), exc_info=True)
                    time.sleep(5) # Esperar antes de reintentar
        
        self.hotkey_manager.stop()
        logging.info(tr("hotkey_server_stopped"))


def main():
    """Punto de entrada del servidor de hotkeys."""
    if not is_admin():
        logging.critical(tr("hotkey_admin_required_critical"))
        # Pequeña pausa para que el usuario pueda leer el mensaje si se ejecuta en una ventana que se cierra sola.
        time.sleep(5)
        sys.exit(1)
        
    server = HotkeyServer(ADDRESS, PORT, AUTH_KEY)
    try:
        server.run()
    except KeyboardInterrupt:
        logging.info(tr("hotkey_keyboard_interrupt"))
    except Exception as e:
        logging.critical(tr("hotkey_fatal_error", error_message=e), exc_info=True)
        time.sleep(10)

if __name__ == "__main__":
    main()
