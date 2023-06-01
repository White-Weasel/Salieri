# TODO: Next step: speaker diarization to detect multiple speaker then indentify who to response.
# TODO: Add a prompt https://platform.openai.com/docs/guides/speech-to-text/prompting.
#  It night be smarter to ask the speaker for prompt.
# TODO: add a sentiment detector to use with the language model.
# TODO: If possible, combine a language model with word-to-word speech to text
import os
import threading
import time
import numpy as np
import speech_recognition as sr
import torch
import whisper
import logging
import sounddevice as sd
from queue import Queue
from sys import platform

# ---- speech_recognition params ----
# How real time the recording is in seconds. The default from example is 2, maybe a bigger value like 12-20 is better?
# PHRASE_LENGTH_LIMIT = 2
# PHRASE_LENGTH_LIMIT = None
PHRASE_LENGTH_LIMIT = None
# How much empty space between recordings before we consider it a new line in the transcription (seconds)
PHRASE_TIMEOUT = 1
# Energy level for mic to detect
ENERGY_THRESHOLD = 300
# input device name, only works on Linux
INPUT_DEVICE = 'pulse'
# -----------------------------------

MODEL = 'tiny.en'
logger = logging.getLogger(__name__)
logger.level = logging.DEBUG


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
        try:
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
        except KeyboardInterrupt:
            ter_func()


class Ears:
    def __init__(self, brain, input_device=None, audio_model=None, diarization=False,
                 *args, **kwargs):
        super().__init__()
        self.input_device = input_device
        if not audio_model:
            audio_model = whisper.load_model(MODEL)
        self.audio_model = audio_model

        self.brain = brain
        self.phrase_audio_queue = Queue()

        self._stop_lock = True
        self.transcribe_thread = None

        # block audio input until Salie done response
        self._blocked = False

    @property
    def is_listening(self):
        return not self._stop_lock

    # noinspection PyAttributeOutsideInit
    def listen(self):
        """Start listening. Create 2 thread, 1 to get phrase audio and another to transcribe it"""
        assert self._stop_lock
        recorder = sr.Recognizer()
        if not self.input_device:
            device = get_microphone()
            self.input_device = device
        else:
            device = self.input_device
        with device as source:
            recorder.adjust_for_ambient_noise(source)
        recorder.dynamic_energy_threshold = True
        # recorder.dynamic_energy_threshold = False
        recorder.energy_threshold = ENERGY_THRESHOLD
        recorder.pause_threshold = PHRASE_TIMEOUT
        # TODO: bandage fix, need to find out later what should we wait for.
        time.sleep(5)
        self.stop_recording_func = recorder.listen_in_background(device, self.record_callback,
                                                                 phrase_time_limit=PHRASE_LENGTH_LIMIT)
        logger.debug("Ears is listening")
        self._stop_lock = False
        self.transcribe_thread = threading.Thread(target=self.thread_target)
        self.transcribe_thread.daemon = True
        self.transcribe_thread.start()

    def record_callback(self, _, audio: sr.AudioData) -> None:
        """
        Threaded callback function to receive audio data when recordings finish.
        audio: An AudioData containing the recorded bytes.
        """
        # Grab the raw bytes and push it into the thread safe queue.
        if not self._blocked:
            audio.end_time_stamp = time.perf_counter()
            self.phrase_audio_queue.put(audio)
            logger.debug("phrase end")
        else:
            logger.debug("\nphrase blocked")
        # result = self.recorder.recognize_whisper_api(audio,
        #                                              api_key='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') # noqa
        # text = result.strip()
        # self.conversation_queue.put(text)

    def thread_target(self):
        """ Run on another thread, constantly listening to the input device. Call stop() to stop this thread"""
        conversation = []
        self.phrase_audio_queue = Queue()
        while not self._stop_lock:
            if not self.phrase_audio_queue.empty():
                self._blocked = True
                phrase_audio = self.phrase_audio_queue.get()
                phrase_end_time_stamp = phrase_audio.end_time_stamp
                # convert audio to numpy array
                phrase_audio = np.frombuffer(phrase_audio.frame_data, np.int16).flatten().astype(np.float32) / 32768.0

                # transcribe
                ws_time = time.perf_counter()
                result = self.audio_model.transcribe(phrase_audio, fp16=torch.cuda.is_available())
                we_time = time.perf_counter()

                text = result['text'].strip()
                if self.brain:
                    conversation.append(f"Q: {text}")
                    # get language model response
                    answer = self.brain.languageProcessor.answer(text)
                    conversation.append(f"A: {answer}")
                    e_time = time.perf_counter()
                    self.brain.mouth.speak(answer, blocking=True)
                else:
                    conversation.append(text)
                    e_time = time.perf_counter()

                os.system('cls' if os.name == 'nt' else 'clear')
                for line in conversation:
                    print(line)
                # Flush stdout.
                print(f"--- whisper transcribe time: {we_time - ws_time} seconds ---", flush=True)
                print(f"--- real-time diff: {e_time - phrase_end_time_stamp} seconds ---", end='', flush=True)
                self._blocked = False
            time.sleep(0.05)

    def stop(self):
        self._stop_lock = True
        if self.transcribe_thread:
            self.transcribe_thread.join()
        self.stop_recording_func()


if __name__ == '__main__':
    # main()

    e = Ears(None)
    e.listen()
