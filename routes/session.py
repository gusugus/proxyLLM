from flask import Blueprint, jsonify
from services.llama_agent import create_session

session_bp = Blueprint("session", __name__)

@session_bp.route("/session", methods=["POST"])
def new_session():
    session_id = create_session()
    return jsonify({"session_id": session_id})