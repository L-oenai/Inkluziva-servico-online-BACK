from flask import Blueprint, redirect
import oauth2 as oauth
import urllib.parse
import os
from dotenv import load_dotenv
from flask_cors import cross_origin

load_dotenv()

# Carregar variáveis de ambiente
consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
request_token_url = os.getenv("REQUEST_TOKEN_URL")
authenticate_url = os.getenv("AUTHENTICATE_URL")
access_token_url = os.getenv("ACCESS_TOKEN_URL")

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/proxy_authenticate', methods=['GET'])
@cross_origin(origins=['https://inkluziva-servio-online.netlify.app', 'https://inkluziva-servio-online.netlify.app/register', 'http://localhost:5173'])
def proxy_authenticate():
    try:
        # Criando um cliente OAuth
        consumer = oauth.Consumer(consumer_key, consumer_secret)
        client = oauth.Client(consumer)

        # Solicitando oauth_token
        resp_oauth_token, content_oauth_token = client.request(request_token_url, 'GET')
        if resp_oauth_token['status'] != '200':
            raise Exception('Falha ao obter token de requisição: %s' % resp_oauth_token['status'])

        # Gerando o oauth_token
        content_oauth_token_str = content_oauth_token.decode('utf-8')
        oauth_token_params = urllib.parse.parse_qs(content_oauth_token_str)
        oauth_token = oauth_token_params['oauth_token'][0]
        oauth_verifier_url = f"{authenticate_url}?oauth_token={oauth_token}"
        
        print("Retornando URL de acesso...")

        # Redirecionar para a oauth_verifier_url
        return redirect(oauth_verifier_url)
    except Exception as e:
        return str(e), 500