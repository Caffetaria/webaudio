import argparse
from pathlib import Path
from synth import babbling_brook, thunderstorm
from synth.io_utils import write_wav


def main() -> None:
    parser = argparse.ArgumentParser(description='Procedural audio project for Lab 3: Farnell synthesis')
    parser.add_argument('sound', choices=['brook', 'thunderstorm'], help='Which sound to render')
    parser.add_argument('--duration', type=float, default=None, help='Duration in seconds')
    parser.add_argument('--sample-rate', type=int, default=44100, help='Sample rate in Hz')
    parser.add_argument('--output', type=str, default=None, help='Output WAV path')
    args = parser.parse_args()

    duration = args.duration
    if args.sound == 'brook':
        signal = babbling_brook(duration=duration or 12.0, sample_rate=args.sample_rate)
        out = Path(args.output or 'output/babbling_brook.wav')
    else:
        signal = thunderstorm(duration=duration or 20.0, sample_rate=args.sample_rate)
        out = Path(args.output or 'output/thunderstorm.wav')

    write_wav(out, args.sample_rate, signal)
    print(f'Wrote {out.resolve()}')


if __name__ == '__main__':
    main()
