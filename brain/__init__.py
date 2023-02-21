from . import LanguageProcessor


class Brain:
    def __init__(self):
        self.languageProcessor = LanguageProcessor.GptJ6B()
        pass
