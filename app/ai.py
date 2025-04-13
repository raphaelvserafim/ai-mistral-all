from llama_cpp import Llama
import os

MODEL_PATH = "./models/mistral.gguf"


llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=2048,  
    n_threads=os.cpu_count(),  
     use_mlock=True,  
       verbose=False,
    n_gpu_layers=0   
)
 
def format_prompt(message, history):
    prompt = "<s>"
    for item in history:
        if item["role"] == "user":
            prompt += f"[INST] {item['content']} [/INST]"
        elif item["role"] == "assistant":
            prompt += f"{item['content']}</s> "
    prompt += f"[INST] {message} [/INST]"
    return prompt

 


def generate_stream(message, history):

    formatted_prompt = format_prompt(message, history)

    output = llm(
        formatted_prompt,
        max_tokens=512,
        temperature=0.7,
        top_p=0.95,
        stream=True,
    )

    for token in output:
        yield token["choices"][0]["text"]
