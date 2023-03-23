# TODO: Next step: speaker diarization to detect multiple speaker then indentify who to response.
# TODO: Add a prompt https://platform.openai.com/docs/guides/speech-to-text/prompting.
#  It night be smarter to ask the speaker for prompt.
# TODO: Whisper is open-source and can be fine tune easily, it might be worth looking into it.
# TODO: add a sentiment detector to use with the language model.
# TODO: If possible, combine a language model with word-to-word speech to text
import os
import time
import numpy as np
import speech_recognition as sr
import torch
import whisper
from queue import Queue
from sys import platform
import threading

# ---- speech_recognition params ----
# How real time the recording is in seconds. The default from example is 2, maybe a bigger value like 12-20 is better?
# PHRASE_LENGTH_LIMIT = 2
# PHRASE_LENGTH_LIMIT = None
PHRASE_LENGTH_LIMIT = None
# How much empty space between recordings before we consider it a new line in the transcription (seconds)
# TODO: higher time out for conversation, maybe 2.5 to 3 seconds?
PHRASE_TIMEOUT = 1.5
# Energy level for mic to detect
ENERGY_THRESHOLD = 300
# input device name, only works on Linux
INPUT_DEVICE = 'pulse'
# -----------------------------------

MODEL = 'base.en'


def get_microphone():
    if 'linux' in platform:
        mic_name = INPUT_DEVICE
        if not mic_name or mic_name == 'list':
            print("Available microphone devices are: ")
            for index, name in enumerate(sr.Microphone.list_microphone_names()):
                print(f"Microphone with name \"{name}\" found")
            return
        else:
            for index, name in enumerate(sr.Microphone.list_microphone_names()):
                if mic_name in name:
                    return sr.Microphone(sample_rate=16000, device_index=index)
    else:
        return sr.Microphone(sample_rate=16000)


def main():
    audio_model = whisper.load_model(MODEL)
    audio_queue = Queue()

    device_index = sr.Microphone.list_microphone_names().index(INPUT_DEVICE)

    recorder = sr.Recognizer()
    with get_microphone() as source:
        recorder.adjust_for_ambient_noise(source)
    # recorder.dynamic_energy_threshold = True
    recorder.dynamic_energy_threshold = False
    recorder.energy_threshold = ENERGY_THRESHOLD
    recorder.pause_threshold = PHRASE_TIMEOUT
    conversation = []

    def record_callback(_, audio: sr.AudioData) -> None:
        """
        Threaded callback function to receive audio data when recordings finish.
        audio: An AudioData containing the recorded bytes.
        """
        # Grab the raw bytes and push it into the thread safe queue.
        audio.end_time_stamp = time.perf_counter()
        audio_queue.put(audio)

    ter_func = recorder.listen_in_background(source, record_callback, phrase_time_limit=PHRASE_LENGTH_LIMIT)
    while True:
        if not audio_queue.empty():
            phrase_audio = audio_queue.get()
            phrase_end_time_stamp = phrase_audio.end_time_stamp
            phrase_audio = np.frombuffer(phrase_audio.frame_data, np.int16).flatten().astype(np.float32) / 32768.0
            result = audio_model.transcribe(phrase_audio, fp16=torch.cuda.is_available())
            e_time = time.perf_counter()
            text = result['text'].strip()
            conversation.append(text)
            os.system('cls' if os.name == 'nt' else 'clear')
            for line in conversation:
                print(line)
            # Flush stdout.
            print(f"--- real-time diff: {e_time - phrase_end_time_stamp} seconds ---", end='', flush=True)


class Ears(threading.Thread):
    # FIXME: Copy the StopableThread over and use it for this class
    def __init__(self, input_device=None, audio_model=None, diarization=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not input_device:
            input_device = get_microphone()
        self.input_device = input_device
        if not audio_model:
            audio_model = whisper.load_model(MODEL)
        self.audio_model = audio_model
        self.phrase_audio_queue = Queue()

    def listen(self):
        """ Run on another thread, constantly listening to the input device. Call"""
        self.start()

    def run(self):
        conversation = []
        while True:
            if not self.phrase_audio_queue.empty():
                phrase_audio = self.phrase_audio_queue.get()
                phrase_end_time_stamp = phrase_audio.end_time_stamp
                phrase_audio = np.frombuffer(phrase_audio.frame_data, np.int16).flatten().astype(np.float32) / 32768.0
                result = self.audio_model.transcribe(phrase_audio, fp16=torch.cuda.is_available())
                e_time = time.perf_counter()
                text = result['text'].strip()
                conversation.append(text)
                os.system('cls' if os.name == 'nt' else 'clear')
                for line in conversation:
                    print(line)
                # Flush stdout.
                print(f"--- real-time diff: {e_time - phrase_end_time_stamp} seconds ---", end='', flush=True)


if __name__ == '__main__':
    main()
