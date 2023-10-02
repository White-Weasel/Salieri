# install ctransformers and download the model before running this script
# pip3 install --upgrade huggingface-hub>=0.17.1
# pip3 install --upgrade ctransformers>=0.2.24
# huggingface-cli download TheBloke/Llama-2-7B-GGUF llama-2-7b.Q4_K_M.gguf
import time
from ctransformers import AutoModelForCausalLM

# Set gpu_layers to the number of layers to offload to GPU. Set to 0 if no GPU acceleration is available on your system.
llm = AutoModelForCausalLM.from_pretrained("TheBloke/Llama-2-7B-GGUF", model_file="llama-2-7b.Q4_K_M.gguf",
                                           model_type="llama", gpu_layers=0)
s_time = time.perf_counter()
print(llm("AI is going to", max_new_tokens=200))
print(f"Generated after {time.perf_counter() - s_time} seconds")
