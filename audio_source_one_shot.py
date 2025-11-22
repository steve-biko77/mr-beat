# audio_source_one_shot.py
import numpy as np

class AudioSourceOneShot:
    def __init__(self):
        self.samples = np.array([], dtype=np.int16)
        self.pos = 0

    def set_samples(self, wav_samples):
        if hasattr(wav_samples, 'tobytes'):
            arr = np.frombuffer(wav_samples.tobytes(), dtype=np.int16)
        else:
            arr = np.array(wav_samples, dtype=np.int16)
        self.samples = arr
        self.pos = 0

    def get_bytes(self, n):
        if self.pos >= len(self.samples):
            return b'\x00\x00' * n
        end = min(self.pos + n, len(self.samples))
        chunk = self.samples[self.pos:end]
        self.pos = end
        pad = n - len(chunk)
        return chunk.tobytes() + b'\x00\x00' * pad