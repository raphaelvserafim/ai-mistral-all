from flask import Blueprint, jsonify, request
from werkzeug.exceptions import NotFound   
from model.ai import generate
from utils.history_utils import load_history, save_history

bp = Blueprint('api', __name__)

@bp.route('/')
def index():
    return jsonify({'message': 'AI BluChat'})

@bp.route('/api/ask', methods=['POST'])
def ask():
    try:
        user_prompt = request.json.get('user_prompt', '')
        session = request.json.get('session', '')

        history = load_history(session)

        response = generate(user_prompt, history)

        answer = response.split('[/INST]')[-1].strip()

        history.append((user_prompt, answer))
        save_history(session, history)

        return jsonify({'status': 200, 'answer': answer})
    except Exception as e:
        error_message = str(e)
        return jsonify({'status': 500, 'message': error_message})
