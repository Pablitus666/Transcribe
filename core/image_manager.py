# core/image_manager.py
from PIL import Image, ImageTk, ImageEnhance
import os

from core.image_enhancer import add_shadow
from core.utils import resource_path # Importar resource_path

def _create_disabled_pil_image(pil_image: Image.Image) -> Image.Image:
    """Crea una versión semitransparente de una imagen para usarla en estado deshabilitado."""
    if pil_image.mode != 'RGBA':
        pil_image = pil_image.convert('RGBA')
    
    alpha = pil_image.getchannel('A')
    alpha = ImageEnhance.Brightness(alpha).enhance(0.4) # Reducir opacidad al 40%
    
    disabled_img = pil_image.copy()
    disabled_img.putalpha(alpha)
    return disabled_img

class ImageManager:
    """
    Gestiona la carga, el escalado, el cacheo y la mejora de imágenes de la
    aplicación para garantizar un rendimiento óptimo y una visualización
    pulida en pantallas con cualquier densidad de píxeles (HiDPI).
    """
    def __init__(self, scale: float = 1.0):
        self.scale = scale
        self._cache = {}
        print(f"ImageManager inicializado con un factor de escala de: {self.scale:.2f}")

    def load(self, path: str, size: tuple[int, int] | None = None, enhance: bool = False, return_disabled: bool = False):
        """
        Carga una imagen, la redimensiona, aplica mejoras y, opcionalmente,
        devuelve también una versión para el estado "deshabilitado".

        :param path: Ruta al archivo de imagen.
        :param size: Tupla (width, height) o None para el tamaño original.
        :param enhance: Si es True, aplica un efecto de sombra.
        :param return_disabled: Si es True, devuelve una tupla (normal_img, disabled_img).
        :return: PhotoImage o tupla de PhotoImages.
        """
        print(f"DEBUG ImageManager.load: Attempting to load original path: '{path}'")
        # Usar resource_path para obtener la ruta correcta
        resource_full_path = resource_path(path)

        if not os.path.exists(resource_full_path):
            print(f"DEBUG ImageManager.load: Image NOT FOUND at: '{resource_full_path}' (original: '{path}')")
            return (None, None) if return_disabled else None
        else:
            print(f"DEBUG ImageManager.load: Image FOUND at: '{resource_full_path}' (original: '{path}')")

        # La clave de caché distingue entre todas las variantes
        key_normal = (resource_full_path, size, self.scale, enhance, False)
        key_disabled = (resource_full_path, size, self.scale, enhance, True)

        if return_disabled:
            if key_normal in self._cache and key_disabled in self._cache:
                return (self._cache[key_normal], self._cache[key_disabled])
        elif key_normal in self._cache:
            return self._cache[key_normal]

        try:
            pil_img = Image.open(resource_full_path).convert("RGBA")
            
            if size:
                w, h = size
                scaled_width = int(w * self.scale)
                scaled_height = int(h * self.scale)
                pil_img = pil_img.resize((scaled_width, scaled_height), Image.Resampling.LANCZOS)

            if enhance:
                if max(pil_img.width, pil_img.height) < 100:
                    pil_img = add_shadow(pil_img, offset=(1, 1), blur_radius=2, border=3)
                else:
                    pil_img = add_shadow(pil_img, offset=(2, 2), blur_radius=3, border=5)

            # Crear y cachear la imagen normal
            tk_img_normal = ImageTk.PhotoImage(pil_img)
            self._cache[key_normal] = tk_img_normal
            
            if return_disabled:
                # Crear y cachear la imagen deshabilitada
                disabled_pil_img = _create_disabled_pil_image(pil_img)
                tk_img_disabled = ImageTk.PhotoImage(disabled_pil_img)
                self._cache[key_disabled] = tk_img_disabled
                return (tk_img_normal, tk_img_disabled)

            return tk_img_normal
        except Exception as e:
            print(f"Error al procesar la imagen '{path}': {e}")
            return (None, None) if return_disabled else None
