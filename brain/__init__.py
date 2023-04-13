import logging
from queue import Queue
from ears import Ears
from utls import StopableThread
from .LanguageProcessor import LanguageProcessor
from .models import ChatGPT
from .Memory import ShortTermMemory, LongTermMemory

logger = logging.getLogger(__name__)


class Brain(StopableThread):
    __instance = None

    def __init__(self, audio_input=None, stt_model=None, diarization=False,
                 audio_output=None, tts_model=None,
                 conversation=None, llm_model=ChatGPT,
                 *args, **kwargs):
        super().__init__()
        if Brain.__instance is not None:
            raise Exception("Brain class is a singleton!")
        else:
            Brain.__instance = self

        self.longTermMemory = ShortTermMemory()
        self.shortTermMemory = LongTermMemory()
        self.conversation_queue = Queue()
        self.languageProcessor = LanguageProcessor(model=llm_model, initial_conversation=conversation)

        self.ears = Ears(self, input_device=audio_input, audio_model=stt_model, diarization=diarization)

    def wake_up(self):
        self.ears.listen()
        # self.start()

    def sleep(self):
        self.ears.stop()
        # self.stop()
    #
    # def thread_target(self):
    #     while not self._stop_lock:
    #         if not self.conversation_queue.empty():
    #             message = self.conversation_queue.get()
    #             answer = self.languageProcessor.answer(message)
