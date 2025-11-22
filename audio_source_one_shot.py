# audio_source_one_shot.py
import numpy as np

class AudioSourceOneShot:
    def __init__(self, engine):
        self.engine = engine
        self.samples = np.array([], dtype=np.int16)
        self.pos = 0

    def start(self): pass

    def set_wav_samples(self, wav_samples):
        if hasattr(wav_samples, 'tobytes'):
            arr = np.frombuffer(wav_samples.tobytes(), dtype=np.int16)
        else:
            arr = np.array(wav_samples, dtype=np.int16)
        self.samples = arr
        self.pos = 0

    def get_bytes(self):
        if self.pos >= len(self.samples):
            return np.zeros(512, dtype=np.int16).tobytes()
        end = self.pos + 512
        chunk = self.samples[self.pos:end]
        self.pos = end
        if len(chunk) < 512:
            chunk = np.pad(chunk, (0, 512 - len(chunk)), 'constant')
        return chunk.astype(np.int16).tobytes()