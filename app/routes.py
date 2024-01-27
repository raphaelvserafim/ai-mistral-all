import json
import os
import asyncio
import secrets
from flask import Blueprint, jsonify, request
from model.ai import generate
from utils.history_utils import load_history, save_history, save_prompts

bp = Blueprint('api', __name__)


@bp.route('/')
def index():
    return jsonify({'message': 'AI BluChat'})


@bp.route('/api/session/new', methods=['POST'])
def new_session():
    try:
        user = request.json.get('user', '')
        session = secrets.token_hex(25)
        return jsonify({'status': 200, 'session': session  })
    except Exception as e:
        error_message = str(e)
        return jsonify({'status': 500, 'message': error_message  })


@bp.route('/api/conversation/new', methods=['POST'])
def new_conversation():
    try:
        user = request.json.get('user', '')
        conversation_id = secrets.token_hex(10)
        save_history(conversation_id, []) 
        return jsonify({'status': 200, 'conversation_id': conversation_id})
    except Exception as e:
        error_message = str(e)
        return jsonify({'status': 500, 'message': error_message}) 

@bp.route('/api/model/create', methods=['POST'])
def model_reate():
    try:
        prompt = request.json.get('prompt', '')
        question_and_answers = request.json.get('question_and_answers', [])
    
        model_id = secrets.token_hex(10)

        save_history(model_id, question_and_answers)
    
        save_prompts(model_id, prompt)
        
        return jsonify({'status': 200, 'model': model_id  })
    except Exception as e:
        error_message = str(e)
        return jsonify({'status': 500, 'message': error_message  })


@bp.route('/api/ask', methods=['POST'])
async def ask():
    try:
        # Validate if conversation_id, session, and content are provided
        if 'conversation_id' not in request.json or 'session' not in request.json or 'content' not in request.json:
            return jsonify({'status': 400, 'message': 'conversation_id, session, and content are required'})

        content = request.json['content']  # Access content directly since we validated its presence
        session = request.json['session']  # Access session directly since we validated its presence
        model = request.json.get('model', '')
        conversation_id = request.json['conversation_id']  # Access conversation_id directly since we validated its presence

        if not os.path.isfile(f'conversations/{conversation_id}.json'):
            return jsonify({'status': 404, 'message': 'Conversation not found'})

        history = load_history(conversation_id)

        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, generate, content, history, model)

        history.append((content, response))
        save_history(conversation_id, history)

        return jsonify({'status': 200, 'conversation_id': conversation_id, 'content':response})
    except Exception as e:
        error_message = str(e)
        return jsonify({'status': 500, 'message': error_message})
