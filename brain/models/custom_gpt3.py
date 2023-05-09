import os

import openai


class CustomGpt3:
    def __init__(self, brain=None, initial_prompt=None,
                 model=None, prompt_end_token=None, completion_end_token=None):
        if model is None:
            model = r"curie:ft-personal:salie-discord-with-username-prefix-2023-05-08-15-53-01"
        if prompt_end_token is None:
            prompt_end_token = '~##~'
        if completion_end_token is None:
            completion_end_token = '~#END#~'
        if initial_prompt is None:
            initial_prompt = []

        self.brain = brain
        self.conversation = initial_prompt
        self.model = model
        self.prompt_end_token = prompt_end_token
        self.completion_end_token = completion_end_token
        self.api_key = os.getenv("OPENAI_API_KEY")

    def answer(self, question, user=None, **kwargs):
        if not user:
            user = 'User'

        context = self.get_context(question, 3)
        if len(self.conversation) > 10:
            self.conversation = self.conversation[2:]
        self.conversation.append(f'{user}: {question}')
        conversation = '\n'.join(['@' + line for line in self.conversation])
        full_prompt = f"{context}\n{conversation}\n@Salie:{self.prompt_end_token}"
        answer = openai.Completion.create(model=self.model,
                                          prompt=full_prompt,
                                          temperature=0.7,
                                          max_tokens=500,
                                          top_p=1,
                                          frequency_penalty=0,
                                          presence_penalty=0,
                                          stop=[self.completion_end_token])
        answer = answer["choices"][0]["text"].strip()
        self.conversation.append(f'Salieri: {answer}')

        if self.brain:
            self.brain.memory.put(f"{user}: {question}\nSalieri: {answer}")
        return answer

    def get_context(self, message, limit):
        """Get context from memory"""
        if not self.brain:
            return ''
        memory = self.brain.memory.long_term_memory
        context = memory.conversation_search(message, limit)
        # add @ before usernames
        context = '\n'.join(['@' + line if line.split(' ')[0].endswith(':') else line for line in context.split('\n')])
        return context


if __name__ == '__main__':
    gpt = CustomGpt3()
    print(gpt.answer("Hello", user="QB"))
