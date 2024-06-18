from flask import Blueprint, redirect
import oauth2 as oauth
import urllib.parse
import os
from requests import request
from dotenv import load_dotenv
from flask_cors import cross_origin
import logging
from flask import Blueprint, request, jsonify
from flask_cors import cross_origin

load_dotenv()

# Carregar variáveis de ambiente
consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
request_token_url = os.getenv("REQUEST_TOKEN_URL")
authenticate_url = os.getenv("AUTHENTICATE_URL")
access_token_url = os.getenv("ACCESS_TOKEN_URL")

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/authenticate', methods=['GET'])
@cross_origin(origins=['https://inkluziva-servio-online.netlify.app', 'https://inkluziva-servio-online.netlify.app/register', 'http://localhost:5173', 'http://localhost:5173/register'])
def authenticate():
    try:
        # Criando um cliente OAuth
        consumer = oauth.Consumer(consumer_key, consumer_secret)
        client = oauth.Client(consumer)

        # Solicitando oauth_token
        resp_oauth_token, content_oauth_token = client.request(request_token_url, 'GET')
        if resp_oauth_token['status'] != '200':
            raise Exception('Falha ao obter token de requisição: %s' % resp_oauth_token['status'])

        print(f"resp_oauth_token: {resp_oauth_token}, content_oauth_token: {content_oauth_token}")

        # Gerando o oauth_token
        content_oauth_token_str = content_oauth_token.decode('utf-8')
        oauth_token_params = urllib.parse.parse_qs(content_oauth_token_str)
        oauth_token = oauth_token_params['oauth_token'][0]
        oauth_verifier_url = f"{authenticate_url}?oauth_token={oauth_token}"
        
        print("Retornando URL de acesso...")

        # Redirecionar para a oauth_verifier_url
        print(oauth_verifier_url)
        return oauth_verifier_url
    except Exception as e:
        return str(e), 500

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@auth_bp.route('/token', methods=['POST'])
@cross_origin(origins=[
    'https://inkluziva-servio-online.netlify.app',
    'https://inkluziva-servio-online.netlify.app/register',
    'http://localhost:5173',
    'http://localhost:5173/register'
])
def token():
    try:
        consumer = oauth.Consumer(consumer_key, consumer_secret)

        data = request.json
        if not data or 'oauth_verifier' not in data or 'oauth_token' not in data:
            raise ValueError("oauth_verifier or oauth_token is missing from the request")

        oauth_verifier = data['oauth_verifier']
        oauth_token = data['oauth_token']
        logger.info(f"OAuth verifier received: {oauth_verifier}")
        logger.info(f"OAuth token received: {oauth_token}")

        # Step 1: Create a token with the oauth_token received and an empty secret
        token = oauth.Token(oauth_token, "")
        token.set_verifier(oauth_verifier)
        client = oauth.Client(consumer, token)

        # Step 2: Request the access token from Twitter
        resp, content = client.request(access_token_url, "POST")
        if resp.status != 200:
            raise Exception('Failed to obtain access token: %s' % resp.status)

        # Step 3: Parse the response
        content_str = content.decode('utf-8')
        access_token_data = urllib.parse.parse_qs(content_str)
        access_token_data = {key: value[0] for key, value in access_token_data.items()}

        # Access token and secret
        access_token = access_token_data.get('oauth_token')
        access_token_secret = access_token_data.get('oauth_token_secret')

        # User data
        user_id = access_token_data.get('user_id')
        screen_name = access_token_data.get('screen_name')

        return jsonify({
            "message": "Token received successfully",
            "access_token": access_token,
            "access_token_secret": access_token_secret,
            "user_id": user_id,
            "screen_name": screen_name
        }), 200
    except Exception as e:
        logger.error(f"Error receiving token: {str(e)}", exc_info=True)
        return jsonify({"error": "An error occurred while processing your request."}), 500

