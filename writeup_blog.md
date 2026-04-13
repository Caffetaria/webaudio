# Lab 3 Writeup: Procedural Sound Synthesis in Python

For this lab I implemented two procedural audio patches in Python. The first was a **babbling brook**, based on a short SuperCollider program from the assignment prompt. The second was a **thunderstorm ambience**, which I chose as my more challenging extra-step sound.

## Sound 1: Babbling brook

The goal of the brook patch was to recreate the bubbling, watery texture of the SuperCollider example:

```supercollider
{RHPF.ar(LPF.ar(BrownNoise.ar(), 400), LPF.ar(BrownNoise.ar(), 14) * 400 + 500, 0.03, 0.1)}.play
```

I interpreted this patch as using two streams of brown noise. The first stream becomes the main sound source and is low-pass filtered at 400 Hz. The second stream is also brown noise, but it is filtered at 14 Hz so that it changes slowly and acts like a control signal rather than an audible texture. I then used that slow control signal to move the cutoff frequency of a resonant high-pass filter over time. This creates a shifting, bubbly timbre that resembles moving water.

In Python, I approximated the resonant high-pass filter using a time-varying biquad filter. That was the main technical challenge of this part, because Python does not have a direct built-in equivalent to SuperCollider's `RHPF` unit generator.

## Sound 2: Thunderstorm ambience

For the open-ended part, I chose to build a **thunderstorm** because it was clearly more challenging and required combining multiple synthesis techniques instead of relying on a single oscillator or filter.

The thunderstorm has four main components:

1. **Rain layer**: white noise shaped with a high-pass and low-pass filter to create a soft spray texture.
2. **Wind layer**: brown noise filtered into lower frequencies, with slow amplitude changes to simulate gusts.
3. **Thunder events**: bursts of low-frequency noise shaped by an amplitude envelope.
4. **Echo and space**: a delay and diffuse tail to make the thunder feel farther away and more environmental.

This patch uses **noise-based synthesis**, **subtractive synthesis**, **modulation**, and **time-based effects**. I chose noise as the main source material because real environmental sounds such as rain, wind, and thunder are not purely pitched or harmonic. Filtering and envelopes were then used to shape that noise into more recognizable sound events.

## Process and experience

This lab felt more open-ended than earlier ones, which was initially uncomfortable, but it became easier once I started thinking in layers. Instead of trying to perfectly model a real-world sound, I focused on identifying the main textures and events that make a sound recognizable. That approach worked especially well for the thunderstorm, where layering several simple components produced a much richer result.

The babbling brook taught me how to read unfamiliar audio code and translate it into another environment. The thunderstorm pushed me to make more independent design choices. My final result does not perfectly reproduce real water or weather, but it does create believable procedural soundscapes using relatively simple building blocks.

## Signal flow graph

### Brook

```text
Brown Noise -> LPF(400 Hz) -> Time-Varying Resonant HPF -> Output
                               ^
                               |
Brown Noise -> LPF(14 Hz) -> scale(*400 + 500)
```

### Thunderstorm

```text
White Noise -> HPF -> LPF -> Rain Gain ---------------------\\
                                                             \\
Brown Noise -> Bandpass -> Gust Modulation -> Wind Gain ------> Master -> WAV Output
                                                               /
Brown Noise Burst -> LPF -> HPF -> Envelope -> Delay --------/
                          + optional White Noise Crack
```

