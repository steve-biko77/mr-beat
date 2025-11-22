# audio_source_mixer.py
import numpy as np
from audio_source_track import AudioSourceTrack

# audio_source_mixer.py
# audio_source_mixer.py
import numpy as np

class AudioSourceMixer:
    SAMPLE_RATE = 44100

    def __init__(self, all_wav_samples, bpm, nb_steps, on_step_changed, min_bpm=80):
        self.bpm = max(bpm, min_bpm)
        self.min_bpm = min_bpm
        self.nb_steps = nb_steps
        self.on_step_changed = on_step_changed
        self.is_playing = False

        # Timing précis (16 steps = 1 mesure 4/4)
        self.samples_per_step = self.SAMPLE_RATE * 60 / self.bpm / 4
        self.total_samples = 0  # temps absolu depuis le play

        self.tracks = []
        for wav in all_wav_samples:
            track = AudioSourceTrack(wav)
            track.set_steps([0] * nb_steps)
            self.tracks.append(track)

    def set_bpm(self, bpm):
        self.bpm = max(bpm, self.min_bpm)
        self.samples_per_step = self.SAMPLE_RATE * 60 / self.bpm / 4

    def set_steps(self, track_idx, steps):
        if 0 <= track_idx < len(self.tracks):
            self.tracks[track_idx].set_steps(steps)

    def audio_play(self):
        self.is_playing = True
        self.total_samples = 0
        for track in self.tracks:
            track.reset()

    def audio_stop(self):
        self.is_playing = False

    def get_bytes(self, n_samples):
        if not self.is_playing:
            return bytes(n_samples * 2)

        mixed = np.zeros(n_samples, dtype=np.int32)

        start_sample = self.total_samples
        self.total_samples += n_samples

        for track in self.tracks:
            mixed += track.render(n_samples, start_sample, self.samples_per_step)

        # Détection du changement de step
        old_step = int(start_sample / self.samples_per_step) % self.nb_steps
        new_step = int(self.total_samples / self.samples_per_step) % self.nb_steps

        if new_step != old_step and self.on_step_changed:
            display_step = (new_step - 2) % self.nb_steps  # compensation latence
            self.on_step_changed(display_step)

        return np.clip(mixed, -32768, 32767).astype(np.int16).tobytes()