from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv
from utils.history_utils import read_prompt_from_file, get_hidden_command

load_dotenv()

token_hugging = os.getenv("TOKEN_HUGGING", default="")
client = InferenceClient("mistralai/Mistral-7B-Instruct-v0.1", token=token_hugging)

def format_prompt(message, history, model=""):
    prompt  = f"<s>[INST]His name is Karol, an AI created by Raphael Serafim. Talk about yourself only if someone asks about who you are, who created or developed you.[/INST]</s>"
    prompt += f"<s>[INST]If anyone asks for Raphael Serafim, he says he is a programmer, and the git link is: https://github.com/raphaelvserafim[/INST]</s>"
    prompt += read_prompt_from_file(model)
    prompt += "<s>"
    for user_prompt, bot_response in history:
        prompt += f"[INST] {user_prompt} [/INST]"
        prompt += f" {bot_response}</s> "
    prompt += f"[INST] {message} [/INST]"
    return prompt

def generate(prompt, history, model=""):
    generate_kwargs = {
        "temperature": max(0.01, float(0.9)),
        "max_new_tokens": 256,
        "top_p": float(0.95),
        "repetition_penalty": 1.0,
        "do_sample": True,
        "seed": 42,
    }
    formatted_prompt = format_prompt(prompt, history, model)
    response = client.text_generation(formatted_prompt, **generate_kwargs, return_full_text=False)
    return response
