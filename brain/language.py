import torch
from transformers import GPTNeoForCausalLM, GPT2Tokenizer
device = "cuda:0" if torch.cuda.is_available() else "cpu"
model = GPTNeoForCausalLM.from_pretrained("EleutherAI/gpt-neo-1.3B").to(device)
tokenizer = GPT2Tokenizer.from_pretrained("EleutherAI/gpt-neo-1.3B")


class LanguageProcessor:
    def __init__(self, prompt=None):
        if prompt:
            self.prompt = prompt
        else:
            self.prompt = (
                "###Human: Hello, who are you?"
                "###AI: I am an AI named Salieri. How can I help you today?###"
                "###Human: "
            )

    def conversation(self, question):
        self.prompt += question + '###AI: '
        input_ids = tokenizer(self.prompt, return_tensors="pt").to(device).input_ids
        gen_tokens = model.generate(
            input_ids,
            do_sample=True,
            temperature=0.9,
            max_length=len(self.prompt) + 45,
        )
        gen_text = tokenizer.batch_decode(gen_tokens)
        print(gen_text)
        gen_text = [text.replace(self.prompt, '') for text in gen_text]
        gen_text = [text[:text.index('###')].strip() for text in gen_text if '###' in text]
        answer = gen_text[0]
        self.prompt += answer + '###Human: '
        return answer
