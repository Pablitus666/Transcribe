# core/hotkeys.py
import threading
import logging
from gui.i18n import tr # Add this import

class HotkeyManager:
    """
    Gestiona hotkeys globales de forma más robusta usando `keyboard.add_hotkey`.
    """
    def __init__(self):
        self._lock = threading.Lock()
        self.keyboard = None  # Se inicializará de forma perezosa

    def _execute_callback(self, callback):
        """Ejecuta un callback en un hilo separado y maneja excepciones."""
        try:
            callback()
        except Exception as e:
            logging.error(tr("hotkeys_callback_error", error_message=e), exc_info=True)

    def start(self, press_callbacks: dict, release_callbacks: dict = None):
        """
        Registra las hotkeys definidas usando add_hotkey para un control granular.
        """
        with self._lock:
            # --- CARGA PEREZOSA (LAZY LOADING) ---
            if self.keyboard is None:
                try:
                    import keyboard
                    self.keyboard = keyboard
                    logging.info(tr("hotkeys_keyboard_loaded"))
                except ImportError as e:
                    logging.critical(tr("hotkeys_keyboard_import_failed", error_message=e))
                    return
            # ------------------------------------

            # Limpiar CUALQUIER estado anterior de la librería para un inicio limpio.
            # Esto es más robusto que clear_all_hotkeys().
            self.keyboard.unhook_all()

            # Instalar un hook global base. Esto a veces ayuda a estabilizar la captura
            # de eventos antes de registrar hotkeys específicas que los suprimen.
            self.keyboard.hook(lambda e: True, suppress=False)
            logging.info("Global keyboard hook installed.")

            press_callbacks = press_callbacks or {}
            release_callbacks = release_callbacks or {}

            try:
                # Registrar callbacks de pulsación
                for key, callback in press_callbacks.items():
                    # Usamos una función anónima (lambda) para asegurar que el callback se capture
                    # correctamente en el bucle y se ejecute en un hilo.
                    # El argumento `suppress=True` es clave para que la hotkey sea exclusiva.
                    self.keyboard.add_hotkey(
                        key,
                        lambda cb=callback: threading.Thread(target=self._execute_callback, args=(cb,)).start(),
                        suppress=True
                    )
                    logging.info(tr("hotkeys_press_registered", key=key))

                # Registrar callbacks de liberación
                for key, callback in release_callbacks.items():
                    self.keyboard.add_hotkey(
                        key,
                        lambda cb=callback: threading.Thread(target=self._execute_callback, args=(cb,)).start(),
                        suppress=True,
                        trigger_on_release=True
                    )
                    logging.info(tr("hotkeys_release_registered", key=key))
                
                logging.info(tr("hotkeys_all_registered"))

            except Exception as e:
                logging.critical(tr("hotkeys_critical_registration_failed", error_message=e), exc_info=True)

    def stop(self):
        """Limpia todas las hotkeys registradas."""
        with self._lock:
            if self.keyboard:
                self.keyboard.unhook_all()
                logging.info(tr("hotkeys_all_stopped_released"))
            else:
                logging.warning(tr("hotkeys_stop_failed_not_loaded"))