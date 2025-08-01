from flask import Blueprint, request, jsonify
from .broker import publish_event

api = Blueprint('api', __name__)

@api.route('/publish', methods=['POST'])
def publish():
    data = request.get_json()
    if not data or 'routing_key' not in data or 'body' not in data:
        return jsonify({"error": "Invalid payload. 'routing_key' and 'body' are required."}), 400

    routing_key = data['routing_key']
    body = data['body']
    
    try:
        publish_event(routing_key, body)
        return jsonify({"message": "Event published successfully"}), 202 # 202 Accepted
    except Exception as e:
        return jsonify({"error": str(e)}), 500
