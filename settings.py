# config/settings.py

# Paleta de colores principal, basada en Ico_Converter.py
COLOR_PRIMARY_BACKGROUND = "#023047"
COLOR_PRIMARY_TEXT = "white"
COLOR_ACCENT = "#fcbf49"
COLOR_WIDGET_BACKGROUND = "#1b1b1b"
COLOR_WIDGET_BACKGROUND_HOVER = "#2a2a2a"
COLOR_VIDEO_BACKGROUND = "#0b2027"

# Tipografía
FONT_FAMILY = "Comic Sans MS"
FONT_DEFAULT = (FONT_FAMILY, 12)
FONT_BOLD = (FONT_FAMILY, 12, "bold")
FONT_TITLE = (FONT_FAMILY, 22, "bold")
FONT_INFO = (FONT_FAMILY, 16, "bold")

# Títulos de ventana

# Geometría de la ventana
MAIN_WINDOW_GEOMETRY = "800x750"
ABOUT_WINDOW_GEOMETRY = "370x280"

# Rutas de recursos (iconos, imágenes)
ICON_PATH = "images/icon.ico"
ROBOT_IMAGE_PATH = "images/robot.png"
BUTTON_IMAGE_PATH = "images/boton.png"
LOGO_IMAGE_PATH = "images/logo.png" # Nuevo path para el logo clickable
TITLE_IMAGE_PATH = "images/titulo.png" # Nuevo path para el título visual

# Ruta de FFmpeg (asumiendo que está en la raíz del proyecto)
import os
FFMPEG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "ffmpeg.exe"))

# Controles del reproductor
SEEK_INTERVAL_MS = 1000 # Intervalo de salto en milisegundos (1 segundo)
FAST_SEEK_INTERVAL_MS = 5000 # Intervalo de salto rápido en milisegundos (5 segundos)

# Configuración de reproducción
REMEMBER_PLAYBACK_POSITION = True

# Internacionalización
DEFAULT_LANGUAGE = "es"

