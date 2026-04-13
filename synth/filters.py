import math
import numpy as np
from scipy.signal import butter, lfilter


def lowpass(signal: np.ndarray, cutoff_hz: float, sample_rate: int, order: int = 2) -> np.ndarray:
    nyq = 0.5 * sample_rate
    norm = min(max(cutoff_hz / nyq, 1e-6), 0.999)
    b, a = butter(order, norm, btype='low')
    return lfilter(b, a, signal).astype(np.float32)



def highpass(signal: np.ndarray, cutoff_hz: float, sample_rate: int, order: int = 2) -> np.ndarray:
    nyq = 0.5 * sample_rate
    norm = min(max(cutoff_hz / nyq, 1e-6), 0.999)
    b, a = butter(order, norm, btype='high')
    return lfilter(b, a, signal).astype(np.float32)



def bandpass(signal: np.ndarray, low_hz: float, high_hz: float, sample_rate: int, order: int = 2) -> np.ndarray:
    nyq = 0.5 * sample_rate
    low = min(max(low_hz / nyq, 1e-6), 0.999)
    high = min(max(high_hz / nyq, low + 1e-6), 0.999)
    b, a = butter(order, [low, high], btype='band')
    return lfilter(b, a, signal).astype(np.float32)


class TimeVaryingHighpass:
    """Sample-by-sample RBJ biquad high-pass filter with time-varying center frequency.

    This is an approximation of SuperCollider's RHPF behavior and works well for
    bubbling / brook-like textures where the cutoff changes continuously.
    """

    def __init__(self, sample_rate: int):
        self.sample_rate = sample_rate
        self.x1 = 0.0
        self.x2 = 0.0
        self.y1 = 0.0
        self.y2 = 0.0

    def _coeffs(self, freq: float, q: float):
        # Clamp parameters for stability
        freq = max(20.0, min(freq, 0.45 * self.sample_rate))
        q = max(0.01, q)
        w0 = 2.0 * math.pi * freq / self.sample_rate
        alpha = math.sin(w0) / (2.0 * q)
        cos_w0 = math.cos(w0)

        b0 = (1.0 + cos_w0) / 2.0
        b1 = -(1.0 + cos_w0)
        b2 = (1.0 + cos_w0) / 2.0
        a0 = 1.0 + alpha
        a1 = -2.0 * cos_w0
        a2 = 1.0 - alpha

        return (
            b0 / a0,
            b1 / a0,
            b2 / a0,
            a1 / a0,
            a2 / a0,
        )

    def process(self, signal: np.ndarray, freqs: np.ndarray, q: float) -> np.ndarray:
        out = np.zeros_like(signal, dtype=np.float32)
        for i, x0 in enumerate(signal):
            b0, b1, b2, a1, a2 = self._coeffs(float(freqs[i]), q)
            y0 = b0 * x0 + b1 * self.x1 + b2 * self.x2 - a1 * self.y1 - a2 * self.y2
            out[i] = y0
            self.x2 = self.x1
            self.x1 = x0
            self.y2 = self.y1
            self.y1 = y0
        return out
