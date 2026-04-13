import numpy as np
from scipy.signal import fftconvolve
from .noise import white_noise, brown_noise
from .filters import lowpass, highpass, bandpass


def _normalize(signal: np.ndarray, peak: float = 0.95) -> np.ndarray:
    mx = np.max(np.abs(signal)) + 1e-8
    return (signal / mx * peak).astype(np.float32)



def _exp_env(n: int, attack_s: float, decay_s: float, sample_rate: int) -> np.ndarray:
    attack_n = max(1, int(attack_s * sample_rate))
    decay_n = max(1, int(decay_s * sample_rate))
    env = np.zeros(n, dtype=np.float32)
    attack = np.linspace(0.0, 1.0, attack_n, dtype=np.float32)
    decay = np.exp(-np.linspace(0.0, 6.0, decay_n, dtype=np.float32))
    env[:attack_n] = attack[: min(attack_n, n)]
    tail_len = min(decay_n, max(0, n - attack_n))
    env[attack_n : attack_n + tail_len] = decay[:tail_len]
    return env



def _simple_delay(signal: np.ndarray, sample_rate: int, delay_s: float, feedback: float, mix: float, repeats: int = 4) -> np.ndarray:
    out = signal.copy().astype(np.float32)
    delay_n = int(delay_s * sample_rate)
    echo = signal.copy().astype(np.float32)
    for i in range(repeats):
        shifted = np.zeros_like(signal)
        start = delay_n * (i + 1)
        if start < len(signal):
            shifted[start:] = echo[:-start] * (feedback ** (i + 1))
            out += shifted * mix
    return out



def thunderstorm(duration: float = 20.0, sample_rate: int = 44100, seed: int = 42) -> np.ndarray:
    rng = np.random.default_rng(seed)
    n = int(duration * sample_rate)
    mix = np.zeros(n, dtype=np.float32)

    # Rain bed: broad white noise sculpted into a hiss/spray band.
    rain = white_noise(duration, sample_rate, amplitude=0.5, rng=rng)
    rain = highpass(rain, 700.0, sample_rate, order=2)
    rain = lowpass(rain, 7000.0, sample_rate, order=2)

    # Add slow amplitude drift so it feels natural.
    drift = lowpass(white_noise(duration, sample_rate, amplitude=1.0, rng=rng), 0.4, sample_rate, order=1)
    drift = 0.6 + 0.4 * (drift - drift.min()) / (drift.max() - drift.min() + 1e-8)
    rain *= drift.astype(np.float32) * 0.16
    mix += rain

    # Wind: lower filtered brown noise with very slow gusts.
    wind = brown_noise(duration, sample_rate, amplitude=0.6, rng=rng)
    wind = bandpass(wind, 40.0, 350.0, sample_rate, order=2)
    gusts = lowpass(white_noise(duration, sample_rate, amplitude=1.0, rng=rng), 0.08, sample_rate, order=1)
    gusts = 0.25 + 0.75 * (gusts - gusts.min()) / (gusts.max() - gusts.min() + 1e-8)
    wind *= gusts.astype(np.float32) * 0.22
    mix += wind

    # Distant thunder events.
    num_events = 4
    min_gap = 2.5
    starts = np.sort(rng.uniform(1.5, max(2.0, duration - 4.0), size=num_events))
    starts = np.maximum.accumulate(starts + np.arange(num_events) * min_gap * 0.05)

    for t0 in starts:
        start_idx = int(t0 * sample_rate)
        length_s = float(rng.uniform(2.4, 4.6))
        event_n = min(int(length_s * sample_rate), n - start_idx)
        if event_n <= 0:
            continue

        body = brown_noise(event_n / sample_rate, sample_rate, amplitude=1.0, rng=rng)
        body = lowpass(body, float(rng.uniform(90, 220)), sample_rate, order=2)
        body = highpass(body, 25.0, sample_rate, order=2)
        env = _exp_env(event_n, attack_s=0.02, decay_s=length_s * 0.9, sample_rate=sample_rate)
        body = body * env * float(rng.uniform(0.35, 0.7))
        body = _simple_delay(body, sample_rate, delay_s=float(rng.uniform(0.22, 0.48)), feedback=0.5, mix=0.22, repeats=3)

        # Optional sharp crack layer for nearer strikes.
        if rng.random() < 0.6:
            crack_n = min(int(0.12 * sample_rate), event_n)
            crack = white_noise(crack_n / sample_rate, sample_rate, amplitude=1.0, rng=rng)
            crack = highpass(crack, 1800.0, sample_rate, order=2)
            crack_env = _exp_env(crack_n, attack_s=0.002, decay_s=0.07, sample_rate=sample_rate)
            body[:crack_n] += crack * crack_env * float(rng.uniform(0.12, 0.24))

        mix[start_idx : start_idx + event_n] += body.astype(np.float32)

    # Very light diffuse tail using a tiny random impulse response.
    ir_len = int(0.06 * sample_rate)
    ir = np.zeros(ir_len, dtype=np.float32)
    tap_positions = rng.integers(0, ir_len, size=24)
    ir[tap_positions] = rng.uniform(0.0, 1.0, size=24)
    ir *= np.exp(-np.linspace(0, 5, ir_len)).astype(np.float32)
    wet = fftconvolve(mix, ir, mode='full')[:n].astype(np.float32)
    mix = mix * 0.88 + wet * 0.12

    return _normalize(mix, peak=0.92)
