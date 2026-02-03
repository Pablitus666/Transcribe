# core/audio_engine.py
import logging


class AudioEngine:
    """
    Capa de abstracción de audio.
    Separa claramente:
    - Volumen (monitoring/output)
    - Ganancia (dB, procesamiento)

    El volumen NO altera la señal, solo la salida.
    """

    def __init__(self, player):
        self.player = player

        # Volumen normalizado [0.0 - 1.0]
        self._volume = 0.5

    # -------------------------------------------------
    # Volumen de salida
    # -------------------------------------------------

    def set_volume(self, value: float):
        """
        Ajusta el volumen de salida.
        """
        value = max(0.0, min(1.0, value))
        self._volume = value

        try:
            # VLC usa volumen [0 - 200], donde 100 es normal.
            # Mapeamos nuestro [0.0 - 1.0] a [0 - 200] para un control más intuitivo.
            vlc_volume = int(self._volume * 200)
            self.player.set_volume_percent(vlc_volume)
        except Exception as e:
            logging.warning(f"Error ajustando volumen: {e}")

    def get_volume(self) -> float:
        return self._volume

    # -------------------------------------------------
    # Integración con dB Gain (existente)
    # -------------------------------------------------

    def set_gain_db(self, db_value: float):
        """
        Delegado al reproductor para procesamiento de señal.
        """
        self.player.set_gain_db(db_value)
