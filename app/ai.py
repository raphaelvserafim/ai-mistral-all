from llama_cpp import Llama
import os
import json

MODEL_PATH = "./models/mistral.gguf"
META_PATH = "./dataset/instruction.json"

llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=4096,  
    n_threads=os.cpu_count(),   
    use_mlock=True,   
    verbose=False,   
    n_gpu_layers=-1 
)

def build_instruction_context():
    with open(META_PATH, "r") as f:
        instructions = json.load(f)
    prompt = "<s>"
    for item in instructions: 
        prompt += f"[INST] {item['instruction']} [/INST]{item['output']}</s> "
    return prompt

def format_prompt(message, history):
    prompt = ""
    for item in history: 
        if item["role"] == "user":
            prompt += f"[INST] {item['content']} [/INST]"
        elif item["role"] == "assistant":
            prompt += f"{item['content']}</s> "
    prompt += f"[INST] {message} [/INST]"
    return prompt

def generate_stream(message, history):
    context = build_instruction_context()
    chat_prompt = format_prompt(message, history)
    full_prompt = f"{context}{chat_prompt}"
    
    output = llm(
        full_prompt,
        max_tokens=100,  
        temperature=0.5,  
        top_p=0.8,
        stream=True
    )
    
    for token in output:
        yield token["choices"][0]["text"]

 