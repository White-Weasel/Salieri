# TODO: process the answer before showing it would reduce the response time.
import logging
from typing import Union, Type
from .models import ChatGPT, Gpt3, GptJ6B

logger = logging.getLogger(__name__)


class LanguageProcessor:
    def __init__(self, model: Type[Union[ChatGPT, Gpt3, GptJ6B]], initial_prompt=None, *args, **kwargs):
        self.conversation = None
        self.initial_prompt = initial_prompt
        self.model = model(initial_prompt=initial_prompt, *args, **kwargs)

    def answer(self, message):
        answer = self.model.answer(message)
        logger.debug(f"Brain answer: {answer}")
        self.conversation = self.model.conversation
        return answer
