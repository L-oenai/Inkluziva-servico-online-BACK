from flask import Flask
from src.verifier_authenticate import auth_bp
from dotenv import load_dotenv
from waitress import serve
from flask_cors import CORS 
import os

load_dotenv()

port = os.getenv('PORT')

mode = 'produt'  # Alterado para 'prod' para diferenciar entre desenvolvimento e produção

app = Flask(__name__)
app.register_blueprint(auth_bp)

cors_config = {
    "origins": [
        "http://localhost:5173",
        "https://inkluziva-servio-online.netlify.app",
        "https://inkluziva-servio-online.netlify.app/register"
    ],  
    "methods": ["GET", "POST"],
    "allow_headers": ["Content-Type", "Authorization"]
}

CORS(app, resources={
    r"/authenticate": cors_config
})

if __name__ == '__main__':
    if mode == 'dev':
        app.run(host='0.0.0.0', port=8080, debug=True)
    else:
        serve(app, port=8041, url_scheme='https')
