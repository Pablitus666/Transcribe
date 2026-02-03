# gui/about_window.py
import tkinter as tk
from tkinter import Toplevel
from PIL import Image, ImageTk
import os

from config import settings
from core.image_manager import ImageManager
from gui.i18n import tr # Add this import

class AboutWindow(Toplevel):
    def __init__(self, parent, image_manager: ImageManager):
        super().__init__(parent)
        self.withdraw()

        self.image_manager = image_manager
        self.title(tr("about_title"))
        self.config(bg=settings.COLOR_PRIMARY_BACKGROUND)
        self.resizable(False, False)
        
        # Guardar referencias
        self.icon_img = None
        self.robot_img = None
        self.boton_photo = None

        self._load_assets()
        
        if self.icon_img:
            self.iconphoto(True, self.icon_img)

        self._create_widgets()
        self._center_popup()

        self.transient(parent) # Mover antes de deiconify
        self.grab_set()        # Mover antes de deiconify
        self.deiconify()

    def _load_assets(self):
        """Carga las imágenes necesarias usando el ImageManager."""
        self.icon_img = self.image_manager.load(settings.ICON_PATH, (32, 32))
        # El robot se carga en su tamaño original para mantener su aspecto
        self.robot_img = self.image_manager.load(settings.ROBOT_IMAGE_PATH, size=None)
        # El botón se mejora con una sombra
        self.boton_photo = self.image_manager.load(settings.BUTTON_IMAGE_PATH, (150, 55), enhance=True)

    def _create_widgets(self):
        """Crea los widgets de la ventana de información."""
        frame_info = tk.Frame(self, bg=settings.COLOR_PRIMARY_BACKGROUND)
        frame_info.pack(pady=10, padx=10, fill="both", expand=True)

        # --- Configuración de Grid para centrado y simetría ---
        frame_info.grid_columnconfigure(0, weight=1)
        frame_info.grid_columnconfigure(1, weight=1)
        frame_info.grid_rowconfigure(0, weight=1)
        frame_info.grid_rowconfigure(1, weight=1)
        frame_info.grid_rowconfigure(2, weight=1)

        if self.robot_img:
            img_label = tk.Label(frame_info, image=self.robot_img, bg=settings.COLOR_PRIMARY_BACKGROUND)
            img_label.grid(row=0, column=0, padx=10, pady=5, rowspan=3, sticky="nsew")

        message = tk.Label(
            frame_info, 
            text=tr("about_developer_info"),
            justify="center", 
            bg=settings.COLOR_PRIMARY_BACKGROUND, 
            fg=settings.COLOR_PRIMARY_TEXT,
            font=(settings.FONT_FAMILY, 18, "bold")
        )
        message.grid(row=0, column=1, rowspan=2, sticky="s", pady=(0, 20))

        if self.boton_photo:
            close_btn = tk.Button(
                frame_info, 
                text=tr("close_button"), 
                image=self.boton_photo, 
                compound="center",
                font=settings.FONT_BOLD, 
                command=self.destroy,
                bg=settings.COLOR_PRIMARY_BACKGROUND, 
                fg=settings.COLOR_PRIMARY_TEXT, 
                bd=0, 
                cursor="hand2",
                highlightthickness=0,
                activebackground=settings.COLOR_PRIMARY_BACKGROUND, 
                activeforeground=settings.COLOR_ACCENT
            )
            close_btn.bind("<Enter>", lambda e: e.widget.config(fg=settings.COLOR_ACCENT))
            close_btn.bind("<Leave>", lambda e: e.widget.config(fg=settings.COLOR_PRIMARY_TEXT))
            close_btn.grid(row=2, column=1, sticky="n", pady=(10, 0))
        else:
            close_btn_fallback = tk.Button(
                frame_info,
                text=tr("close_button"),
                command=self.destroy,
                font=settings.FONT_BOLD,
                bg=settings.COLOR_ACCENT,
                fg=settings.COLOR_PRIMARY_BACKGROUND,
                cursor="hand2"
            )
            close_btn_fallback.grid(row=2, column=1, sticky="n")

    def _center_popup(self):
        """Centra la ventana emergente en la pantalla con un tamaño fijo."""
        width = 370
        height = 230
        
        self.update_idletasks()
        
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        
        self.geometry(f"{width}x{height}+{x}+{y}")