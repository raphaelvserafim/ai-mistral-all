import json
import os

HISTORY_FOLDER = 'conversations/'
PROMPTS_FOLDER = 'prompts/'

def load_history(session):
    file_path = f'{HISTORY_FOLDER}{session}.json'
    try:
        with open(file_path, 'r') as file:
            history = json.load(file)
        return history if isinstance(history, list) else []
    except FileNotFoundError:
        return []

def save_history(session, history):
    if not os.path.exists(HISTORY_FOLDER):
            os.makedirs(HISTORY_FOLDER)
            
    file_path = f'{HISTORY_FOLDER}{session}.json'
    with open(file_path, 'w') as file:
        json.dump(history, file)

def save_prompts(model, prompt):  
    formatted_prompt = '\n'.join([f'[INST] {line} [/INST]' for line in prompt.split('\n')])
    file_path = f'{PROMPTS_FOLDER}{model}.txt'
    if not os.path.exists(PROMPTS_FOLDER):
        os.makedirs(PROMPTS_FOLDER)
            
    with open(file_path, 'w') as file:
        file.write(formatted_prompt)

def read_prompt_from_file(model):
    try:
        file_path = f'{PROMPTS_FOLDER}{model}.txt'
        with open(file_path, 'r') as file:
            model_prompt = file.read()
            model_prompt = model_prompt.replace('[INST]', '<s></s>[INST]')
        return model_prompt
    except FileNotFoundError:
        return ""
    
def get_hidden_command():
    try:
        file_path = f'hidden_command.md'
        with open(file_path, 'r') as file:
            model_prompt = file.read()
        return model_prompt
    except FileNotFoundError:
        return ""
    
    
    