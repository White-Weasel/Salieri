import json
import os
import requests


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
