import json

HISTORY_FOLDER = 'conversations/'

def load_history(session):
    file_path = f'{HISTORY_FOLDER}{session}.json'
    try:
        with open(file_path, 'r') as file:
            history = json.load(file)
        return history if isinstance(history, list) else []
    except FileNotFoundError:
        return []

def save_history(session, history):
    file_path = f'{HISTORY_FOLDER}{session}.json'
    with open(file_path, 'w') as file:
        json.dump(history, file)
