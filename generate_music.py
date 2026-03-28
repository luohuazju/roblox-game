import struct
import math
import wave

def generate_bgm(filename="bgm.wav", duration=30, sample_rate=44100):
    samples = []
    total_samples = sample_rate * duration

    melody = [
        (261.6, 0.5), (329.6, 0.5), (392.0, 0.5), (440.0, 0.5),
        (523.3, 0.5), (440.0, 0.5), (392.0, 0.5), (329.6, 0.5),
        (293.7, 0.5), (349.2, 0.5), (440.0, 0.5), (349.2, 0.5),
        (329.6, 0.5), (261.6, 0.5), (293.7, 0.5), (329.6, 0.5),
        (392.0, 1.0), (329.6, 0.5), (261.6, 0.5),
        (293.7, 0.5), (329.6, 0.5), (392.0, 0.5), (440.0, 0.5),
        (392.0, 1.0), (329.6, 1.0),
    ]

    bass = [
        (130.8, 1.0), (146.8, 1.0), (164.8, 1.0), (146.8, 1.0),
        (130.8, 1.0), (110.0, 1.0), (130.8, 1.0), (146.8, 1.0),
        (164.8, 1.0), (146.8, 1.0), (130.8, 1.0), (110.0, 1.0),
    ]

    melody_sample = 0
    melody_idx = 0
    bass_sample = 0
    bass_idx = 0

    for i in range(total_samples):
        t = i / sample_rate

        mel_freq, mel_dur = melody[melody_idx % len(melody)]
        mel_samples = int(mel_dur * sample_rate)
        mel_env = 1.0 - (melody_sample / mel_samples) * 0.5
        mel = math.sin(2 * math.pi * mel_freq * t) * 0.25 * mel_env

        melody_sample += 1
        if melody_sample >= mel_samples:
            melody_sample = 0
            melody_idx += 1

        bass_freq, bass_dur = bass[bass_idx % len(bass)]
        bass_samples = int(bass_dur * sample_rate)
        bass_phase = (bass_freq * t) % 1.0
        bas = (2 * abs(2 * bass_phase - 1) - 1) * 0.15

        bass_sample += 1
        if bass_sample >= bass_samples:
            bass_sample = 0
            bass_idx += 1

        val = mel + bas
        val = max(-0.9, min(0.9, val))
        samples.append(int(val * 16000))

    # Write stereo WAV at 44100Hz
    with wave.open(filename, 'w') as f:
        f.setnchannels(2)
        f.setsampwidth(2)
        f.setframerate(sample_rate)
        for s in samples:
            f.writeframes(struct.pack('<h', s))
            f.writeframes(struct.pack('<h', s))  # duplicate for stereo

    print(f"Generated {filename} ({duration}s, 44100Hz stereo)")

if __name__ == '__main__':
    generate_bgm()
