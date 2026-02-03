# core/dpi.py


def enable_dpi_awareness():
    """
    Activa el reconocimiento de DPI en Windows para que la aplicación no se vea borrosa
    en pantallas con escalado superior al 100%.
    Debe llamarse antes de crear la ventana principal de Tkinter.
    """
    import ctypes
    try:
        # Windows 8.1 y superior
        shcore = ctypes.WinDLL('shcore', use_last_error=True)
        shcore.SetProcessDpiAwareness(1)
        print("DPI awareness establecido a 'Per-Monitor Aware'.")
    except (AttributeError, OSError):
        try:
            # Windows Vista y superior
            user32 = ctypes.WinDLL('user32', use_last_error=True)
            user32.SetProcessDPIAware()
            print("DPI awareness establecido a 'System DPI Aware'.")
        except (AttributeError, OSError):
            print("Advertencia: No se pudo establecer el DPI awareness. La UI puede aparecer borrosa.")

def get_tkinter_scalefactor(window):
    """
    Calcula el factor de escala que Tkinter debe usar basado en el DPI actual de la pantalla.
    El valor base de Windows es 96 DPI, que corresponde a una escala del 100%.
    """
    try:
        dpi = window.winfo_fpixels('1i')
        scale = dpi / 96.0
        # No escalar si el factor es menor o igual a 1 para evitar encoger la UI
        return scale if scale > 1 else 1
    except Exception:
        return 1
