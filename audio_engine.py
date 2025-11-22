# audio_engine.py
import sounddevice as sd
import numpy as np

from audio_source_one_shot import AudioSourceOneShot
from audio_source_mixer import AudioSourceMixer


class AudioEngine:
    NB_CHANNELS = 1
    SAMPLE_RATE = 44100
    BUFFER_SIZE = 512  # Réduit pour moins de latence (comme audiostream)

    def __init__(self):
        self.stream = sd.OutputStream(
            samplerate=self.SAMPLE_RATE,
            channels=1,
            blocksize=self.BUFFER_SIZE,
            dtype='int16',
            latency='low',
            callback=self._callback
        )
        self.stream.start()

        self.active_sources = []
        self.audio_source_one_shot = AudioSourceOneShot(self)
        self.audio_source_one_shot.start()

    def _callback(self, outdata, frames, time, status):
        out = np.zeros(frames, dtype=np.int16)

        for source in self.active_sources[:]:
            try:
                raw = source.get_bytes()
                samples = np.frombuffer(raw, dtype=np.int16)
                n = min(len(samples), frames)
                out[:n] += samples[:n]
            except:
                pass  # source terminée ou erreur

        np.clip(out, -32768, 32767, out=out)
        outdata[:] = out.reshape(-1, 1)  # shape correct pour channels=1

    def play_sound(self, wav_samples):
        self.audio_source_one_shot.set_wav_samples(wav_samples)
        if self.audio_source_one_shot not in self.active_sources:
            self.active_sources.append(self.audio_source_one_shot)

    def create_mixer(self, all_wav_samples, bpm, nb_steps, on_step_changed, min_bpm):
        mixer = AudioSourceMixer(
            self, all_wav_samples, bpm, self.SAMPLE_RATE,
            nb_steps, on_step_changed, min_bpm
        )
        mixer.start()
        if mixer not in self.active_sources:
            self.active_sources.append(mixer)
        return mixer