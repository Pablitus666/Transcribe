import threading
import time
import queue
import vlc
import os
import pathlib
import logging
from enum import Enum, auto

from core.playback_state import PlaybackState


# Renombrado de la clase y el enum para que coincida con la estructura del proyecto
class PlayerState(Enum):
    NO_MEDIA = auto()
    LOADING = auto()
    PLAYING = auto()
    PAUSED = auto()
    STOPPED = auto()
    FINISHED = auto()
    ERROR = auto()


class Player:
    def __init__(self, tk_root, playback_state: PlaybackState, on_state_change=None, on_time_changed=None, on_media_parsed=None):
        # --- Atributos de integración ---
        self.tk_root = tk_root
        self.playback_state = playback_state
        self.on_state_change = on_state_change
        self.on_time_changed = on_time_changed
        self.on_media_parsed = on_media_parsed

        # --- Atributos del reproductor VLC ---
        self.instance = vlc.Instance(["--verbose=-1"])
        self.media_player = self.instance.media_player_new()
        self._hwnd = None
        self._current_media_path = None

        # --- Atributos de estado ---
        self._state = PlayerState.NO_MEDIA
        self._command_queue = queue.Queue()
        self._running = True
        self._db_gain = 0.0
        self._monitor_volume_percent = 100

        # --- Hilo de trabajo ---
        self._thread = threading.Thread(target=self._worker_loop, daemon=True)
        self._thread.start()

    # ---------------------------------------------------------
    # API PÚBLICA (Compatible con la anterior)
    # ---------------------------------------------------------

    def load_media(self, path):
        self._command_queue.put(("load", path))

    def play(self):
        self._command_queue.put(("play", None))

    def pause(self):
        self._command_queue.put(("pause", None))

    def stop(self):
        self._command_queue.put(("stop", None))

    def release(self):
        self._running = False
        self._command_queue.put(("quit", None))
    
    def set_position(self, pos):
        self._command_queue.put(('set_position', pos))

    def set_gain_db(self, db_value):
        self._command_queue.put(('set_gain', db_value))

    def set_volume_percent(self, volume_percent):
        self._command_queue.put(('set_volume', volume_percent))
    
    def set_drawable(self, hwnd):
        self._hwnd = hwnd
        self._command_queue.put(('set_drawable', hwnd))
        
    def get_state(self):
        return self._state

    def get_current_media_path(self):
        return self._current_media_path

    # ---------------------------------------------------------
    # INTERNALS (Lógica principal del hilo de trabajo)
    # ---------------------------------------------------------

    def _worker_loop(self):
        while self._running:
            try:
                # Procesar comandos de la cola de prioridad
                action, payload = self._command_queue.get(timeout=0.25)
                self._process_command(action, payload)
            
            except queue.Empty:
                # Si no hay comandos, hacer tareas de sondeo
                if self.media_player:
                    vlc_state = self.media_player.get_state()

                    # 1. Sondeo de final de archivo
                    if vlc_state == vlc.State.Ended and self._state != PlayerState.FINISHED:
                        self._update_state(PlayerState.FINISHED)
                        # No hacer nada más, esperar a que el usuario pulse Play

                    # 2. Sondeo de tiempo y posición durante la reproducción
                    elif self._state == PlayerState.PLAYING:
                        cur = self.media_player.get_time()
                        total = self.media_player.get_length()
                        self._update_time(cur, total)
                        self._save_position()

    def _process_command(self, action, payload):
        if action == "load": self._handle_load(payload)
        elif action == "play": self._handle_play()
        elif action == "pause": self._handle_pause()
        elif action == "stop": self._handle_stop()
        elif action == "quit": self._handle_quit()
        elif action == "set_position": self._handle_set_position(payload)
        elif action == "set_gain": self._handle_set_gain(payload)
        elif action == "set_volume": self._handle_set_volume(payload)
        elif action == "set_drawable": self._handle_set_drawable(payload)
            
    # ---------------------------------------------------------
    # COMMAND HANDLERS (Manejadores de acciones)
    # ---------------------------------------------------------

    def _handle_load(self, filepath):
        self._update_state(PlayerState.LOADING)
        if not os.path.exists(filepath):
            self._update_state(PlayerState.ERROR)
            return

        self._current_media_path = filepath
        media = self.instance.media_new(pathlib.Path(filepath).as_uri())
        
        # Integración de funciones que faltaban
        media.add_option(":no-hw-decoding")
        if self._hwnd:
            self.media_player.set_hwnd(self._hwnd)

        self.media_player.set_media(media)
        media.parse()
        
        # Detectar si es video
        tracks = media.tracks_get()
        self.playback_state.has_video = any(t.type == vlc.TrackType.video for t in tracks or [])
        if self.on_media_parsed:
            self.tk_root.after_idle(self.on_media_parsed)

        self.media_player.play() # Iniciar y pausar para obtener duración y estado
        time.sleep(0.05)
        self.media_player.pause()

        # Restaurar posición
        last_pos = self.playback_state.get_position(self._current_media_path)
        if last_pos and last_pos > 0:
            self.media_player.set_time(last_pos)
            logging.info(f"Posición restaurada: {last_pos} ms")

        self._worker_update_final_volume()
        self._update_state(PlayerState.PAUSED)

    def _handle_play(self):
        # Lógica de reinicio robusta
        if self.media_player.get_state() == vlc.State.Ended:
            self.media_player.stop()
            time.sleep(0.05)
            # set_time(0) es implícito al volver a dar a play tras stop

        self.media_player.play()
        self._update_state(PlayerState.PLAYING)

    def _handle_pause(self):
        self.media_player.pause()
        self._update_state(PlayerState.PAUSED)

    def _handle_stop(self):
        self._save_position()
        self.media_player.stop()
        self._current_media_path = None
        self.playback_state.has_video = False
        self._update_state(PlayerState.STOPPED)

    def _handle_quit(self):
        self._running = False
        if self.media_player:
            self.media_player.release()
        self.instance.release()

    def _handle_set_position(self, position):
        if self.media_player.is_seekable():
            self.media_player.set_position(position)
            
    def _handle_set_gain(self, gain):
        self._db_gain = gain
        self._worker_update_final_volume()

    def _handle_set_volume(self, volume):
        self._monitor_volume_percent = volume
        self._worker_update_final_volume()
        
    def _handle_set_drawable(self, hwnd):
        self._hwnd = hwnd
        if self.media_player:
            self.media_player.set_hwnd(hwnd)

    # ---------------------------------------------------------
    # HELPERS (Estado, Tiempo, Volumen)
    # ---------------------------------------------------------
    
    def _save_position(self):
        if not self._current_media_path or self.media_player is None: return
        try:
            pos = self.media_player.get_time()
            if pos > 0:
                self.playback_state.set_position(self._current_media_path, pos)
        except Exception:
            pass

    def _update_time(self, current_ms, total_ms):
        if self.on_time_changed:
            self.tk_root.after_idle(self.on_time_changed, current_ms, total_ms)

    def _update_state(self, state):
        if self._state == state:
            return
        self._state = state
        if self.on_state_change:
            self.tk_root.after_idle(self.on_state_change, state)

    def _worker_update_final_volume(self):
        if not self.media_player: return
        power = 1.8
        if self._db_gain >= 0:
            gain = 100 + ((self._db_gain / 20.0) ** power) * 100
        else:
            gain = 100 - ((abs(self._db_gain) / 20.0) ** power) * 50
        final = (gain / 100.0) * self._monitor_volume_percent
        self.media_player.audio_set_volume(int(max(0, min(final, 200))))