import time
from transformers import pipeline, set_seed

generator = pipeline('text-generation', model='gpt2')
set_seed(int(time.time()))
res = generator("", max_length=30, num_return_sequences=5)
for i, mes in enumerate(res):
    print(f"{i}: {mes['generated_text']}")
