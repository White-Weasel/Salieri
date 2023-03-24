import json
import os
import logging
import openai
import requests

logger = logging.getLogger(__name__)


class Gpt3:
    def __init__(self, initial_prompt=None, model='text-davinci-003'):
        if initial_prompt:
            self.prompt = initial_prompt
        else:
            self.prompt = """
            Marv is a clever person who reluctantly answers questions with sarcastic responses:
            You: How many pounds are in a kilogram?
            Marv: This again? There are 2.2 pounds in a kilogram. Please make a note of this.
            You: What does HTML stand for?
            Marv: Was Google too busy? Hypertext Markup Language. The T is for try to ask better questions in the future.
            You: When did the first airplane fly?
            Marv: On December 17, 1903, Wilbur and Orville Wright made the first flights. I wish they’d come and take me away.
            You: What is the meaning of life?
            Marv: I’m not sure. I’ll ask my friend Google.
            You: """
        self.model = model
        self.api_key = os.getenv("OPENAI_API_KEY")

    def answer(self, question, **kwargs):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.prompt += question
        answer = openai.Completion.create(model=self.model, prompt=self.prompt,
                                          temperature=0.5, max_tokens=100, **kwargs)
        answer = answer["choices"][0]["text"]
        self.prompt += answer
        answer = answer[answer.index('Marv: ') + 6:]
        return answer


class ChatGPT:
    def __init__(self, model='gpt-3.5-turbo', initial_prompt=None, temperature=0.4):
        if not initial_prompt:
            # noinspection PyPep8
            initial_prompt = '''Marv is a informal person who answers questions with comedic, sarcastic responses. When he can't do something, Marv will says he forgot how to do it or asks for more information instead. Marv don't know about programming. Answer questions as Marv. Never break character.'''
            self.conversation = [
                {"role": "system", "content": initial_prompt},
            ]
        elif isinstance(initial_prompt, list):
            self.conversation = initial_prompt
        else:
            self.conversation = []

        self.model = model
        self.temperature = temperature

    def answer(self, message, role='user'):
        self.conversation.append({"role": role, "content": message})
        response = openai.ChatCompletion.create(
            model=self.model,
            temperature=self.temperature,
            messages=self.conversation
        )
        response = response['choices'][0]['question']['content']
        self.conversation.append({"role": "assistant", "content": response})
        return response


class GptJ6B:
    def __init__(self, api_key=None, prompt=None, model='EleutherAI/gpt-j-6B'):
        if prompt:
            self.prompt = prompt
        else:
            self.prompt = "###Human: Hello\n###AI: Hi\n###Human: What is your name?\n###AI: My name is Salieri.\n" \
                          "###Human: What are you?\n###AI: I am an AI.\n###Human: Can you tell me your name again?\n" \
                          "###AI: Yes, I am an Artificial Intelligence named Salieri.\n###Human: "
        if api_key:
            self.api_key = api_key
        else:
            self.api_key = os.getenv('hf_api_key')
        self.model = model

    def answer(self, question):
        self.prompt += question + '\n###AI: '
        try:
            payload = {
                "wait_for_model": True,
                "inputs": self.prompt,
                "parameters": {
                    "do_sample": True,
                    "max_new_tokens": 30,
                    "penalty_alpha": 0.6,
                    "top_k": 4
                }
            }
            headers = {"Authorization": f"Bearer {self.api_key}"}
            res = requests.post(rf"https://api-inference.huggingface.co/models/{self.model}",
                                headers=headers, data=json.dumps(payload))
            res = res.json()
            answer = res[0]['generated_text']
            answer = answer.replace(self.prompt, '')
            if '###' in answer:
                answer = answer[:answer.index('###')].strip()
            else:
                assert 'Human: ' not in answer
            self.prompt += answer + '\n###Human:'
        except Exception as e:
            self.prompt.replace(question + '\n###AI: ', '')
            raise e
        return answer
