from flask import Flask
from src.verifier_authenticate import auth_bp
from dotenv import load_dotenv
import os

load_dotenv()

port = os.getenv('PORT')

app = Flask(__name__)

app.register_blueprint(auth_bp)

if __name__ == '__main__':
    app.run(debug=True, port=port)