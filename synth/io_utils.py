from pathlib import Path
import numpy as np
from scipy.io import wavfile


def write_wav(path: str | Path, sample_rate: int, signal: np.ndarray) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    clipped = np.clip(signal, -1.0, 1.0)
    pcm = (clipped * 32767).astype(np.int16)
    wavfile.write(path, sample_rate, pcm)
