from llama_cpp import Llama
import os
import json
import multiprocessing

MODEL_PATH = "./models/deepseek.gguf"
META_PATH = "./dataset/instruction.json"

llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=2048,  
    n_threads=multiprocessing.cpu_count(),   
    use_mlock=True,   
    verbose=False,   
    n_gpu_layers=-1,
    n_batch=512
)

 
def build_instruction_context():
    with open(META_PATH, "r") as f:
        instructions = json.load(f)
    return instructions

 
def format_prompt(message, history):
    prompt = ""
    for item in history: 
        if item["role"] == "user":
            prompt += f"User: {item['content']}\n"
        elif item["role"] == "assistant":
            prompt += f"Assistant: {item['content']}\n"
    prompt += f"User: {message}\n"  
    return prompt


def generate_stream(message, history):
    instructions = build_instruction_context() 
    output = llm.create_chat_completion(
        messages= instructions + history + [
            {"role": "user", "content": message},
        ],
        stream=True
    )
     
    response = ""
    for token in output:
        content = (
            token.get("choices", [{}])[0]
                 .get("delta", {})
                 .get("content")
        )
        if content:
            yield content