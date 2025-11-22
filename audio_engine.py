# audio_engine.py
import sounddevice as sd
import numpy as np

from audio_source_one_shot import AudioSourceOneShot
from audio_source_mixer import AudioSourceMixer


class AudioEngine:
    SAMPLE_RATE = 44100
    BUFFER_SIZE = 256  # plus petit = moins de latence

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
        self.one_shot = AudioSourceOneShot()

    def _callback(self, outdata, frames, time, status):
        out = np.zeros(frames, dtype=np.int16)

        for source in self.active_sources[:]:
            try:
                raw = source.get_bytes(frames)
                samples = np.frombuffer(raw, dtype=np.int16)[:frames]
                out += samples
            except:
                if source in self.active_sources:
                    self.active_sources.remove(source)

        np.clip(out, -32768, 32767, out=out)
        outdata[:] = out.reshape(-1, 1)

    def play_sound(self, wav_samples):
        self.one_shot.set_samples(wav_samples)
        if self.one_shot not in self.active_sources:
            self.active_sources.append(self.one_shot)

    def create_mixer(self, all_wav_samples, bpm, nb_steps, callback, min_bpm):
        mixer = AudioSourceMixer(all_wav_samples, bpm, nb_steps, callback, min_bpm)
        self.active_sources.append(mixer)
        return mixer