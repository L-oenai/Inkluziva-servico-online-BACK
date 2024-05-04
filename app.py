from flask import Flask
from src.verifier_authenticate import auth_bp

app = Flask(__name__)

app.register_blueprint(auth_bp)

app.run(debug=True)