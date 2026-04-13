import numpy as np
from .noise import brown_noise
from .filters import lowpass, TimeVaryingHighpass


def babbling_brook(duration: float = 12.0, sample_rate: int = 44100, seed: int = 7) -> np.ndarray:
    """Approximate the SuperCollider patch:

    {RHPF.ar(LPF.ar(BrownNoise.ar(), 400), LPF.ar(BrownNoise.ar(), 14) * 400 + 500, 0.03, 0.1)}.play

    Interpreted in Python as:
    1) brown noise -> LPF at 400 Hz
    2) another brown noise -> LPF at 14 Hz -> scale to make a moving filter frequency
    3) time-varying resonant high-pass filter on the first signal
    4) output gain trim
    """
    rng = np.random.default_rng(seed)

    source = brown_noise(duration, sample_rate, amplitude=0.55, rng=rng)
    source = lowpass(source, 400.0, sample_rate, order=2)

    modulator = brown_noise(duration, sample_rate, amplitude=1.0, rng=rng)
    modulator = lowpass(modulator, 14.0, sample_rate, order=2)
    freqs = np.clip(modulator * 400.0 + 500.0, 80.0, 2400.0)

    hp = TimeVaryingHighpass(sample_rate)
    # In SC, rq is reciprocal of Q-ish width. A small rq creates resonance.
    q = 1.0 / 0.03
    bubbly = hp.process(source, freqs, q=q)

    # Gentle soft clip to control resonant peaks
    bubbly = np.tanh(bubbly * 1.35) * 0.16
    return bubbly.astype(np.float32)
