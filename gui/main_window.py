# gui/main_window.py
import tkinter as tk
from tkinter import ttk, filedialog
from tkinterdnd2 import DND_FILES
import os
import logging
import time
import threading

from config import settings
from gui.about_window import AboutWindow
from gui.progress_bar import ProgressCanvas
from gui.audio_placeholder import AudioPlaceholder
from core.player import Player, PlayerState
from core.image_manager import ImageManager
from core.playback_state import PlaybackState
from core.waveform_simulator import WaveformSimulator
from gui.waveform_canvas import WaveformCanvas
from gui.i18n import tr # Add this import
from core.audio_engine import AudioEngine
from gui.volume_slider import VolumeSlider

class MainWindow(ttk.Frame):
    def __init__(self, parent, scale_factor=1.0, ipc_connection=None):
        super().__init__(parent)
        self.parent = parent
        self.scale_factor = scale_factor
        self.ipc_connection = ipc_connection
        
        self.about_window = None
        self._is_user_seeking = False
        self._total_duration_ms = 0
        self._current_time_ms = 0
        self._last_delete_time = 0
        self._last_stop_press_time = 0
        self._seeking_after_id = None
        self._seek_target_ms = 0  # Variable para el seek continuo
        self._has_resumed_playback = False # Flag para la reanudación única
        self._should_reset_audio_controls = False # Flag para resetear controles de audio

        self.image_manager = ImageManager(scale_factor)
        self.playback_state = PlaybackState() # Instanciar PlaybackState PRIMERO
        self.waveform_simulator = WaveformSimulator() # Instanciar WaveformSimulator
        self.player = Player(parent,
                             self.playback_state, # Pasarlo al player
                             on_state_change=self._on_player_state_change,
                             on_time_changed=self._on_player_time_changed,
                             on_media_parsed=self._on_media_parsed)
        self.audio_engine = AudioEngine(self.player)
        self.current_media_path = None # Para rastrear el archivo actual


        self._load_assets()
        self._configure_window()
        self._create_widgets()
        
        if ipc_connection:
            self.ipc_listener_thread = threading.Thread(target=self._ipc_listener, daemon=True)
            self.ipc_listener_thread.start()

        self.parent.protocol("WM_DELETE_WINDOW", self._on_closing)
        self.parent.after(100, lambda: self.player.set_drawable(self.video_frame.winfo_id()))
        self.parent.after(150, lambda: self._on_player_state_change(self.player.get_state()))

    def _on_media_parsed(self):
        """
        Callback que se ejecuta cuando el Player ha terminado de analizar
        las pistas del medio. Aquí es seguro actualizar la UI.
        """
        logging.info("Media parsed, updating display.")
        self._update_media_display()

    def _ipc_listener(self):
        while True:
            try:
                msg = self.ipc_connection.recv()
                if msg.get("command"): self.parent.after(0, self._process_ipc_command, msg.get("command"))
            except (EOFError, BrokenPipeError):
                logging.warning("Se ha perdido la conexión con el servidor de hotkeys.")
                break

    def _process_ipc_command(self, command):
        logging.info(f"Procesando comando IPC: '{command}'")
        if command == 'toggle_play_pause': self._toggle_play_pause()
        elif command == 'pause_only': self._pause_only()
        elif command == 'seek_backward': self._start_continuous_seek("backward")
        elif command == 'seek_forward': self._start_continuous_seek("forward")
        elif command == 'stop_seek': self._stop_continuous_seek()
        elif command == 'delete_media': self._delete_current_media()
        elif command == 'stop_button_pressed': self._handle_stop_button_press()

    def _send_ipc_message(self, message: dict):
        if self.ipc_connection:
            try: self.ipc_connection.send(message)
            except (BrokenPipeError, EOFError): logging.warning("No se pudo enviar mensaje a hotkey server.")

    def _load_assets(self):
        self.title_photo = self.image_manager.load(settings.TITLE_IMAGE_PATH, (450, 90), enhance=True)
        self.logo_photo = self.image_manager.load(settings.LOGO_IMAGE_PATH, (70, 70), enhance=True)
        self.small_button_normal, self.small_button_disabled = self.image_manager.load(settings.BUTTON_IMAGE_PATH, (80, 45), enhance=True, return_disabled=True)
        self.large_button_normal, self.large_button_disabled = self.image_manager.load(settings.BUTTON_IMAGE_PATH, (150, 45), enhance=True, return_disabled=True)
        self.app_icon = self.image_manager.load(settings.ICON_PATH, (32, 32))

    def _configure_window(self):
        self.parent.title(tr("title"))
        self.parent.configure(bg=settings.COLOR_PRIMARY_BACKGROUND)
        self.parent.resizable(False, False)
        width, height = map(int, settings.MAIN_WINDOW_GEOMETRY.split('x'))
        x = (self.parent.winfo_screenwidth() // 2) - (width // 2)
        y = (self.parent.winfo_screenheight() // 2) - (height // 2)
        self.parent.geometry(f"{width}x{height}+{x}+{y}")
        try:
            # iconbitmap es más robusto en Windows para establecer el ícono
            self.parent.iconbitmap(settings.ICON_PATH)
        except Exception:
            # Si falla (p.ej., en un sistema no Windows o archivo corrupto),
            # el método anterior con iconphoto podría servir como fallback,
            # pero por ahora lo dejamos así para simplicidad.
            if self.app_icon:
                self.parent.iconphoto(True, self.app_icon)

    def _create_widgets(self):
        self.parent.columnconfigure(0, weight=1)
        self.parent.rowconfigure(0, weight=1)
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Main.TFrame", background=settings.COLOR_PRIMARY_BACKGROUND)
        style.configure("Controls.TFrame", background=settings.COLOR_PRIMARY_BACKGROUND)
        style.configure("TLabel", background=settings.COLOR_PRIMARY_BACKGROUND, foreground=settings.COLOR_PRIMARY_TEXT, font=settings.FONT_DEFAULT)

        # Configuración de la barra de decibelios (Scale)
        style.configure("Horizontal.TScale",
                        background=settings.COLOR_PRIMARY_BACKGROUND,
                        troughcolor='#ffffff',  # Color del canal
                        sliderrelief='flat')

        # Mapea el color del slider (thumb) para que sea siempre blanco y no cambie
        style.map("Horizontal.TScale",
          sliderbackground=[('!active', '#ffffff'),
                              ('active', '#ffffff')],
          background=[('!disabled', settings.COLOR_PRIMARY_BACKGROUND)],
          troughcolor=[('!disabled', '#ffffff')])


        main_frame = ttk.Frame(self.parent, style="Main.TFrame")
        main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)

        title_bar_frame = ttk.Frame(main_frame, style="Controls.TFrame")
        title_bar_frame.grid(row=0, column=0, sticky="ew", pady=(0, 5))
        title_bar_frame.columnconfigure(0, weight=1)
        inner_title_frame = ttk.Frame(title_bar_frame, style="Controls.TFrame")
        inner_title_frame.grid(row=0, column=0)
        if self.logo_photo:
            logo_button = tk.Button(inner_title_frame, image=self.logo_photo, bg=settings.COLOR_PRIMARY_BACKGROUND, bd=0, highlightthickness=0, activebackground=settings.COLOR_PRIMARY_BACKGROUND, cursor="hand2", command=self._show_about_window)
            logo_button.pack(side="left", padx=(0, 10))
        if self.title_photo:
            tk.Label(inner_title_frame, image=self.title_photo, bg=settings.COLOR_PRIMARY_BACKGROUND, bd=0, highlightthickness=0).pack(side="left")

        self.video_frame = tk.Frame(main_frame, bg=settings.COLOR_VIDEO_BACKGROUND)
        self.video_frame.grid(row=1, column=0, sticky="nsew", padx=(10, 10))
        self.video_frame.pack_propagate(False)
        self.video_frame.drop_target_register(DND_FILES)
        self.video_frame.dnd_bind("<<Drop>>", self._handle_drop)
        # Configurar grid interna para los elementos del video_frame
        self.video_frame.grid_rowconfigure(0, weight=1)
        self.video_frame.grid_columnconfigure(0, weight=1)

        # Instanciar el placeholder de audio
        self.audio_placeholder = AudioPlaceholder(self.video_frame)
        self.audio_placeholder.grid(row=0, column=0, sticky="nsew") # Grid it initially, its visibility will be managed

        # Instanciar el WaveformCanvas
        self.waveform_canvas = WaveformCanvas(self.video_frame, self.waveform_simulator) # Pass the simulator
        self.waveform_canvas.grid(row=0, column=0, sticky="nsew") # Grid it, its visibility will be managed

        # Crear la etiqueta de 'arrastrar y soltar' una sola vez
        self.drop_message_label = tk.Label(self.video_frame, text=tr("drag_drop_message"), font=settings.FONT_BOLD, bg=settings.COLOR_VIDEO_BACKGROUND, fg=settings.COLOR_PRIMARY_TEXT)
        self.drop_message_label.grid(row=0, column=0, sticky="nsew") # Grid it, its visibility will be managed

        # Initial state: hide placeholder and waveform, show drop message
        self.audio_placeholder.grid_remove()
        self.waveform_canvas.grid_remove()


        self.progress_bar = ProgressCanvas(main_frame,
                                           on_seek=self._on_progress_seek,
                                           height=int(12 * self.scale_factor),
                                           bg_color="#0b2027",
                                           progress_color=settings.COLOR_ACCENT,
                                           thumb_color=settings.COLOR_PRIMARY_TEXT,
                                           dpi_scale=self.scale_factor)
        self.progress_bar.grid(row=2, column=0, sticky="ew", pady=(5, 15))

        controls_frame = ttk.Frame(main_frame, style="Controls.TFrame")
        controls_frame.grid(row=3, column=0, sticky="ew")
        controls_frame.columnconfigure([0, 2], weight=1)
        controls_frame.columnconfigure(1, weight=0)

        info_frame = ttk.Frame(controls_frame, style="Controls.TFrame")
        info_frame.grid(row=0, column=0, sticky='w')
        self.status_label = ttk.Label(info_frame, text=tr("ready_status"), font=settings.FONT_DEFAULT, anchor='w', width=24)
        self.status_label.pack(side='top', anchor='w', padx=5)
        self.time_label = ttk.Label(info_frame, text="00:00 / 00:00", font=settings.FONT_DEFAULT, width=15)
        self.time_label.pack(side='top', anchor='w', padx=5)

        gain_frame = ttk.Frame(controls_frame, style="Controls.TFrame")
        gain_frame.grid(row=0, column=2, sticky='e', padx=(10, 0))
        gain_frame.columnconfigure(0, weight=1)
        gain_label_frame = ttk.Frame(gain_frame, style="Controls.TFrame")
        gain_label_frame.grid(row=0, column=0, sticky='ew')
        ttk.Label(gain_label_frame, text=tr("gain_label"), font=settings.FONT_DEFAULT).grid(row=0, column=0, sticky='w')
        self.gain_value_label = ttk.Label(gain_frame, text="0.0 dB", font=settings.FONT_DEFAULT, width=8, anchor='w')
        self.gain_value_label.grid(row=0, column=1, sticky='w', padx=(5,0))
        self.gain_var = tk.DoubleVar(value=0.0)
        self.gain_slider = ttk.Scale(gain_frame, from_=-20.0, to=20.0, orient="horizontal", command=self._on_gain_slider_changed, variable=self.gain_var)
        self.gain_slider.grid(row=1, column=0, columnspan=2, sticky='ew')

        # --- Barra de Volumen (Monitoring) ---
        self.volume_slider = VolumeSlider(gain_frame, self.audio_engine)
        self.volume_slider.grid(row=2, column=0, columnspan=2, sticky='ew', pady=(10, 0))

        button_container = ttk.Frame(controls_frame, style="Controls.TFrame")
        button_container.grid(row=0, column=1)
        self.rewind_button = self._create_image_button(button_container, tr("rewind_button"), None, self.small_button_normal, self.small_button_disabled)
        self.rewind_button.pack(side="left", padx=2)
        self.rewind_button.bind("<ButtonPress-1>", lambda e: self._start_continuous_seek("backward"))
        self.rewind_button.bind("<ButtonRelease-1>", lambda e: self._stop_continuous_seek())
        self.play_pause_button = self._create_image_button(button_container, tr("play_button"), self._toggle_play_pause, self.small_button_normal, self.small_button_disabled)
        self.play_pause_button.pack(side="left", padx=2)
        self.stop_button = self._create_image_button(button_container, tr("stop_button"), self._handle_stop_button_press, self.small_button_normal, self.small_button_disabled)
        self.stop_button.pack(side="left", padx=2)
        self.forward_button = self._create_image_button(button_container, tr("forward_button"), None, self.small_button_normal, self.small_button_disabled)
        self.forward_button.pack(side="left", padx=2)
        self.forward_button.bind("<ButtonPress-1>", lambda e: self._start_continuous_seek("forward"))
        self.forward_button.bind("<ButtonRelease-1>", lambda e: self._stop_continuous_seek())

        bottom_buttons_frame = ttk.Frame(controls_frame, style="Controls.TFrame")
        bottom_buttons_frame.grid(row=1, column=0, columnspan=3, sticky='ew', pady=(10,0))
        bottom_buttons_frame.columnconfigure([0, 3], weight=1)
        self.load_file_button = self._create_image_button(bottom_buttons_frame, tr("load_file_button"), self._load_file_from_dialog, self.large_button_normal, self.large_button_disabled)
        self.load_file_button.grid(row=0, column=1, padx=5)
        self.exit_button = self._create_image_button(bottom_buttons_frame, tr("exit_button"), self._on_closing, self.large_button_normal, self.large_button_disabled)
        self.exit_button.grid(row=0, column=2, padx=5)

    def _create_image_button(self, parent, text, cmd, img_normal, img_disabled):
        btn = tk.Button(parent, text=text, image=img_normal, compound="center", font=settings.FONT_BOLD, command=cmd, bg=settings.COLOR_PRIMARY_BACKGROUND, fg=settings.COLOR_PRIMARY_TEXT, bd=0, cursor="hand2", highlightthickness=0, activebackground=settings.COLOR_PRIMARY_BACKGROUND, activeforeground=settings.COLOR_ACCENT)
        btn.image_normal = img_normal
        btn.image_disabled = img_disabled
        btn.bind("<Enter>", lambda e: e.widget.config(fg=settings.COLOR_ACCENT) if e.widget['state'] == tk.NORMAL else None)
        btn.bind("<Leave>", lambda e: e.widget.config(fg=settings.COLOR_PRIMARY_TEXT))
        return btn

    def _handle_drop(self, event):
        try:
            filepath = self.parent.tk.splitlist(event.data)[0]
            if self.player.get_current_media_path() and os.path.normpath(self.player.get_current_media_path()) == os.path.normpath(filepath):
                original_text = self.status_label.cget("text")
                self.status_label.config(text=tr("file_already_loaded"))
                self.parent.after(2000, lambda: self.status_label.config(text=original_text) if self.status_label.cget("text") == tr("file_already_loaded") else None)
                return
            if os.path.exists(filepath) and os.path.isfile(filepath):
                if settings.REMEMBER_PLAYBACK_POSITION and self.current_media_path:
                    current_position = self._current_time_ms
                    total_duration = self._total_duration_ms
                    if current_position is not None and total_duration is not None:
                        self.playback_state.save_position(self.current_media_path, current_position, total_duration)

                self._has_resumed_playback = False 
                self._reset_playback_ui()
                self._disable_all_controls()
                self.status_label.config(text=tr("loading_file_status", filename=os.path.basename(filepath)))
                self._should_reset_audio_controls = True # Reset audio controls on new media drop
                self.player.stop()
                self.parent.after(150, lambda: self.player.load_media(filepath))
                self.current_media_path = filepath
        except Exception as e: logging.error(f"Error en drop: {e}", exc_info=True)

    def _toggle_play_pause(self):
        state = self.player.get_state()
        if state == PlayerState.PLAYING:
            self.player.pause()
        elif state == PlayerState.FINISHED:
            # El reproductor VLC ya está en tiempo 0 y pausado gracias a la nueva lógica del player
            self.player.play()
        elif state in [PlayerState.PAUSED, PlayerState.STOPPED]:
            self.player.play()

    def _handle_stop_button_press(self):
        """Gestiona el botón de parada con lógica de doble clic.
        - Un clic: Pausa la reproducción.
        - Doble clic: Detiene y reinicia la reproducción por completo.
        """
        current_time = time.time()
        # Umbral para el doble clic en segundos
        DOUBLE_CLICK_THRESHOLD = 0.5

        if (current_time - self._last_stop_press_time) < DOUBLE_CLICK_THRESHOLD:
            # Es un doble clic
            logging.info("Doble clic en Detener: reiniciando.")
            self._should_reset_audio_controls = True # Reset audio controls on full stop
            self.player.stop()
            # Reseteamos el tiempo para que el próximo clic sea simple
            self._last_stop_press_time = 0
        else:
            # Es un solo clic
            logging.info("Un solo clic en Detener: pausando.")
            self._pause_only()
            # Guardamos el tiempo de este clic
            self._last_stop_press_time = current_time

    def _pause_only(self):
        if self.player.get_state() == PlayerState.PLAYING: self.player.pause()

    def _delete_current_media(self):
        if time.time() - self._last_delete_time < 0.5: return
        self._last_delete_time = time.time()
        if self.player.get_state() != PlayerState.NO_MEDIA:
            self._should_reset_audio_controls = True # Reset audio controls on media delete
            self.player.stop()

    def _load_file_from_dialog(self):
        filepath = filedialog.askopenfilename(title="Seleccionar archivo")
        if filepath: self._handle_drop(type('event', (object,), {'data': f"{{{filepath}}}"})())

    def _start_continuous_seek(self, direction):
        if self.player.get_state() not in [PlayerState.PLAYING, PlayerState.PAUSED]: return
        
        self._is_user_seeking = True
        self._seek_target_ms = self.progress_bar._current_ms
        if self._seeking_after_id:
            self.parent.after_cancel(self._seeking_after_id)
            self._seeking_after_id = None
        
        self._perform_seek_step(direction)
        self._seeking_after_id = self.parent.after(150, lambda: self._continue_seeking_loop(direction))

    def _continue_seeking_loop(self, direction):
        if not self._is_user_seeking: return
        self._perform_seek_step(direction)
        self._seeking_after_id = self.parent.after(100, lambda: self._continue_seeking_loop(direction))

    def _perform_seek_step(self, direction):
        self._seek_target_ms += settings.SEEK_INTERVAL_MS if direction == "forward" else -settings.SEEK_INTERVAL_MS
        self._seek_target_ms = max(0, min(self._total_duration_ms, self._seek_target_ms))
        
        self.progress_bar.set_progress(self._seek_target_ms, self._total_duration_ms)
        
        if self._total_duration_ms > 0:
            new_position = self._seek_target_ms / self._total_duration_ms
            self.player.set_position(new_position)

    def _stop_continuous_seek(self):
        if self._seeking_after_id:
            self.parent.after_cancel(self._seeking_after_id)
            self._seeking_after_id = None
        
        self.parent.after(150, lambda: setattr(self, '_is_user_seeking', False))

    def _on_player_state_change(self, state):
        logging.info(f"UI State Change: {state}")
        # La llamada a _update_media_display() se ha movido a _on_media_parsed

        if state in [PlayerState.PLAYING, PlayerState.PAUSED]:
            self._is_user_seeking = False
            
            if not self._has_resumed_playback and settings.REMEMBER_PLAYBACK_POSITION and self.current_media_path:
                saved_position_ms = self.playback_state.get_position(self.current_media_path)
                if saved_position_ms is not None and saved_position_ms > 0:
                    current_duration = self._total_duration_ms
                    if current_duration is not None and current_duration > 0:
                        position_float = saved_position_ms / current_duration
                        self.player.set_position(position_float)
                        self._has_resumed_playback = True
                        minutes, seconds = divmod(saved_position_ms // 1000, 60)
                        self.status_label.config(text=tr("resuming_from_status", minutes=minutes, seconds=seconds))
                        self.parent.after(3000, lambda: self.status_label.config(text=tr("playing_status")) if self.player.get_state() == PlayerState.PLAYING else None)
                else:
                    self._has_resumed_playback = True
        
        if state == PlayerState.PLAYING:
            self.status_label.config(text=tr("playing_status"))
            self._update_button(self.play_pause_button, tr("pause_button"))
            self._enable_controls(for_playback=True)
            self._send_ipc_message({"status": "media_loaded"})
            # Llamar a _update_media_display de forma asíncrona para evitar posibles conflictos
            self.parent.after_idle(self._update_media_display)
            # if not self.playback_state.has_video:  # Esta línea y la siguiente eran para el audio_placeholder
            #     self.audio_placeholder.start_animation() # Eliminada
        elif state == PlayerState.PAUSED:
            self.status_label.config(text=tr("paused_status"))
            self._update_button(self.play_pause_button, tr("play_button"))
            self._enable_controls(for_playback=True)
            self._send_ipc_message({"status": "media_loaded"})
            if not self.playback_state.has_video:
                self.audio_placeholder.pause_animation()
            if settings.REMEMBER_PLAYBACK_POSITION and self.current_media_path:
                current_position = self._current_time_ms
                total_duration = self._total_duration_ms
                if current_position is not None and total_duration is not None and total_duration > 0:
                    self.playback_state.save_position(self.current_media_path, current_position, total_duration)
        elif state == PlayerState.STOPPED:
            self.status_label.config(text=tr("stopped_status"))
            self._update_button(self.play_pause_button, tr("play_button"))
            self._reset_playback_ui()
            self._enable_controls(for_playback=False)
            self._send_ipc_message({"status": "media_unloaded"})
            self.audio_placeholder.reset()
            self.waveform_simulator.reset_energy(soft=False)
            self._update_media_display()
            if settings.REMEMBER_PLAYBACK_POSITION and self.current_media_path:
                current_position = self._current_time_ms
                total_duration = self._total_duration_ms
                if current_position is not None and total_duration is not None and total_duration > 0:
                    self.playback_state.save_position(self.current_media_path, current_position, total_duration)
            
            if self._should_reset_audio_controls:
                self._reset_audio_controls_to_default() # Reset on explicit stop (new media, delete, double-click stop)
                self._should_reset_audio_controls = False # Reset the flag
        
        elif state == PlayerState.FINISHED:
            self.status_label.config(text=tr("finished_status"))
            self._update_button(self.play_pause_button, tr("play_button"))
            self.progress_bar.set_progress(self._total_duration_ms, self._total_duration_ms)
            self.waveform_simulator.reset_energy(soft=True)
            self._reset_audio_controls_to_default() # Reset on finish

        elif state in [PlayerState.NO_MEDIA, PlayerState.ERROR]:
            msg = tr("ready_status") if state == PlayerState.NO_MEDIA else tr("error_status")
            self.status_label.config(text=msg)
            self._update_button(self.play_pause_button, tr("play_button"))
            self._reset_playback_ui()
            self._disable_all_controls()
            self._send_ipc_message({"status": "media_unloaded"})
            self.audio_placeholder.reset()
            self.waveform_simulator.reset_energy(soft=False)
            self._update_media_display()
            self._reset_audio_controls_to_default() # Reset on no media or error
        elif state == PlayerState.LOADING:
            self.status_label.config(text=tr("loading_status"))
            self._disable_all_controls()

    def _on_player_time_changed(self, current_time_ms, total_time_ms):
        if self._is_user_seeking:
            return
            
        self._total_duration_ms = total_time_ms
        self._current_time_ms = current_time_ms
        if not self._is_user_seeking:
            self.progress_bar.set_progress(current_time_ms, total_time_ms)
        
        # Calculate playback_position for the waveform canvas
        playback_position = 0.0
        if total_time_ms > 0:
            playback_position = current_time_ms / total_time_ms

        self.waveform_canvas.set_playback_position(playback_position) # Update this line


        current_s, total_s = current_time_ms // 1000, total_time_ms // 1000
        self.time_label.config(text=f"{divmod(current_s,60)[0]:02}:{divmod(current_s,60)[1]:02} / {divmod(total_s,60)[0]:02}:{divmod(total_s,60)[1]:02}")

    def _on_progress_seek(self, time_ms: int):
        if self.player.get_state() not in [PlayerState.PLAYING, PlayerState.PAUSED]: return
        if self._total_duration_ms <= 0: return

        self._is_user_seeking = True
        
        new_position = time_ms / self._total_duration_ms
        self.player.set_position(new_position)
        
        self.progress_bar.set_progress(time_ms, self._total_duration_ms)
        
        self.parent.after(150, lambda: setattr(self, '_is_user_seeking', False))

    def _reset_playback_ui(self):
        self.progress_bar.reset()
        self.time_label.config(text="00:00 / 00:00")
        self._total_duration_ms = 0

    def _reset_audio_controls_to_default(self):
        # Reset Gain Slider
        self.gain_var.set(0.0)
        self.gain_value_label.config(text=f"{0.0:.1f} dB")
        self.player.set_gain_db(0.0) # Ensure player gain is also reset

        # Reset Volume Slider
        self.volume_slider.set_volume(0.5) # Set to 50%

    def _update_media_display(self):
        """
        Gestiona qué widget es visible en el video_frame (placeholder,
        mensaje de drop, o ninguno si es vídeo), evitando destruir widgets.
        """
        # Ocultar siempre todos los widgets gestionados primero
        self.audio_placeholder.grid_remove()
        self.drop_message_label.grid_remove()
        self.waveform_canvas.grid_remove() # Ocultar también el waveform canvas

        current_state = self.player.get_state()

        if current_state in [PlayerState.NO_MEDIA, PlayerState.ERROR, PlayerState.STOPPED]:
            # Mostrar solo la etiqueta de arrastrar y soltar
            self.drop_message_label.grid(row=0, column=0, sticky="nsew")
        elif self.playback_state.has_video:
            # Para vídeo, no mostramos ningún widget sobre el frame. VLC dibuja detrás.
            pass
        else: # Es solo audio y está cargado (PLAYING o PAUSED)
            self.waveform_canvas.grid(row=0, column=0, sticky="nsew") # Mostrar waveform para audio


    def _enable_controls(self, for_playback=False):
        self._update_button(self.load_file_button, state=tk.NORMAL)
        self._update_button(self.play_pause_button, state=tk.NORMAL)
        self._update_button(self.stop_button, state=tk.NORMAL)
        self._update_button(self.rewind_button, state=tk.NORMAL)
        self._update_button(self.forward_button, state=tk.NORMAL)
        self.gain_slider.config(state=tk.NORMAL if for_playback else tk.DISABLED)
    
    def _disable_all_controls(self):
        self.gain_slider.config(state=tk.DISABLED)

    def _update_button(self, button, text=None, state=None):
        if text: button.config(text=text)
        if state is not None: button.config(state=state, image=button.image_normal if state == tk.NORMAL else button.image_disabled)

    def _on_gain_slider_changed(self, value):
        self.player.set_gain_db(float(value))
        self.gain_value_label.config(text=f"{float(value):.1f} dB")

    def _show_about_window(self):
        if self.about_window is None or not self.about_window.winfo_exists():
            self.about_window = AboutWindow(self.parent, self.image_manager)
        self.about_window.focus()

    def _on_closing(self):
        if settings.REMEMBER_PLAYBACK_POSITION and self.current_media_path and self.player.get_state() not in [PlayerState.NO_MEDIA, PlayerState.ERROR]:
            current_position = self._current_time_ms
            total_duration = self._total_duration_ms
            if current_position is not None and total_duration is not None and total_duration > 0:
                self.playback_state.save_position(self.current_media_path, current_position, total_duration)

        self._send_ipc_message({"status": "ui_closing"})
        time.sleep(0.2)
        self.player.release()
        self.parent.quit()
