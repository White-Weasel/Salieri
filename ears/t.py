import os
import time
import numpy as np
import speech_recognition as sr
import torch
import whisper
from queue import Queue

# TODO: Somehow we go 2.5-3 seconds delay, it might just be this pc but further testing is needed.

# ---- speech_recognition params ----
# How real time the recording is in seconds. The default from example is 2, maybe a bigger value like 12-20 is better?
# PHRASE_LENGTH_LIMIT = 2
# PHRASE_LENGTH_LIMIT = None
PHRASE_LENGTH_LIMIT = None
# How much empty space between recordings before we consider it a new line in the transcription (seconds)
PHRASE_TIMEOUT = 1.5
# Energy level for mic to detect
ENERGY_THRESHOLD = 300
# input device name
INPUT_DEVICE = 'pulse'
# -----------------------------------

MODEL = 'tiny.en'


def main():
    audio_model = whisper.load_model(MODEL)
    audio_queue = Queue()

    device_index = sr.Microphone.list_microphone_names().index(INPUT_DEVICE)

    recorder = sr.Recognizer()
    source = sr.Microphone(sample_rate=16000, device_index=device_index)
    with source:
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


if __name__ == '__main__':
    main()
