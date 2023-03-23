class LanguageProcessor:
    def __init__(self, model, initial_prompt='', *args, **kwargs):
        self.model = model
        self.initial_prompt = initial_prompt
