from flask import Flask
from flask_cors import CORS
from routes.chat import chat_bp
from routes.session import session_bp
from routes.permission import permission_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(chat_bp)
app.register_blueprint(session_bp)
app.register_blueprint(permission_bp)

if __name__ == "__main__":
    app.run(port=5000, debug=True)