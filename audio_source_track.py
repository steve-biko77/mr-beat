# audio_source_track.py
import numpy as np

class AudioSourceTrack:
    def __init__(self, engine, wav_samples, bpm, sample_rate, min_bpm=80):
        self.engine = engine
        self.sample_rate = sample_rate
        self.min_bpm = min_bpm
        self.bpm = max(bpm, min_bpm)

        if hasattr(wav_samples, 'tobytes'):
            arr = np.frombuffer(wav_samples.tobytes(), dtype=np.int16)
        else:
            arr = np.array(wav_samples, dtype=np.int16)
        self.samples = arr
        self.nb_samples = len(arr)

        self.steps = []
        self.step_idx = 0
        self.sample_idx = 0
        self.last_trigger = 0

        self.step_nb_samples = self._calc_step(bpm)
        self.buffer_nb_samples = self._calc_step(min_bpm)
        self.silence = np.zeros(self.buffer_nb_samples, dtype=np.int16)

    def _calc_step(self, bpm):
        if bpm <= 0: return 512
        return max(1, int(self.sample_rate * 15 / bpm))

    def start(self): pass

    def set_steps(self, steps):
        if len(steps) != len(self.steps):
            self.step_idx = 0
        self.steps = list(steps)

    def set_bpm(self, bpm):
        self.bpm = max(bpm, self.min_bpm)
        self.step_nb_samples = self._calc_step(self.bpm)

    def get_bytes_array(self):
        if not self.steps or all(s == 0 for s in self.steps):
            return np.zeros(self.step_nb_samples, dtype=np.int16)

        buf = np.zeros(self.step_nb_samples, dtype=np.int16)

        if self.steps[self.step_idx] == 1:
            self.last_trigger = self.sample_idx
            end = min(self.step_nb_samples, self.nb_samples)
            buf[:end] = self.samples[:end]
        else:
            played = self.sample_idx - self.last_trigger
            if played < self.nb_samples:
                remain = self.nb_samples - played
                copy = min(self.step_nb_samples, remain)
                buf[:copy] = self.samples[played:played + copy]

        self.sample_idx += self.step_nb_samples
        self.step_idx = (self.step_idx + 1) % len(self.steps)
        return buf