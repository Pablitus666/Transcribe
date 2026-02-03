# gui/volume_slider.py
import tkinter as tk
from tkinter import ttk

from config import settings
from gui.i18n import tr


class VolumeSlider(ttk.Frame):
    """
    Barra de volumen (monitoring) independiente de la ganancia en dB.
    Controla únicamente el volumen de salida del reproductor.
    """

    def __init__(self, parent, audio_engine, **kwargs):
        super().__init__(parent, **kwargs)
        self.audio_engine = audio_engine

        self.configure(style="Controls.TFrame")
        self._build_ui()

        # Establecer el valor inicial desde el motor de audio
        initial_volume = self.audio_engine.get_volume()
        initial_percent = initial_volume * 100
        self._volume_var.set(initial_percent)
        self.value_label.config(text=f"{initial_percent:.0f}%")
        self._update_label_icon(initial_volume)

    def _build_ui(self):
        """Construye la interfaz de usuario del control deslizante de volumen."""
        self._volume_var = tk.DoubleVar()

        # Configurar la columna para que se expanda
        self.columnconfigure(0, weight=1)

        # Etiqueta con icono y texto
        self.label = ttk.Label(
            self,
            text=tr("volume_label"), # Usar 'tr' para la etiqueta
            font=settings.FONT_DEFAULT, # Usar la fuente por defecto
        )
        self.label.grid(row=0, column=0, sticky='w')
        
        self.value_label = ttk.Label(
            self,
            text=f"{int(self._volume_var.get()):.0f}%",
            font=settings.FONT_DEFAULT,
            width=5,
            anchor='w'
        )
        self.value_label.grid(row=0, column=1, sticky='w', padx=(5,0))

        # Control deslizante (Slider)
        self.slider = ttk.Scale(
            self,
            from_=0,
            to=100,
            orient="horizontal",
            variable=self._volume_var,
            command=self._on_volume_changed,
            style="Horizontal.TScale" # Reutilizar el estilo del slider de ganancia
        )
        self.slider.grid(row=1, column=0, columnspan=2, sticky='ew')

    def _on_volume_changed(self, value_str: str):
        """Se llama cuando el valor del control deslizante cambia."""
        value_float = float(value_str)
        volume_normalized = value_float / 100.0
        
        self.audio_engine.set_volume(volume_normalized)
        self.value_label.config(text=f"{value_float:.0f}%")
        self._update_label_icon(volume_normalized)

    def _update_label_icon(self, volume_normalized: float):
        """Actualiza el icono de la etiqueta según el nivel de volumen."""
        if volume_normalized == 0:
            self.label.config(text="🔇")
        elif 0 < volume_normalized <= 0.5:
            self.label.config(text="🔈")
        else: # volume > 0.5
            self.label.config(text="🔊")

    def set_volume(self, value: float):
        """API pública para establecer el volumen desde fuera (p. ej., al restaurar)."""
        value = max(0.0, min(1.0, value))
        self._volume_var.set(value * 100)
        self.audio_engine.set_volume(value)
        self.value_label.config(text=f"{value * 100:.0f}%")
        self._update_label_icon(value)

    def get_volume(self) -> float:
        """API pública para obtener el volumen actual."""
        return self._volume_var.get() / 100.0
