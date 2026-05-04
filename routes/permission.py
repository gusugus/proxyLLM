from flask import Blueprint, request, jsonify
from services.permissions import send_permission

permission_bp = Blueprint("permission", __name__)

@permission_bp.route("/permission", methods=["POST"])
def permission():
    data = request.json

    ok = send_permission(data["request_id"], data["allow"])

    return jsonify({"ok": ok})