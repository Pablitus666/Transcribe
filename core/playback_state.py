import json
import os
import threading
from datetime import datetime
from typing import Optional

# Ruta del archivo de estado (dentro de /config)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
STATE_FILE_PATH = os.path.join(BASE_DIR, "config", "playback_state.json")


class PlaybackState:
    """
    Gestiona el guardado y restauración automática de la posición de reproducción
    por archivo, de forma similar a SMPlayer.

    - Persistencia por ruta absoluta
    - Posición en milisegundos
    - Escrituras event-driven (no por tick)
    - Totalmente desacoplado de UI y Player
    """

    _lock = threading.Lock()

    def __init__(self):
        self._state: dict[str, dict] = {}
        self._load_state_from_disk()

    # -------------------------
    # API PÚBLICA
    # -------------------------

    def get_position(self, media_path: str) -> Optional[int]:
        """
        Devuelve la última posición guardada (ms) para el archivo,
        o None si no existe o no es válida.
        """
        path = self._normalize_path(media_path)
        entry = self._state.get(path)

        if not entry:
            return None

        position = entry.get("position_ms")
        duration = entry.get("duration_ms")

        # Validaciones defensivas
        if (
            position is None
            or duration is None
            or duration <= 0
            or position < 0
            or position > duration
        ):
            return None

        # Evitar restaurar si estaba prácticamente al final
        if position >= max(0, duration - 2000):
            return None

        return int(position)

    def save_position(self, media_path: str, position_ms: int, duration_ms: int):
        """
        Guarda la posición actual del archivo.
        """
        if (
            not media_path
            or duration_ms <= 0
            or position_ms < 0
            or position_ms > duration_ms
        ):
            return

        path = self._normalize_path(media_path)

        with self._lock:
            self._state[path] = {
                "position_ms": int(position_ms),
                "duration_ms": int(duration_ms),
                "last_seen": datetime.now().isoformat(timespec="seconds")
            }
            self._save_state_to_disk()

    def clear(self, media_path: str):
        """
        Elimina el estado guardado de un archivo específico.
        """
        path = self._normalize_path(media_path)

        with self._lock:
            if path in self._state:
                del self._state[path]
                self._save_state_to_disk()

    def clear_all(self):
        """
        Borra completamente el estado de reproducción.
        """
        with self._lock:
            self._state.clear()
            self._save_state_to_disk()

    # -------------------------
    # IMPLEMENTACIÓN INTERNA
    # -------------------------

    def _normalize_path(self, path: str) -> str:
        return os.path.normcase(os.path.abspath(path))

    def _load_state_from_disk(self):
        if not os.path.exists(STATE_FILE_PATH):
            return

        try:
            with open(STATE_FILE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    self._state = data
        except Exception:
            # Archivo corrupto → no romper la app
            self._state = {}

    def _save_state_to_disk(self):
        os.makedirs(os.path.dirname(STATE_FILE_PATH), exist_ok=True)

        try:
            with open(STATE_FILE_PATH, "w", encoding="utf-8") as f:
                json.dump(self._state, f, indent=2, ensure_ascii=False)
        except Exception:
            # Fallo silencioso: nunca bloquear la UI
            pass