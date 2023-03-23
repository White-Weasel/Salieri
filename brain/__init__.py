from .LanguageProcessor import LanguageProcessor


class Brain:
    def __init__(self, **kwargs):
        if not kwargs.get('conversation'):
            self.conversation = ''
        self.languageProcessor = LanguageProcessor(model='gpt-3.5-turbo')
        pass
