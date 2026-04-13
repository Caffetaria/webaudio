import numpy as np


def white_noise(duration: float, sample_rate: int, amplitude: float = 1.0, rng: np.random.Generator | None = None) -> np.ndarray:
    rng = rng or np.random.default_rng()
    n = int(duration * sample_rate)
    return amplitude * rng.uniform(-1.0, 1.0, n).astype(np.float32)



def brown_noise(duration: float, sample_rate: int, amplitude: float = 1.0, rng: np.random.Generator | None = None) -> np.ndarray:
    """Brown noise similar to the WebAudio snippet from the lab prompt."""
    rng = rng or np.random.default_rng()
    n = int(duration * sample_rate)
    out = np.zeros(n, dtype=np.float32)
    last_out = 0.0
    for i in range(n):
        brown = rng.uniform(-1.0, 1.0)
        sample = (last_out + (0.02 * brown)) / 1.02
        last_out = sample
        out[i] = sample * 3.5
    out *= amplitude
    return np.clip(out, -1.0, 1.0)
