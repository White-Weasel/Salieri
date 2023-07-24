from .GladosTTS import GladosTTS
import sounddevice as sd


class Mouth:
    def __init__(self, audio_output_device=None, tts_model=None):
        if tts_model is None:
            tts_model = GladosTTS
        self.tts_model = tts_model
        pass

    def speak(self, text, emotion, blocking=True):
        # tts_model function text_to_speech() should return a numpy array
        audio = self.tts_model.text_to_speech(text, emotion)
        sd.play(audio, blocking=blocking)


if __name__ == '__main__':
    tts = GladosTTS()
    audio = tts.text_to_speech("I'm not angry, I'm just ... disappointed")
    sd.play(audio, samplerate=22050)
    sd.wait()
