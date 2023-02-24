from . import LanguageProcessor


class Brain:
    def __init__(self):
        self.languageProcessor = LanguageProcessor.Gpt3()
        pass
