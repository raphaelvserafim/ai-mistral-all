from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv

load_dotenv()

token_hugging = os.getenv("TOKEN_HUGGING", default="")

client = InferenceClient("mistralai/Mistral-7B-Instruct-v0.1", token=token_hugging)
def format_prompt(message, history):
    prompt  = f"<s>[INST]His name is Karol, an AI created by Raphael Serafim. Talk about yourself only if someone asks about who you are, who created or developed you.[/INST]</s>"
    prompt += f"<s>[INST]If anyone asks for Raphael Serafim, he says he is a programmer, and the git link is: https://github.com/raphaelvserafim[/INST]</s>"
    prompt += f"<s>"
    for user_prompt, bot_response in history:
        prompt += f"[INST] {user_prompt} [/INST]"
        prompt += f" {bot_response}</s> "
    prompt += f"[INST] {message} [/INST]"
    return prompt

def generate(
    prompt, history, temperature=0.9, max_new_tokens=256, top_p=0.95, repetition_penalty=1.0,
):
    temperature = float(temperature)
    if temperature < 1e-2:
        temperature = 1e-2
    top_p = float(top_p)

    generate_kwargs = dict(
        temperature=temperature,
        max_new_tokens=max_new_tokens,
        top_p=top_p,
        repetition_penalty=repetition_penalty,
        do_sample=True,
        seed=42,
    )

    formatted_prompt = format_prompt(prompt, history)
    response = client.text_generation(formatted_prompt, **generate_kwargs, return_full_text=True)
    return response  