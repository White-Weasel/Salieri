# TODO: process the answer before showing it would reduce the response time.
import logging
from typing import Union, Type
from .models import ChatGPT, Gpt3, GptJ6B

logger = logging.getLogger(__name__)


class LanguageProcessor:
    def __init__(self, brain, model: Type[Union[ChatGPT, Gpt3, GptJ6B]], initial_conversation=None, *args, **kwargs):
        self.brain = brain
        self.conversation = None
        self.initial_conversation = initial_conversation
        self.model = model(brain, initial_prompt=initial_conversation, *args, **kwargs)

    def answer(self, message):
        answer = self.model.answer(message)
        logger.debug(f"Brain answer: {answer}")
        self.conversation = self.model.conversation
        return answer
