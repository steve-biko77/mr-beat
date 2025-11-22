# audio_source_one_shot.py
import numpy as np

class AudioSourceOneShot:
    def __init__(self):
        self.samples = np.array([], dtype=np.int16)
        self.pos = 0

    def set_samples(self, wav_samples):
        # Supporte array('h') ou numpy
        if hasattr(wav_samples, 'tobytes'):
            self.samples = np.frombuffer(wav_samples.tobytes(), dtype=np.int16)
        else:
            self.samples = np.array(wav_samples, dtype=np.int16)
        self.pos = 0

    def get_bytes(self, n_samples):
        if self.pos >= len(self.samples):
            return bytes(n_samples * 2)  # silence

        end = min(self.pos + n_samples, len(self.samples))
        chunk = self.samples[self.pos:end]
        self.pos = end

        # Padding avec du silence si le sample est fini
        if len(chunk) < n_samples:
            padding = np.zeros(n_samples - len(chunk), dtype=np.int16)
            chunk = np.concatenate([chunk, padding])

        return chunk.tobytes()