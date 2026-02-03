import tkinter as tk


class WaveformCanvas(tk.Canvas):
    def __init__(self, parent, simulator, **kwargs):
        super().__init__(
            parent,
            bg="#0B2A3A",          # fondo acorde a tu UI
            highlightthickness=0,
            bd=0,
            **kwargs
        )

        self.simulator = simulator
        self.playback_position = 0.0

        # Colores de tu paleta
        self.wave_color = "#00C8FF"
        self.wave_glow = "#4DDCFF"

    def set_playback_position(self, position: float):
        self.playback_position = position
        self.redraw()

    def redraw(self):
        self.delete("wave")

        w = self.winfo_width()
        h = self.winfo_height()
        if w <= 1 or h <= 1:
            return

        center_y = h // 2
        max_height = int(h * 0.46)

        amplitudes = self.simulator.get_window(
            self.playback_position,
            w
        )

        for x, amp in enumerate(amplitudes):
            bar = int(abs(amp) * max_height)

            # Glow suave (profundidad)
            self.create_line(
                x,
                center_y - bar - 1,
                x,
                center_y + bar + 1,
                fill=self.wave_glow,
                width=1,
                tags="wave"
            )

            # Barra principal
            self.create_line(
                x,
                center_y - bar,
                x,
                center_y + bar,
                fill=self.wave_color,
                width=1,
                tags="wave"
            )