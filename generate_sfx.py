import struct
import math
import wave
import random

def generate_wav(filename, samples_data, sample_rate=44100):
    with wave.open(filename, 'w') as f:
        f.setnchannels(2)
        f.setsampwidth(2)
        f.setframerate(sample_rate)
        for s in samples_data:
            val = int(s)
            f.writeframes(struct.pack('<h', val))
            f.writeframes(struct.pack('<h', val))  # stereo

def coin_sound(filename="coin.wav"):
    sr = 44100
    samples = []
    for i in range(int(sr * 0.2)):
        t = i / sr
        env = max(0, 1.0 - t / 0.2)
        val = math.sin(2 * math.pi * 880 * t) * env * 0.5
        val += math.sin(2 * math.pi * 1320 * t) * env * 0.3
        val += math.sin(2 * math.pi * 1760 * t) * env * 0.1
        samples.append(val * 20000)
    generate_wav(filename, samples, sr)
    print(f"Generated {filename}")

def explode_sound(filename="explode.wav"):
    sr = 44100
    samples = []
    for i in range(int(sr * 0.5)):
        t = i / sr
        env = max(0, 1.0 - t / 0.5)
        noise = random.uniform(-1, 1)
        low = math.sin(2 * math.pi * 60 * t)
        mid = math.sin(2 * math.pi * 120 * t)
        val = (noise * 0.4 + low * 0.4 + mid * 0.2) * env * 0.6
        samples.append(val * 20000)
    generate_wav(filename, samples, sr)
    print(f"Generated {filename}")

if __name__ == '__main__':
    coin_sound()
    explode_sound()
