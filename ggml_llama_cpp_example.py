# need the llama-cpp-python package
# no GPU: pip install llama-cpp-python
# linux: CMAKE_ARGS="-DLLAMA_CUBLAS=on" pip install llama-cpp-python
# window: $env:CMAKE_ARGS = "-DLLAMA_OPENBLAS=on"
#         pip install llama-cpp-python
import argparse
import os

from llama_cpp import Llama

parser = argparse.ArgumentParser()
parser.add_argument("-m", "--model", type=str, default="/home/giang/data/llama-2-7b.Q4_K_M.gguf")
args = parser.parse_args()

llm = Llama(model_path=args.model)
prompt = "Question: What are the names of the planets in the solar system? Answer: "
stream = llm(
    prompt,
    max_tokens=48,
    stop=["Q:", "\n"],
    stream=True,
)
s = prompt
for output in stream:
    os.system("clear")
    s += output['choices'][0]['text']
    print(s)
