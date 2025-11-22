# audio_source_mixer.py
import numpy as np
from audio_source_track import AudioSourceTrack

class AudioSourceMixer:
    def __init__(self, engine, all_wav_samples, bpm, sample_rate, nb_steps, on_step_changed, min_bpm):
        self.engine = engine
        self.sample_rate = sample_rate
        self.nb_steps = nb_steps
        self.min_bpm = min_bpm
        self.bpm = max(bpm, min_bpm)
        self.on_step_changed = on_step_changed
        self.is_playing = False
        self.current_step = 0

        self.tracks = []
        for samples in all_wav_samples:
            track = AudioSourceTrack(engine, samples, self.bpm, sample_rate, min_bpm)
            track.set_steps([0] * nb_steps)
            self.tracks.append(track)

    def start(self): pass

    def set_steps(self, index, steps):
        if 0 <= index < len(self.tracks):
            self.tracks[index].set_steps(steps)

    def set_bpm(self, bpm):
        self.bpm = max(bpm, self.min_bpm)
        for track in self.tracks:
            track.set_bpm(self.bpm)

    def audio_play(self):
        self.is_playing = True
        self.current_step = 0

    def audio_stop(self):
        self.is_playing = False

    def get_bytes(self):
        if not self.is_playing or not self.tracks:
            size = self.tracks[0].step_nb_samples if self.tracks else 512
            return np.zeros(size, dtype=np.int16).tobytes()

        # MAJ BPM
        for track in self.tracks:
            track.set_bpm(self.bpm)

        step_size = self.tracks[0].step_nb_samples
        mixed = np.zeros(step_size, dtype=np.int32)

        for track in self.tracks:
            buf = track.get_bytes_array()
            if len(buf) == step_size:
                mixed += buf

        np.clip(mixed, -32768, 32767, out=mixed)
        result = mixed.astype(np.int16)

        # Callback visuel avec -2 steps (comme l'original)
        if self.on_step_changed:
            display_step = (self.current_step - 2) % self.nb_steps
            self.on_step_changed(display_step)

        self.current_step = (self.current_step + 1) % self.nb_steps
        return result.tobytes()