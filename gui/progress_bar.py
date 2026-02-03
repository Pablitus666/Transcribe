import tkinter as tk


class ProgressCanvas(tk.Canvas):
    """
    Barra de progreso tipo SMPlayer.
    - Click absoluto sin saltos
    - Drag fluido
    - Progreso azul detrás
    """

    def __init__(
        self,
        parent,
        height=12,
        bg_color="#2e2e2e",
        progress_color="#2196F3",
        thumb_color="#ffffff",
        on_seek=None,
        dpi_scale=1.0, # Add dpi_scale parameter
        **kwargs
    ):
        super().__init__(
            parent,
            height=height,
            bg=bg_color,
            highlightthickness=0,
            **kwargs
        )

        self.bg_color = bg_color
        self.progress_color = progress_color
        self.thumb_color = thumb_color
        self.on_seek = on_seek
        self.dpi_scale = dpi_scale
        self._user_seeking = False
        self._current_ms = 0
        self._duration_ms = 0

        self._track_id = None
        self._progress_id = None
        self._thumb_id = None

        self.bind("<Configure>", self._redraw)
        self.bind("<Button-1>", self._on_click)
        self.bind("<B1-Motion>", self._on_drag)
        self.bind("<ButtonRelease-1>", self._on_release)

    # ──────────────────────────────
    # Public API
    # ──────────────────────────────

    def set_progress(self, current_ms, total_ms):
        if self._user_seeking:
            return

        self._current_ms = max(0, current_ms)
        self._duration_ms = max(1, total_ms)
        self._redraw()

    def reset(self):
        self._current_ms = 0
        self._duration_ms = 0
        self._redraw()

    # ──────────────────────────────
    # Drawing
    # ──────────────────────────────

    def _redraw(self, event=None):
        self.delete("all")

        width = self.winfo_width()
        height = self.winfo_height()

        if width <= 0:
            return

        # Background track
        self._track_id = self.create_rectangle(
            0, height // 3,
            width, height * 2 // 3,
            fill=self.bg_color,
            outline=""
        )

        percent = self._current_ms / self._duration_ms if self._duration_ms > 0 else 0
        played_width = int(width * percent)

        # Played track
        self._progress_id = self.create_rectangle(
            0, height // 3,
            played_width, height * 2 // 3,
            fill=self.progress_color,
            outline=""
        )

        # Thumb
        thumb_x = played_width
        self._draw_thumb(thumb_x)

    def _draw_thumb(self, x_center: int):
        """
        Dibuja el thumb estilo SMPlayer:
        barra vertical con extremos redondeados.
        """
        width = self.winfo_width()
        height = self.winfo_height()

        thumb_width = int(8 * self.dpi_scale) # Aumentado a 8px para mejor visibilidad y hitbox
        thumb_height = int(22 * self.dpi_scale) # Aumentado a 22px para mejor visibilidad
        radius = thumb_width // 2

        # Asegurarse de que el thumb no se salga de los límites
        x_center = max(thumb_width // 2, min(width - thumb_width // 2, x_center))

        x1 = x_center - thumb_width // 2
        x2 = x_center + thumb_width // 2
        y1 = height // 2 - thumb_height // 2
        y2 = height // 2 + thumb_height // 2

        # Sombra sutil
        self.create_round_rect(
            x1 + 1, y1 + 1, x2 + 1, y2 + 1,
            radius=radius,
            fill="#000000", # Negro
            outline="",
            tag="thumb_shadow"
        )

        # Thumb principal
        self.create_round_rect(
            x1, y1, x2, y2,
            radius=radius,
            fill=self.thumb_color, # Usar el color definido en el constructor (settings.COLOR_PRIMARY_TEXT, que es blanco)
            outline="",
            tag="thumb"
        )
        # Asegurarse de que el cursor cambie al pasar por encima del thumb
        self.tag_bind("thumb", "<Enter>", lambda e: self.config(cursor="hand2"))
        self.tag_bind("thumb", "<Leave>", lambda e: self.config(cursor=""))
        self.tag_bind("thumb_shadow", "<Enter>", lambda e: self.config(cursor="hand2"))
        self.tag_bind("thumb_shadow", "<Leave>", lambda e: self.config(cursor=""))


    def create_round_rect(self, x1, y1, x2, y2, radius=10, **kwargs):
        """
        Dibuja un rectángulo con esquinas redondeadas en un Canvas.
        """
        # Limitar el radio para que no sea mayor que la mitad de la dimensión más pequeña
        radius = min(radius, abs(x2 - x1) // 2, abs(y2 - y1) // 2)

        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1
        ]
        return self.create_polygon(points, smooth=True, **kwargs)

    # ──────────────────────────────
    # Mouse handling
    # ──────────────────────────────

    def _calc_time_from_x(self, x):
        width = max(1, self.winfo_width())
        percent = min(max(x / width, 0.0), 1.0)
        return int(percent * self._duration_ms)

    def _on_click(self, event):
        self._user_seeking = True
        self._current_ms = self._calc_time_from_x(event.x)
        self._redraw()

    def _on_drag(self, event):
        self._current_ms = self._calc_time_from_x(event.x)
        self._redraw()

    def _on_release(self, event):
        self._current_ms = self._calc_time_from_x(event.x)
        self._user_seeking = False
        self._redraw()

        if self.on_seek:
            self.on_seek(self._current_ms)
