# audio_source_track.py
import numpy as np

class AudioSourceTrack:
    def __init__(self, wav_samples):
        self.set_sample(wav_samples)
        self.steps = []
        self.playhead = 0  # position dans le sample en cours de lecture

    def set_sample(self, wav_samples):
        if hasattr(wav_samples, 'tobytes'):
            self.samples = np.frombuffer(wav_samples.tobytes(), dtype=np.int16)
        else:
            self.samples = np.array(wav_samples, dtype=np.int16)

    def set_steps(self, steps):
        if len(steps) != len(self.steps):
            self.playhead = 0
        self.steps = list(steps)

    def reset(self):
        self.playhead = 0

    def render(self, n_samples, global_sample_pos, samples_per_step):
        if not self.steps or all(s == 0 for s in self.steps):
            return np.zeros(n_samples, dtype=np.int16)

        out = np.zeros(n_samples, dtype=np.int16)

        for i in range(n_samples):
            current_sample = global_sample_pos + i
            step_index = int(current_sample / samples_per_step) % len(self.steps)

            # Détection du front montant de step
            prev_step = int((current_sample - 1) / samples_per_step) % len(self.steps)
            if step_index != prev_step and self.steps[step_index]:
                self.playhead = 0  # TRIGGER !

            # Lecture du sample si le step est actif
            if self.steps[step_index] and self.playhead < len(self.samples):
                out[i] = self.samples[self.playhead]
                self.playhead += 1

        return out