from transformers import GPTNeoForCausalLM, GPT2Tokenizer

model = GPTNeoForCausalLM.from_pretrained("EleutherAI/gpt-neo-1.3B")
tokenizer = GPT2Tokenizer.from_pretrained("EleutherAI/gpt-neo-1.3B")


class LanguageProcessor:
    def __init__(self, prompt=None):
        if prompt:
            self.prompt = prompt
        else:
            self.prompt = (
                "Human: Hello, who are you?###\n"
                "AI: I am an AI named Salieri. How can I help you today?###\n"
                "Human: "
            )

    def conversation(self, question):
        self.prompt += question
        input_ids = tokenizer(self.prompt, return_tensors="pt").input_ids
        gen_tokens = model.generate(
            input_ids,
            do_sample=True,
            temperature=0.9,
            max_length=len(self.prompt) + 45,
        )
        gen_text = tokenizer.batch_decode(gen_tokens)
        print(gen_text)
        gen_text = [text.replace(self.prompt + question, '') for text in gen_text]
        gen_text = [text[:text.index('###')].strip() for text in gen_text]
        answer = gen_text[0]
        return answer
