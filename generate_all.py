from pathlib import Path
from synth import babbling_brook, thunderstorm
from synth.io_utils import write_wav

SAMPLE_RATE = 44100
OUT = Path('output')


def main() -> None:
    brook = babbling_brook(duration=12.0, sample_rate=SAMPLE_RATE)
    storm = thunderstorm(duration=20.0, sample_rate=SAMPLE_RATE)

    write_wav(OUT / 'babbling_brook.wav', SAMPLE_RATE, brook)
    write_wav(OUT / 'thunderstorm.wav', SAMPLE_RATE, storm)
    print('Wrote:')
    print(' -', (OUT / 'babbling_brook.wav').resolve())
    print(' -', (OUT / 'thunderstorm.wav').resolve())


if __name__ == '__main__':
    main()
