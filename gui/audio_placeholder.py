import tkinter as tk
import random

# Colores y estilo (se podrán mover a settings.py más adelante)
COLOR_BACKGROUND = "#012a36"
COLOR_BARS_ACTIVE = "#2a9d8f"
COLOR_BARS_INACTIVE = "#A1D6E2"
BAR_COUNT = 16
ANIMATION_SPEED_MS = 100

class AudioPlaceholder(tk.Canvas):
    """
    Un widget que muestra una waveform simulada para archivos de solo audio.
    Hereda de tk.Canvas y se encarga de su propio dibujado y animación.
    """
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        
        self.configure(bg=COLOR_BACKGROUND, highlightthickness=0)
        
        self._is_animating = False
        self._after_id = None
        self.bars = []

        # Nos aseguramos de que el canvas se redibuje cuando cambia de tamaño
        self.bind("<Configure>", self._on_resize)

    def _on_resize(self, event=None):
        """Maneja el evento de redimensionamiento del canvas para recalcular las barras."""
        self.reset() # Limpia y redibuja las barras con las nuevas dimensiones

    def _setup_bars(self):
        """Inicializa o reinicializa las barras de la waveform."""
        if not self.winfo_viewable():
            # Si el widget no es visible, no podemos obtener su tamaño.
            # Lo intentaremos de nuevo más tarde.
            self.after(50, self._setup_bars)
            return
            
        canvas_width = self.winfo_width()
        canvas_height = self.winfo_height()

        if canvas_width <= 1 or canvas_height <= 1:
            # Aún no hay tamaño para dibujar, reintentar.
            self.after(50, self._setup_bars)
            return

        # Limpiar barras antiguas si existen
        for bar in self.bars:
            self.delete(bar)
        self.bars.clear()

        bar_width = canvas_width / (BAR_COUNT * 2 - 1)
        
        for i in range(BAR_COUNT):
            x0 = i * (bar_width * 2)
            y0 = canvas_height
            x1 = x0 + bar_width
            y1 = canvas_height
            bar = self.create_rectangle(x0, y0, x1, y1, fill=COLOR_BARS_INACTIVE, outline="")
            self.bars.append(bar)

    def _animate(self):
        """Bucle de animación principal. Se llama a sí mismo usando after()."""
        if not self._is_animating:
            return

        canvas_height = self.winfo_height()
        
        for bar in self.bars:
            # Altura pseudo-aleatoria para la barra
            bar_height = random.randint(int(canvas_height * 0.1), int(canvas_height * 0.9))
            
            # Obtener coordenadas actuales
            x0, _, x1, _ = self.coords(bar)
            
            # Mover la barra a su nueva altura
            self.coords(bar, x0, canvas_height - bar_height, x1, canvas_height)
        
        # Programar la siguiente actualización
        self._after_id = self.after(ANIMATION_SPEED_MS, self._animate)

    # --- Interfaz Pública ---

    def start_animation(self):
        """Inicia el bucle de animación."""
        if not self.bars:
            self._setup_bars()

        for bar in self.bars:
            self.itemconfig(bar, fill=COLOR_BARS_ACTIVE)

        if not self._is_animating:
            self._is_animating = True
            self._animate()

    def pause_animation(self):
        """Detiene el bucle de animación."""
        self._is_animating = False
        if self._after_id:
            self.after_cancel(self._after_id)
            self._after_id = None
        
        for bar in self.bars:
            self.itemconfig(bar, fill=COLOR_BARS_INACTIVE)

    def reset(self):
        """Restablece el widget a su estado inicial, deteniendo la animación."""
        self.pause_animation()
        self._setup_bars() # Redibuja las barras en su posición inicial (altura cero)

    def update_theme(self, background_color, active_color, inactive_color):
        """Permite cambiar los colores del widget dinámicamente."""
        global COLOR_BACKGROUND, COLOR_BARS_ACTIVE, COLOR_BARS_INACTIVE
        COLOR_BACKGROUND = background_color
        COLOR_BARS_ACTIVE = active_color
        COLOR_BARS_INACTIVE = inactive_color
        
        self.configure(bg=COLOR_BACKGROUND)
        if self._is_animating:
            for bar in self.bars:
                self.itemconfig(bar, fill=COLOR_BARS_ACTIVE)
        else:
            for bar in self.bars:
                self.itemconfig(bar, fill=COLOR_BARS_INACTIVE)

# --- Para pruebas ---
if __name__ == '__main__':
    root = tk.Tk()
    root.title("Prueba de AudioPlaceholder")
    root.geometry("600x400")
    root.configure(bg=COLOR_BACKGROUND)

    placeholder = AudioPlaceholder(root)
    placeholder.pack(fill="both", expand=True, padx=10, pady=10)

    # Controles para la prueba
    controls_frame = tk.Frame(root, bg=COLOR_BACKGROUND)
    controls_frame.pack(pady=10)

    start_button = tk.Button(controls_frame, text="Start", command=placeholder.start_animation)
    start_button.pack(side="left", padx=5)

    pause_button = tk.Button(controls_frame, text="Pause", command=placeholder.pause_animation)
    pause_button.pack(side="left", padx=5)

    reset_button = tk.Button(controls_frame, text="Reset", command=placeholder.reset)
    reset_button.pack(side="left", padx=5)

    root.mainloop()
