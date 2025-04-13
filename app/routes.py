import json
import os
import asyncio
import secrets
from flask import Blueprint, stream_with_context, jsonify, request, Response
from app.ai import generate_stream

from app.db.queries import save_message, load_history, list_conversations
 
bp = Blueprint('api', __name__)


@bp.route('/')
def index():
    return jsonify({'message': 'AI API is running'})


@bp.route('/api/conversation', methods=['GET'])
def get_conversations():
    try:
        conversations = list_conversations()
        return jsonify({'status': 200, 'conversations': conversations})
    except Exception as e:
        return jsonify({'status': 500, 'message': str(e)})
    
@bp.route('/api/conversation', methods=['POST'])
def new_conversation():
    try:
        conversation_id = secrets.token_hex(10)

        return jsonify({'status': 200, 'conversation_id': conversation_id})
    except Exception as e:
        error_message = str(e)
        return jsonify({'status': 500, 'message': error_message}) 


@bp.route('/api/conversation/<conversation_id>', methods=['GET'])
def get_conversation_messages(conversation_id):
    try:
        messages = load_history(conversation_id)
        return jsonify({'status': 200, 'messages': messages})
    except Exception as e:
        return jsonify({'status': 500, 'message': str(e)})

@bp.route('/api/ask', methods=['POST'])
def ask_stream():
    prompt = request.json.get("content", "")
    conversation_id = request.json.get("conversation_id", "")

    if not conversation_id:
        return jsonify({"error": "conversation_id is required"}), 400

    history = load_history(conversation_id)
    response_text = ""

    @stream_with_context
    def generate():
        nonlocal response_text
        try:
            for chunk in generate_stream(prompt, history):
                response_text += chunk
                yield f"{chunk}"
            
            
            save_message(conversation_id, "user", prompt)
            save_message(conversation_id, "assistant", response_text)
    
        except GeneratorExit:
            pass
        except Exception as e:
            yield f"[error] {str(e)}"

    return Response(generate(), mimetype='text/event-stream')