import math
import random


class WaveformSimulator:
    def __init__(self, total_points=50000):
        self.total_points = total_points

        # Señal base (NO se regenera salvo reset duro)
        self._base_data = self._generate()

        # Energía visual dinámica
        self._energy = 1.0
        self._target_energy = 1.0

    # ---------------------------------------------------------
    # GENERACIÓN BASE
    # ---------------------------------------------------------

    def _generate(self):
        data = []
        phase = 0.0

        for _ in range(self.total_points):
            base = math.sin(phase) * 0.6
            harmonic = math.sin(phase * 2.5) * 0.3
            noise = random.uniform(-0.25, 0.25)

            amp = base + harmonic + noise
            amp = max(-1.0, min(1.0, amp))

            data.append(amp)
            phase += 0.035

        return data

    # ---------------------------------------------------------
    # API PÚBLICA
    # ---------------------------------------------------------

    def get_window(self, position: float, width: int):
        """
        Devuelve una ventana de amplitudes moduladas por energía.
        """
        position = max(0.0, min(1.0, position))
        center_index = int(position * self.total_points)

        window_size = width
        start = center_index - window_size // 4
        end = start + window_size

        if start < 0:
            start = 0
            end = window_size

        if end > self.total_points:
            end = self.total_points
            start = end - window_size

        window = self._base_data[start:end]

        if len(window) < window_size:
            window += [0.0] * (window_size - len(window))

        # 🔥 aplicar energía dinámica
        self._update_energy()
        return [v * self._energy for v in window]

    # ---------------------------------------------------------
    # ENERGÍA VISUAL (CLAVE)
    # ---------------------------------------------------------

    def reset_energy(self, soft=True):
        """
        Reinicia la energía visual del waveform.

        soft=True  → reinicio suave (FINISHED)
        soft=False → reinicio total (STOP / LOAD)
        """
        if soft:
            # Bajamos energía, pero permitimos que vuelva sola
            self._energy = 0.15
            self._target_energy = 1.0
        else:
            # Reset completo
            self._energy = 1.0
            self._target_energy = 1.0

    def _update_energy(self):
        """
        Transición suave de energía (evita congelamiento visual).
        """
        if self._energy < self._target_energy:
            self._energy += 0.02
            if self._energy > self._target_energy:
                self._energy = self._target_energy
